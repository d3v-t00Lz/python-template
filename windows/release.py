# Run this script from Windows, not MSYS2

from glob import glob
import argparse
import importlib
import json
import pkgutil
import os
import re
import shutil
import subprocess
import sys

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
            'C compiler'
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
            #'--windows-disable-console',
            '--include-qt-plugins=platform,sensible',
            '--enable-plugin=pyqt6',
        ],
    ),
    # PT:QT
]

def nuitka():
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
            os.path.join('scripts', script),
        ]
        print(nuitka_call)
        subprocess.check_call(nuitka_call)
        if os.path.exists(f'dist/{script}'):
            shutil.rmtree(f'dist/{script}')
        shutil.move(f'{script}.dist', f'dist/{script}')

if args.compile:
    nuitka()
else:
    pyinstaller()

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

print("Running NSIS")
subprocess.check_call([args.nsis_path, template_name])

