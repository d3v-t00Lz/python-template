#!/usr/bin/env python3

import argparse
import copy
import json
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

META_PATH = os.path.join(CWD, '..', 'meta.json')
with open(META_PATH) as f:
    META = json.load(f)
PRODUCT = META['product']

from pytemplate import __version__ as VERSION

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
            'dirnames',
            choices=DIRS,
            nargs='+',
            help='The appimage directory to build',
        )
    return parser.parse_args()

def build(args):
    if not os.path.isdir('../dist'):
        os.mkdir('../dist')
    dirnames = args.dirnames if len(DIRS) > 1 else DIRS
    current_repo = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
        ),
    )
    env = copy.deepcopy(os.environ)
    env['CURRENT_REPO'] = current_repo
    env['PT_EXCLUDE_LIBS'] = 'ALL'

    for dirname in dirnames:
        print(f'Running python-appimage for {dirname}/')
        subprocess.check_call(
            [
                'python-appimage',
                'build',
                'app',
                '--python-version', args.pyversion,
                dirname,
            ],
            env=env,
        )

    for appimage in glob('*.AppImage'):
        dest = os.path.join('..', 'dist', appimage)
        if os.path.exists(dest):
            print(f'Deleting old version {dest}')
            os.remove(dest)
        print(f'Moving {appimage} to ../dist/')
        shutil.move(appimage, '../dist/')

    os.chdir('../dist')
    if len(dirnames) > 1:
        def _filter(tarinfo):
            tarinfo.mode = int('0755', base=8)
            return tarinfo
        tarpath = f'{PRODUCT}-{VERSION}-x86_64.AppImage.tar.gz'
        if os.path.isfile(tarpath):
            os.remove(tarpath)
        import tarfile
        with tarfile.open(tarpath, 'w:gz') as f:
            for appimage in glob('*.AppImage'):
                f.add(
                    appimage,
                    arcname=os.path.basename(appimage),
                    filter=_filter,
                )

    print('Finished!  AppImage files are in [project_root]/dist')

def main():
    args = parse_args()
    build(args)

if __name__ == '__main__':
    main()

