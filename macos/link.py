#!/usr/bin/env python3

import argparse
import collections
import copy
import glob
import os
import shutil
import subprocess

DESC = """\
Recursively re-link executables and libraries

MacOS app bundles that contain binary executables and libraries must
have their linkage changed from system paths to relative paths.  This
script will recursively copy and relink all required binaries to an
app bundle.  You must keep the dylibs and executables in the same
directory
"""

def parse_args():
    parser = argparse.ArgumentParser(DESC)
    parser.add_argument(
        'binaries',
        nargs='+',
        help='One or more binaries to relink'
    )
    parser.add_argument(
        '--outdir',
        '-o',
        default='.',
        dest='outdir',
        help='The directory to output relinked executables and libraries to'
    )
    return parser.parse_args()

args = parse_args()
os.chdir(args.outdir)

def relink(binary):
    otool = subprocess.check_output([
        'otool',
        '-L',
        binary,
    ]).decode('utf-8')
    for line in otool.split('\n'):
        arr = line.split()
        if not arr:
            continue
        dylib = arr[0]
        if dylib.endswith('.dylib') and (
            dylib.startswith('/usr/local/')
            or
            dylib.startswith('/opt/homebrew/')
        ):
            basename = os.path.basename(dylib)
            print(
                f'Relinking {binary} -> {basename}',
            )
            subprocess.check_output([
                'install_name_tool',
                '-change',
                dylib,
                f'@loader_path/{basename}',
                binary,
            ])

            if not os.path.exists(basename):
                shutil.copyfile(dylib, basename)
                relink(basename)

for binary in args.binaries:
    assert os.path.exists(binary), binary
    relink(binary)

