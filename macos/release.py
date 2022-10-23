#!/usr/bin/env python3

from glob import glob
import argparse
import json
import os
import platform
import re
import shutil
import subprocess


def suffix(
    spec_file,
    pattern='.*-([a-z0-9]+).spec',
):
    match = re.match(pattern, spec_file)
    assert match, f'"{spec_file}" does not match pattern {pattern}'
    return match.groups()[0]

ARCH = platform.machine()

CWD = os.path.abspath(
        os.path.join(
        os.path.dirname(__file__),
        '..',
    ),
)
os.chdir(CWD)

SPEC_FILES = [os.path.basename(x) for x in glob('macos/onedir*.spec')]
assert len(SPEC_FILES) >= 1, 'no spec_files available'
CHOICES = {suffix(x): x for x in SPEC_FILES}

def parse_args():
    parser = argparse.ArgumentParser('Create MacOS packages')
    if len(SPEC_FILES) > 1:
        parser.add_argument(
            'choice',
            choices=list(CHOICES),
            help='The user interface to build and package',
        )
    return parser.parse_args()

args = parse_args()
if len(SPEC_FILES) == 1:
    SPEC_FILE = SPEC_FILES[0]
else:
    SPEC_FILE = CHOICES[args.choice]
SUFFIX = args.choice
with open('meta.json') as f:
    META = json.load(f)
PRODUCT = META['product']
DISPLAY_NAME = META['display_name'][SUFFIX]
BUNDLE = f"{DISPLAY_NAME}.app"

from pytemplate import __version__ as VERSION

#for BUNDLE in glob('dist/*.app'):
#    if os.path.isdir(BUNDLE):
#        shutil.rmtree(BUNDLE)

retcode = subprocess.check_call([
    'pyinstaller',
    '--noconfirm',
    f'macos/{SPEC_FILE}',
])

os.chdir('dist')

ARCH_NAMES = {
    'x86_64': 'intel',
    'arm64': 'm1',
}

DMG = f'{PRODUCT}_{SUFFIX}-{VERSION}-macos-{ARCH_NAMES[ARCH]}-{ARCH}.dmg'
if os.path.exists(DMG):
    os.remove(DMG)

subprocess.check_call([
    'create-dmg',
    '--volname', f'{DISPLAY_NAME}',
    '--icon', BUNDLE, '128', '128',
    '--hide-extension', BUNDLE,
    '--app-drop-link', '384', '128',
    '--icon-size', '128',
    '--window-size', '512', '384',
    '--format', 'UDBZ',
    DMG,
    BUNDLE,
])

