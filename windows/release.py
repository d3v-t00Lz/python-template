# Run this script from Windows, not MSYS2

from glob import glob
import argparse
import json
import os
import re
import shutil
import subprocess

from jinja2 import Template

CWD = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
    ),
)
os.chdir(CWD)

SPEC_FILES = [os.path.basename(x) for x in glob('windows/*.spec')]
assert len(SPEC_FILES) >= 1, 'no spec_files available'

def parse_args():
    parser = argparse.ArgumentParser('Create Windows packages')
    if len(SPEC_FILES) > 1:
        parser.add_argument(
            'spec_file',
            choices=SPEC_FILES,
            help='The Pyinstaller spec file to use.',
        )
    return parser.parse_args()

args = parse_args()
if len(SPEC_FILES) == 1:
    SPEC_FILE = SPEC_FILES[0]
else:
    SPEC_FILE = args.spec_file
PREFIX, SUFFIX = re.match('([a-z]+)-([a-z0-9]+).spec', SPEC_FILE).groups()

with open('meta.json') as f:
    META = json.load(f)

MAJOR_VERSION = 'pytemplate'
from pytemplate import __version__ as MINOR_VERSION

for path in glob(f'dist/*_{SUFFIX}'):
    if os.path.isdir(path):
        shutil.rmtree(path)

print("Running Pyinstaller")
subprocess.check_call(["pyinstaller", f"windows/{SPEC_FILE}"])

if PREFIX == 'onedir':
    with open('windows/nsis.jinja') as f:
        TEMPLATE = Template(f.read())

    template = TEMPLATE.render(
        MINOR_VERSION=MINOR_VERSION,
        MAJOR_VERSION=MAJOR_VERSION,
        MAJOR_VERSION_NUM=1,
        ORG=META['org'],
        SUFFIX=SUFFIX,
    )
    template_name = "{0}.nsi".format(MAJOR_VERSION)
    with open(template_name, "w") as f:
        f.write(template)

    NSIS = r"C:\Program Files (x86)\NSIS\Bin\makensis.exe"
    print("Running NSIS")
    subprocess.check_call([NSIS, template_name])

