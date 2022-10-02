#!/usr/bin/env python3
"""

"""

import os
import sys
from setuptools import setup, find_packages

assert sys.version_info > (3, 7), f"Python >= 3.7 required, have {sys.version}"

PT_EXCLUDE_LIBS = os.environ.get('PT_EXCLUDE_LIBS', '').strip()
EXCLUDE_LIBS = set(
    x.strip()
    for x in PT_EXCLUDE_LIBS.split(',')
)
print(EXCLUDE_LIBS)

def load_requirements(*fnames):
    if PT_EXCLUDE_LIBS == 'ALL':
        return []
    result = []
    for fname in fnames:
        with open(fname) as f:
            reqs = [
                x.strip() for x in f
                if (
                    x.strip()
                    and
                    not x.strip().startswith('#')
                )
            ]
        result.extend([
            x for x in reqs
            if x not in EXCLUDE_LIBS
        ])
    print(result)
    return result

NAME = "pytemplate"
URL = 'https://github.com/d3v-t00Lz/python-template'  # TODO
DESCRIPTION = (
    "TODO"
)

SCRIPTS = [
    os.path.join('scripts', x)
    for x in os.listdir(
        os.path.join(
            os.path.dirname(__file__),
            'scripts',
        )
    )
]

def _version():
    path = sys.path[:]
    dirname = os.path.dirname(__file__)
    abspath = os.path.abspath(dirname)
    sys.path.insert(
        0,
        abspath,
    )
    from src import pytemplate
    version = pytemplate.__version__
    sys.path = path
    return version

VERSION = _version()


def _gitlab_download_url(
    name=NAME,
    url=URL,
    version=VERSION,
):
    return "{url}/-/archive/{version}/{name}-{version}.tar.gz".format(
        name=name,
        url=url,
        version=version,
    )


def _github_download_url(
    url=URL,
    version=VERSION,
):
    return "{url}/archive/{version}.tar.gz".format(
        url=url,
        version=version
    )

with open('README.md', 'rt') as f:
    LONG_DESC = f.read()

setup(
    name=NAME,
    version=VERSION,
    author="TODO",
    author_email="TODO",
    license="TODO",
    description=DESCRIPTION,
    long_description=LONG_DESC,
    url=URL,
    packages=find_packages(where='src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    install_requires=load_requirements(
        "requirements/common.txt",
        "requirements/cli.txt",
        "requirements/qt.txt",
        "requirements/rest.txt",
        "requirements/sdl2.txt",
    ),
    extras_require={},
    scripts=SCRIPTS,
    # PT:PYPI
    # PyPI
    download_url=_gitlab_download_url(),  # TODO
    keywords=[],  # TODO
    # PT:PYPI
)
