#!/usr/bin/env python3

from glob import glob
import argparse
import importlib
import json
import os
import pkgutil
import platform
import re
import shutil
import subprocess
import sys


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
    parser.add_argument(
        '--compile',
        action='store_true',
        default=False,
        help='Transpile to C using Nuitka and compile using clang',
    )
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
    else:
        dmg.add_argument(
            '--choice',
            choices=list(CHOICES),
            default=list(CHOICES.keys())[0],
            dest='choice',
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

def create_bundle_pyinstaller():
    if len(SPEC_FILES) == 1:
        SPEC_FILE = SPEC_FILES[0]
    else:
        SPEC_FILE = CHOICES[args.choice]
    subprocess.check_call([
        'pyinstaller',
        '--noconfirm',
        f'macos/{SPEC_FILE}',
    ])

def recurse_modules(
    root_name: str,
):
    """ Recursively list submodules of @root_name
        Necessary because of the machinery used to implement subcommands,
        importlib.import_module is not seen by pyinstaller, therefore
        we need to enumerate the submodules here.
    """
    yield root_name
    root_mod = importlib.import_module(root_name)
    for sub_info in pkgutil.iter_modules(root_mod.__path__):
        sub_name = '.'.join((root_name, sub_info.name))
        yield sub_name
        sub_mod = importlib.import_module(sub_name)
        if sub_info.ispkg:
            for mod_name in recurse_modules(sub_name):
                yield mod_name

def nuitka_modules(root_name: str):
    return [
        f'--include-module={x}'
        for x in recurse_modules(root_name)
    ]

# PT:SDL2
import sdl2dll
SDL2_DATA_ARGS = [
    f'--include-data-dir={x}={os.path.basename(x)}'
    if os.path.isdir(x) else
    f'--include-data-file={x}={os.path.basename(x)}'
    for x in glob(os.path.join(sdl2dll.get_dllpath(), '*'))
]
# PT:SDL2

NUITKA_TARGETS = [
    # PT:SDL2
    (
        'pytemplate_sdl2', 
        SDL2_DATA_ARGS,
    ),
    # PT:SDL2
    # PT:CLI
    ('pytemplate_cli', []),
    # PT:CLI
    # PT:QT
    (
        'pytemplate_qt',
        [
            '--include-module=pytemplate_qt',
            '--include-qt-plugins=platform,sensible',
            '--enable-plugin=pyqt6',
        ],
    ),
    # PT:QT
]

def create_bundle_nuitka():
    print("Running Nuitka")
    scripts_dir = os.path.join(
        os.path.dirname(__file__),
        '..',
        'scripts',
    )
    os.makedirs('dist', exist_ok=True)
    assert NUITKA_TARGETS, 'No targets'
    for script, nuitka_args in NUITKA_TARGETS:
        nuitka_call = [
            sys.executable,
            '-m', 'nuitka',
            '--standalone',
            *nuitka_modules('pytemplate'),
            *nuitka_modules(script),
            *nuitka_args,
            f'--macos-target-arch={ARCH}',
            '--macos-create-app-bundle',
            '--macos-app-icon=files/icons/pytemplate.icns',
            f"--macos-app-name='Python Template'",
            '--macos-signed-app-name=com.github.d3v-t00lz.pytemplate',
            '--macos-app-mode=gui',
            f'--macos-app-version={VERSION}',
            os.path.join('scripts', script),
        ]
        print(nuitka_call)
        subprocess.check_call(nuitka_call)
        if os.path.exists(f'dist/{script}'):
            shutil.rmtree(f'dist/{script}')
        shutil.move(f'{script}.app', f'dist/{script}.app')

def create_dmg():
    SUFFIX = args.choice
    DISPLAY_NAME = META['display_name'][SUFFIX]
    BUNDLE = f"{DISPLAY_NAME}.app"
    if args.compile:
        create_bundle_nuitka()
    else:
        create_bundle_pyinstaller()
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
    #
    #subprocess.check_call([
    #    'codesign',
    #    '--force',
    #    '--sign',
    #    'TODO: Add your codesiging identity',
    #    DMG,
    #])


def create_pkg():
    PKG = f'{PRODUCT}-{VERSION}-macos-{ARCH_NAMES[ARCH]}-{ARCH}.pkg'
    pb_args = []
    if args.compile:
        create_bundle_nuitka()
    for SUFFIX, SPEC_FILE in CHOICES.items():
        pb_args.append('--package')
        pb_args.append(f'{SUFFIX}.pkg')
        DISPLAY_NAME = META['display_name'][SUFFIX]
        if not args.compile:
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
        # '--sign', 'TODO: Add your codesigning identity',
        *pb_args,
        PKG,
    ])

if __name__ == '__main__':
    args = parse_args()
    args.func()
