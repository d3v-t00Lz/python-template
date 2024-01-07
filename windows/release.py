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

SPEC_FILES = [os.path.basename(x) for x in glob('windows/onedir*.spec')]

def parse_args():
    parser = argparse.ArgumentParser('Create Windows packages')
    parser.add_argument(
        '--compile',
        action='store_true',
        default=False,
        help=(
            'Transpile Python code to C, and compile using a '
            'C compiler',
        )
    )
    parser.add_argument(
        '--nsis-path',
        default=r"C:\Program Files (x86)\NSIS\Bin\makensis.exe",
        dest='nsis_path',
        help='The full path to the NSIS executable',
    )
    return parser.parse_args()

with open('meta.json') as f:
    META = json.load(f)

args = parse_args()
MAJOR_VERSION = META['product']
DISPLAY_NAME = META['display_name']['all']
from pytemplate import __version__ as MINOR_VERSION

def pyinstaller():
    for SPEC_FILE in SPEC_FILES:
        _, SUFFIX = re.match('([a-z]+)-([a-z0-9]+).spec', SPEC_FILE).groups()
        for path in glob(f'dist/*_{SUFFIX}'):
            if os.path.isdir(path):
                shutil.rmtree(path)

        print("#" * 80)
        print(f"\n\nRunning Pyinstaller on {SPEC_FILE}\n\n")
        print("#" * 80)
        subprocess.check_call(["pyinstaller", f"windows/{SPEC_FILE}"])

    with open('windows/nsis.jinja') as f:
        TEMPLATE = Template(f.read())

    template = TEMPLATE.render(
        DISPLAY_NAME=DISPLAY_NAME,
        MINOR_VERSION=MINOR_VERSION,
        MAJOR_VERSION=MAJOR_VERSION,
        MAJOR_VERSION_NUM=1,
        ORG=META['org'],
    )
    template_name = "{0}.nsi".format(MAJOR_VERSION)
    with open(template_name, "w") as f:
        f.write(template)


def nuitka():
    print("Running Nuitka")
    scripts_dir = os.path.join(
        os.path.dirname(__file__),
        '..',
        'scripts',
    )
    for script in os.listdir(scripts_dir):
        subprocess.check_call([
            sys.executable,
            '-m', 'nuitka',
            '--standalone',
            '--windows-disable-console',
            '--include-qt-plugins=platform,sensible',
            '--enable-plugin=pyqt6',
            script,
        ])

        os.makedirs('dist', exist_ok=True)
        if os.path.exists(f'dist/{script}'):
            shutil.rmtree(f'dist/{script}')
        shutil.move(f'{script}.dist', f'dist/{script}')

if args.compile:
    nuitka()
else:
    pyinstaller()

print("Running NSIS")
subprocess.check_call([args.nsis_path, template_name])

