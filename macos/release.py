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
    parser.set_defaults(func=parser.print_help)
    subparsers = parser.add_subparsers()
    dmg = subparsers.add_parser(
        'dmg',
        description='Create a DMG installer of a single user interface',
    )
    dmg.set_defaults(func=create_dmg)
    if len(SPEC_FILES) > 1:
        dmg.add_argument(
            'choice',
            choices=list(CHOICES),
            help='The user interface to build and package',
        )
    pkg = subparsers.add_parser(
        'pkg',
        description='Create a PKG installer of all user interfaces',
    )
    pkg.set_defaults(func=create_pkg)
    return parser.parse_args()

with open('meta.json') as f:
    META = json.load(f)
PRODUCT = META['product']
from pytemplate import __version__ as VERSION

ARCH_NAMES = {
    'x86_64': 'intel',
    'arm64': 'm1',
}

def create_dmg():
    if len(SPEC_FILES) == 1:
        SPEC_FILE = SPEC_FILES[0]
    else:
        SPEC_FILE = CHOICES[args.choice]
    SUFFIX = args.choice
    DISPLAY_NAME = META['display_name'][SUFFIX]
    BUNDLE = f"{DISPLAY_NAME}.app"

    #for BUNDLE in glob('dist/*.app'):
    #    if os.path.isdir(BUNDLE):
    #        shutil.rmtree(BUNDLE)

    subprocess.check_call([
        'pyinstaller',
        '--noconfirm',
        f'macos/{SPEC_FILE}',
    ])

    os.chdir('dist')
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

def create_pkg():
    PKG = f'{PRODUCT}-{VERSION}-macos-{ARCH_NAMES[ARCH]}-{ARCH}.pkg'
    pb_args = []
    for SUFFIX, SPEC_FILE in CHOICES.items():
        pb_args.append('--package')
        pb_args.append(f'{SUFFIX}.pkg')
        DISPLAY_NAME = META['display_name'][SUFFIX]
        subprocess.check_call([
            'pyinstaller',
            '--noconfirm',
            f'macos/{SPEC_FILE}',
        ])
        subprocess.check_call([
            'pkgbuild',
            '--root', f"dist/{DISPLAY_NAME}.app",
            '--identifier', f'com.github.pytemplate_{SUFFIX}',
            '--scripts', 'macos/Scripts',
            '--install-location', f"/Applications/{DISPLAY_NAME}.app",
            f'dist/{SUFFIX}.pkg',
        ])
    os.chdir('dist')
    subprocess.check_call([
        'productbuild',
        *pb_args,
        PKG,
    ])

if __name__ == '__main__':
    args = parse_args()
    args.func()
