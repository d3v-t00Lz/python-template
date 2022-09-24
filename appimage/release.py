#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
from glob import glob

LOCALPATH_MSG = """
Finished.  Now check the files and add to source control:

    git status
    git diff
    git commit -a
    git push
"""

CWD = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
    ),
)
os.chdir(CWD)

DIRS = tuple(sorted(x for x in os.listdir() if os.path.isdir(x)))

def parse_args():
    parser = argparse.ArgumentParser('Create AppImages')
    parser.set_defaults(func=lambda x: print('No subcommand chosen!'))

    subparsers = parser.add_subparsers()
    localrepo_parser = subparsers.add_parser(
        'localrepo',
        help=(
            'Set the AppImages to build from the local reposistory instead '
            'of the remote repository.  You must commit the changes '
            'after this.'
        ),
    )
    localrepo_parser.set_defaults(func=localrepo)

    build_parser = subparsers.add_parser(
        'build',
        help='Build an AppImage',
    )
    build_parser.set_defaults(func=build)
    build_parser.add_argument(
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
        build_parser.add_argument(
            'dirname',
            choices=DIRS,
            help='The appimage directory to build',
        )
    return parser.parse_args()

def localrepo(args):
    localpath = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
        ),
    )
    for path in glob('*/requirements.txt'):
        with open(path, 'w') as f:
            f.write(f'file:{localpath}')
    print(LOCALPATH_MSG)

def build(args):
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

def main():
    args = parse_args()
    func = args.__dict__.pop('func')
    func(args)

if __name__ == '__main__':
    main()

