#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
from glob import glob


CWD = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
    ),
)
os.chdir(CWD)

DIRS = tuple(sorted(x for x in os.listdir() if os.path.isdir(x)))

def parse_args():
    parser = argparse.ArgumentParser('Create AppImages')
    parser.add_argument(
        '-p',
        '--python-version',
        default='3.10',
        dest='pyversion',
        help=(
            'The Python version to use, ie: 3.9, 3.8.  This should probably '
            'be set to the same version as is installed on the system, '
            'otherwise Python.h may be missing when building an AppImage'

        ),
    )
    if len(DIRS) > 1:
        parser.add_argument(
            'dirname',
            choices=DIRS,
            help='The appimage directory to build',
        )
    return parser.parse_args()

args = parse_args()
DIRNAME = args.dirname if len(DIRS) > 1 else DIRS[0]

subprocess.check_call([
    'python-appimage',
    'build',
    'app',
    '--python-version', args.pyversion,
    DIRNAME,
])

if not os.path.isdir('../dist'):
    os.mkdir('../dist')

for appimage in glob('*.AppImage'):
    dest = os.path.join('..', 'dist', appimage)
    if os.path.exists(dest):
        os.remove(dest)
    shutil.move(appimage, '../dist/')

print('Finished!  AppImage files are in [project_root]/dist')

