#!/usr/bin/env python3

from typing import Optional
import argparse
import json
import os
import subprocess
import sys


COMMIT_MSG = """\
Initial commit

Fork github.com/d3v-t00Lz/python-template into {name}
Source commit hash: {commit_hash}
fork.py args: {argv}
"""

COMMIT_HASH = subprocess.check_output(
    ['git', 'rev-parse', '--short', 'HEAD'],
).decode().strip()

SUCCESS_MSG = """
Successfully forked.

Add a new remote origin with:
    git remote add origin $GIT_CLONE_URL

Please update the following files as needed and replace any TODO items:
"""

FILES_TO_UPDATE = [
    "DEBIAN/control",
    "LICENSE",
    "rpm.spec",
    "setup.py",
    'README.md',
    'files/linux/systemd.service',
    'meta.json',
    'windows/nsis.jinja',
]


def _(x):
    """ Run a shell command """
    print(x)
    retcode = os.system(x)
    assert not retcode, retcode


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Forks the project into a new project, renaming to the new name "
            "and if desired, removing unused components using the command "
            "line options"
        )
    )
    parser.add_argument(
        'org',
        help=(
            'The organization name that owns the project.  You may want '
            'to make this the same as your Github org, or etc...'
        ),
    )
    parser.add_argument(
        'name',
        help=(
            'The new project name. Must be lowercase and alphanumeric '
            'only.  Underscores (_) are allowed, but generally '
            'discouraged.  A good name will be ~4-12 characters'
        ),
    )

    features = parser.add_argument_group('Features')
    pymodules = parser.add_argument_group('Python Modules')
    packaging = parser.add_argument_group('Packaging Formats and Platforms')
    services = parser.add_argument_group('Services')

    features.add_argument(
        '--no-git-repo',
        action='store_false',
        dest='git_repo',
        default=True,
        help=(
            'Do not create a git repo.  Useful when creating instances '
            'inside a mono-repo'
        ),
    )
    features.add_argument(
        '--shebang',
        dest='shebang',
        default=None,
        help=(
            'Specify an alternate shebang lines for files in scripts/ .  '
            'Used to run with an alternate interpreter to standard CPython3.'
            '  For example:  --shebang="#!/usr/bin/env pypy3"'
        ),
    )

    pymodules.add_argument(
        '--no-library',
        '-L',
        action='store_false',
        dest='library',
        default=True,
        help='Do not include the shared library (not recommended)',
    )
    pymodules.add_argument(
        '--cli',
        '-c',
        action='store_true',
        dest='cli',
        default=False,
        help='Include a command line interface (CLI) utility',
    )
    pymodules.add_argument(
        '--qt-ui',
        '-q',
        action='store_true',
        dest='qt_ui',
        default=False,
        help='Include a Qt UI',
    )
    pymodules.add_argument(
        '--rest-api',
        '-R',
        action='store_true',
        dest='rest_api',
        default=False,
        help='Include a REST API',
    )
    pymodules.add_argument(
        '--sdl2',
        '-s',
        action='store_true',
        dest='sdl2',
        default=False,
        help='Include an SDL2 UI',
    )

    packaging.add_argument(
        '--docker',
        '-D',
        action='store_true',
        dest='docker',
        default=False,
        help='Include Docker packaging',
    )
    packaging.add_argument(
        '--deb',
        '-d',
        action='store_true',
        dest='deb',
        default=False,
        help='Include Debian packaging',
    )
    packaging.add_argument(
        '--rpm',
        '-r',
        action='store_true',
        dest='rpm',
        default=False,
        help='Include RPM packaging',
    )
    packaging.add_argument(
        '--macos',
        '-m',
        action='store_true',
        dest='macos',
        default=False,
        help='Include Apple(tm) MacOS(tm) packaging',
    )
    packaging.add_argument(
        '--windows',
        '-w',
        action='store_true',
        dest='windows',
        default=False,
        help='Include Microsoft(tm) Windows(tm) packaging',
    )
    packaging.add_argument(
        '--vendor',
        '-v',
        action='store_true',
        dest='vendor',
        default=False,
        help='Include vendored packages from pip',
    )
    packaging.add_argument(
        '--pypi',
        '-P',
        action='store_true',
        dest='pypi',
        default=False,
        help='Include tools to upload to PyPi',
    )

    services.add_argument(
        '--systemd',
        '-S',
        action='store_true',
        dest='systemd',
        default=False,
        help='Include a systemd service file',
    )
    services.add_argument(
        '--win-service',
        '-W',
        action='store_true',
        dest='windows_service',
        default=False,
        help='Configure as a Windows Service',
    )

    args = parser.parse_args()
    if not any((
        args.library,
        args.qt_ui,
        args.cli,
        args.rest_api,
        args.sdl2,
    )):
        print('Error: When you exclude everything, there is nothing of value')
        exit(1)
    if not any((args.sdl2, args.qt_ui)):
        args.macos = False
        if not args.cli:
            args.windows = False
    return args

def remove_text(path: str, string: str):
    """ Remove specific text from a file  """
    if not os.path.isfile(path):
        print(f'{path} does not exist, not editing')
        return
    with open(path) as f:
        text = f.read()
    text = text.replace(string, '')
    with open(path, 'w') as f:
        f.write(text)

def remove_lines(path: str, string: str):
    """ Remove entire lines containing specific text """
    if not os.path.isfile(path):
        print(f'{path} does not exist, not editing')
        return
    with open(path) as f:
        lines = [x for x in f if string not in x]
    with open(path, 'w') as f:
        f.write("".join(lines))

def remove_lines_range(
    path: str,
    start: str,
    end: Optional[str]=None,
):
    """ Remove entire ranges of lines containing specific text

        @path:  The path to the file
        @start: The text to be present in the first line to delete
        @end:   The text in the last line to delete, or None to use start as
                the text to end with
    """
    if not os.path.isfile(path):
        print(f'{path} does not exist, not editing')
        return
    deleting = False
    lines = []
    with open(path) as f:
        if end is None:
            end = start
        for line in f:
            if deleting:
                if end in line:
                    deleting = False
            else:
                if start in line:
                    deleting = True
                else:
                    lines.append(line)

    with open(path, 'w') as f:
        f.write("".join(lines))

def remove_makefile_target(name: str):
    lines = []
    deleting = False
    with open('Makefile') as f:
        for line in f:
            if not deleting and line.startswith(f"{name}:"):
                deleting = True
                continue
            if deleting and not line.startswith("\t"):
                deleting = False
            if not deleting:
                lines.append(
                    line.replace(f' {name}', ''),  # Remove calls to target
                )
    with open('Makefile', 'w') as f:
        f.write("".join(lines))

def replace_makefile_target(name: str, old: str, new: str):
    """ Replace text within a Makefile target """
    lines = []
    replacing = False
    with open('Makefile') as f:
        for line in f:
            if not replacing and line.startswith(f"{name}:"):
                replacing = True
            elif replacing and not line.startswith("\t"):
                replacing = False

            if replacing:
                lines.append(line.replace(old, new))
            else:
                lines.append(line)
    with open('Makefile', 'w') as f:
        f.write("".join(lines))

def meta_json(org, name):
    with open('meta.json') as f:
        j = json.load(f)
    j['org'] = org
    j['product'] = name
    with open('meta.json', 'w') as f:
        json.dump(j, f, sort_keys=True, indent=4)

def update_shebang(shebang: Optional[str]):
    if shebang is None:
        return
    assert shebang.startswith("#!")
    shebang += "\n"
    for fname in os.listdir('scripts'):
        path = os.path.join('scripts', fname)
        with open(path) as f:
            lines = list(f)
        assert(lines[0].startswith("#!")), (path, lines[0])
        lines[0] = shebang
        with open(path, 'w') as f:
            f.write(''.join(lines))

def main():
    file_path = os.path.abspath(__file__)
    dirname = os.path.dirname(file_path)
    os.chdir(dirname)

    args = parse_args()

    name = args.name
    assert name
    assert name.islower(), name
    assert name.replace("_", "").isalnum(), name
    assert len(name) < 20, len(name)

    # Delete Python bytecode files
    _("find . -name '*.pyc' -delete")

    meta_json(args.org, args.name)
    update_shebang(args.shebang)

    if any((args.sdl2, args.qt_ui, (args.cli and args.windows))):
        _(f'mv files/icons/pytemplate.png files/icons/{name}.png')
        _(f'mv files/icons/pytemplate.ico files/icons/{name}.ico')
    else:
        _('rm -rf files/icons')
        remove_makefile_target('install_linux_icon')

    if args.qt_ui:
        _(f'mv src/pytemplate_qt src/{name}_qt')
        _(f'mv scripts/pytemplate_qt scripts/{name}_qt')
        remove_lines('rpm.spec', 'PT:GUI')
    else:
        _('rm -rf src/pytemplate_qt scripts/pytemplate_qt')
        _('rm -rf windows/*-qt.spec macos/*-qt.spec')
        remove_lines('requirements.txt', 'PyQt')
        remove_lines_range('rpm.spec', 'PT:GUI')

    if args.rest_api:
        _('mv src/pytemplate_rest src/{}_rest'.format(name))
        _('mv test/pytemplate_rest test/{}_rest'.format(name))
        _('mv scripts/pytemplate_rest scripts/{}_rest'.format(name))
    else:
        _('rm -rf src/pytemplate_rest scripts/pytemplate_rest')
        _('rm -rf test/pytemplate_rest')
        _('rm -f Dockerfile-rest')
        remove_text('setup.cfg', '--cov=pytemplate_rest ')
        remove_lines('requirements.txt', 'sanic')
        remove_makefile_target('docker-rest')
        replace_makefile_target('type-check', 'pytemplate_rest', '')

    if args.sdl2:
        _('mv src/pytemplate_sdl2 src/{}_sdl2'.format(name))
        _('mv scripts/pytemplate_sdl2 scripts/{}_sdl2'.format(name))
    else:
        _('rm -rf pytemplate_sdl2 scripts/pytemplate_sdl2')
        _('rm -rf windows/*sdl2.spec macos/*sdl2.spec')
        remove_lines('requirements.txt', 'PySDL2')
        remove_lines('requirements.txt', 'sdl2')

    if args.cli:
        _('mv scripts/pytemplate_cli scripts/{}_cli'.format(name))
        _('mv src/pytemplate_cli src/{}_cli'.format(name))
        _('mv test/pytemplate_cli test/{}_cli'.format(name))
    else:
        _('rm -rf src/pytemplate_cli test/pytemplate_cli scripts/pytemplate')
        _('rm -f Dockerfile-cli')
        _('rm -f windows/*-cli.spec')
        remove_text('setup.cfg', '--cov=pytemplate_cli ')
        remove_makefile_target('docker-cli')
        remove_makefile_target('install_completions')
        remove_lines('Makefile', 'COMPLETIONS')
        remove_lines_range('rpm.spec', 'PT:CLI')
        remove_lines('requirements.txt', 'shtab')
        replace_makefile_target('type-check', 'pytemplate_cli', '')

    if args.library:
        _('mv src/pytemplate src/{}'.format(name))
        _('mv test/pytemplate test/{}'.format(name))
    else:
        remove_text('setup.cfg', ' --cov=pytemplate')
        _('rm -rf src/pytemplate test/pytemplate')
        replace_makefile_target('type-check', 'pytemplate ', '')

    if args.systemd:
        remove_lines('rpm.spec', 'PT:SYSTEMD')
    else:
        _('rm -f files/linux/systemd.service')
        remove_makefile_target('install_systemd')
        remove_lines_range('rpm.spec', 'PT:SYSTEMD')
        FILES_TO_UPDATE.remove('files/linux/systemd.service')

    if args.windows_service:
        remove_lines('windows/nsis.jinja', 'PT:WINDOWS_SERVICE')
    else:
        remove_lines_range('windows/nsis.jinja', 'PT:WINDOWS_SERVICE')

    if not args.deb:
        _('rm -rf DEBIAN/')
        remove_makefile_target('deb')
        FILES_TO_UPDATE.remove('DEBIAN/control')
    if not args.macos:
        _('rm -rf macos/')
    if not args.windows:
        _('rm -rf windows/')
        FILES_TO_UPDATE.remove('windows/nsis.jinja')
    if not args.docker:
        _('rm -f Dockerfile*')
        remove_makefile_target('docker-cli')
        remove_makefile_target('docker-rest')
    if not args.vendor:
        _('rm -f vendor.sh pytemplate/setup/vendor.py')
        remove_lines('pytemplate/setup/__init__.py', 'vendor')
        remove_makefile_target('install_linux_vendor')

    if not args.rpm:
        _('rm -f rpm.spec')
        remove_makefile_target('rpm')
        FILES_TO_UPDATE.remove('rpm.spec')
    if args.pypi:
        remove_lines('setup.py', 'PT:PYPI')
    else:
        remove_makefile_target('pypi')
        remove_lines_range('setup.py', 'PT:PYPI')

    _(
        "find setup.* fork.py src/ test/ scripts/ Dockerfile* "
        "macos/ windows/ Makefile rpm.spec meta.json DEBIAN/ "
        "-type f "
        "| xargs sed -i 's/pytemplate/{name}/gI'".format(name=name)
    )

    with open('README.md', 'w') as f:
        f.write(f"# {name}\nTODO")

    _('rm -rf .git')

    if args.git_repo:
        _('git init .')
        _('git add .')
        commit_msg = COMMIT_MSG.format(
            name=name,
            commit_hash=COMMIT_HASH,
            argv=sys.argv,
        )
        _(f'git commit -am "{commit_msg}"')

    SUCCESS_MSG += "\n".join(f'    {x}' for x in FILES_TO_UPDATE)
    print(SUCCESS_MSG)

    with open('TODO-fork', 'w') as f:
        f.write(SUCCESS_MSG)

if __name__ == "__main__":
    main()

