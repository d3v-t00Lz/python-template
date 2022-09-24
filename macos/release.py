#!/usr/bin/env python3

from glob import glob
import argparse
import json
import os
import platform
import re
import shutil
import subprocess


HOME = os.path.expanduser('~')
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

def parse_args():
    parser = argparse.ArgumentParser('Create MacOS packages')
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
SUFFIX = re.match('.*-([a-z0-9]+).spec', SPEC_FILE).groups()[0]

MAJOR_VERSION = 'pytemplate'
from pytemplate import __version__ as VERSION

BUNDLE = f'dist/{MAJOR_VERSION}.app'
if os.path.isdir(BUNDLE):
    shutil.rmtree(BUNDLE)

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

DMG = f'pytemplate{VERSION}-macos-{ARCH_NAMES[ARCH]}-{ARCH}.dmg'
if os.path.exists(DMG):
    os.remove(DMG)

subprocess.check_call([
    'create-dmg',
    '--format', 'UDBZ',
    DMG,
    f'{MAJOR_VERSION}_{SUFFIX}.app',
])

