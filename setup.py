#!/usr/bin/env python3
"""

"""

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements


PT_EXCLUDE_LIBS = os.environ.get('PT_EXCLUDE_LIBS', '').strip()
EXCLUDE_LIBS = set(
    x.strip()
    for x in PT_EXCLUDE_LIBS.split(',')
)
print(EXCLUDE_LIBS)

def load_requirements(fname):
    if PT_EXCLUDE_LIBS == 'ALL':
        return []
    reqs = parse_requirements(fname, session="test")
    try:
        result = [
            str(x.requirement)
            for x in reqs
            if str(x.requirement) not in EXCLUDE_LIBS
        ]
    except AttributeError as ex:
        print(f'Assuming older Python version: {ex}')
        result = [
            str(x.req)
            for x in reqs
            if str(x.req) not in EXCLUDE_LIBS
        ]

    print(result)
    return result

NAME = "pytemplate"
URL = 'https://gitlab.com/jaelen/python-template'  # TODO
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
    if 'test' in sys.argv:
        # avoid triggering a pytest coverage report bug
        return 'test'
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


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)

    def run_tests(self):
        #import here, because outside the eggs aren't loaded
        import pytest
        errno = pytest.main()
        sys.exit(errno)

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
	install_requires=load_requirements("requirements.txt"),
    tests_require=[
        'pytest',
        'pytest-cov',
        'sanic_testing<=22.8',
        'types-pyyaml',
    ],
    extras_require={},
    cmdclass={
        'test': PyTest,
    },
    setup_requires=[
        'pytest-runner',
    ],
    scripts=SCRIPTS,
    # PT:PYPI
    # PyPI
    download_url=_gitlab_download_url(),  # TODO
    keywords=[],  # TODO
    # PT:PYPI
)
