#!/usr/bin/env python3

from typing import Optional
import argparse
from glob import glob
import json
import os
from platform import platform
from shutil import move as mv, rmtree
import subprocess
import sys


COMMIT_MSG = """\
Initial commit

Fork {remote} into {name}

python-template commit hash forked from: {commit_hash}
tools/fork.py command used: {argv}
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

DESCRIPTION = """\
Forks the project into a new project, renaming to the new name and choosing
which features, user interfaces and packaging to include using the command line
options.  Note that fork.py can only be run one time, after which it will
delete itself.
"""

FILES_TO_UPDATE = [
    '.circleci/config.yml',
    "appimage/*/*",
    "debian/control",
    "LICENSE",
    "tools/rpm.spec",
    "setup.py",
    'README.md',
    'files/linux/systemd.service',
    'meta.json',
    'windows/nsis.jinja',
]

def rm(*paths):
    for path in paths:
        _glob = glob(path)
        for _path in _glob:
            if not os.path.exists(_path):
                print(f'WARNING: "{_path}" does not exist')
            elif os.path.isdir(_path):
                rmtree(_path)
            elif os.path.isfile(_path):
                os.remove(_path)
            elif os.path.islink(_path):
                os.unlink(_path)
            else:
                raise OSError(_path)

def _(x):
    """ Run a shell command """
    print(x)
    retcode = os.system(x)
    assert not retcode, retcode


def parse_args():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
    )
    parser.add_argument(
        'org',
        help=(
            'The organization name that owns the project.  You may want '
            'to make this the same as your Github org, open source project, '
            'company, etc...'
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
    parser.add_argument(
        'display_name',
        help=(
            'The display name for the project.  If @name is "python-template" '
            'then display name might be "Python Template"'
        ),
    )

    features = parser.add_argument_group('Features')
    cicd = parser.add_argument_group('CI/CD')
    pymodules = parser.add_argument_group('Python Modules')
    packaging = parser.add_argument_group('Packaging Formats and Platforms')
    services = parser.add_argument_group('Services')

    features.add_argument(
        '--git-origin',
        dest='git_origin',
        default=None,
        help=(
            'The URL of the git origin to add to the new repository.  '
            'Create one in Github, Gitlab, Codeberg, etc... before running '
            'this command'
        ),
    )
    features.add_argument(
        '--no-git-repo',
        action='store_false',
        dest='git_repo',
        default=True,
        help=(
            'Do not create a git repo.  Useful when creating instances '
            'inside a mono-repo.  Mutually exclusive with --keep-git-history.'
        ),
    )
    features.add_argument(
        '--keep-git-history',
        action='store_true',
        dest='git_history',
        default=False,
        help=(
            'Retain git history from the python-template repo.  Useful if '
            'you may want to try to rebase against python-template later '
            'for updates.  Not recommended, as no efforts will be made to '
            'preserve backwards or forward compatibility.  Mutually '
            'exclusvie with --no-git-repo'
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
    features.add_argument(
        '--no-os-module',
        action='store_false',
        dest='os_module',
        default=True,
        help=(
            'Do not include the OS module in the shared library for '
            'detecting the current operating system and adding OS-specific '
            'quirks.'
        ),
    )

    cicd.add_argument(
        '--circle-ci',
        '-C',
        dest='circle_ci',
        action='store_true',
        default=False,
        help='Include a CircleCI config',
    )
    cicd.add_argument(
        '--travis-ci',
        '-T',
        dest='travis_ci',
        action='store_true',
        default=False,
        help='Include a TravisCI config',
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
        '--qt',
        '-q',
        action='store_true',
        dest='qt',
        default=False,
        help='Include a Qt UI',
    )
    pymodules.add_argument(
        '--rest-api',
        '-R',
        action='store_true',
        dest='rest',
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
        '--appimage',
        '-a',
        action='store_true',
        dest='appimage',
        default=False,
        help=(
            'Include AppImage packaging for Linux.  Only valid if '
            'including a CLI, Qt and/or SDL2 interface.'
        ),
    )
    packaging.add_argument(
        '--docker',
        '-D',
        action='store_true',
        dest='docker',
        default=False,
        help=(
            'Include Docker packaging.  Only valid if including a '
            'REST or CLI interface.'
        ),
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
        help=(
            'Include Apple(tm) MacOS(tm) packaging.  Only valid if including '
            'a Qt and/or SDL interface.'
        ),
    )
    packaging.add_argument(
        '--windows',
        '-w',
        action='store_true',
        dest='windows',
        default=False,
        help=(
            'Include Microsoft(tm) Windows(tm) packaging.  Only valid if '
            'including a Qt, SDL and/or CLI interface.'
        ),
    )
    packaging.add_argument(
        '--vendor',
        '-v',
        action='store_true',
        dest='vendor',
        default=False,
        help='Include tools for vendoring packages from pip',
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
        help=(
            'Include a systemd service file.  Only valid if using '
            'RPM and/or Debian packaging'
        ),
    )
    services.add_argument(
        '--win-service',
        '-W',
        action='store_true',
        dest='windows_service',
        default=False,
        help=(
            'Configure as a Windows Service.  Only valid if packaging '
            'for Windows'
        ),
    )

    args = parser.parse_args()
    if not any((
        args.library,
        args.qt,
        args.cli,
        args.rest,
        args.sdl2,
    )):
        parser.error('When you exclude everything, there is nothing of value')

    if args.git_history and not args.git_repo:
        parser.error(
            '--no-git-repo and --keep-git-history are mutually exclusive'
        )
    if not any((args.sdl2, args.qt)):
        if args.macos:
            parser.error(
                'If using --macos, must include one of: --qt, --sdl2'
            )
        if not args.cli:
            if args.appimage:
                parser.error(
                    'If using --appimage, must include one of: '
                    '--cli, --qt, --sdl2'
                )
            if args.windows:
                parser.error(
                    'If using --windows, must include one of: '
                    '--cli, --qt, --sdl2'
                )
    if (
        not any((args.cli, args.rest))
        and
        args.docker
    ):
        parser.error(
            'If using --docker, must include one of: --cli, --rest-api'
        )
    if args.systemd and not (args.deb or args.rpm):
        parser.error('If using --systemd, must include one of: --deb, --rpm')
    if args.windows_service and not args.windows:
        parser.error('If using --win-service, must include --windows')

    org = args.org
    if not org:
        parser.error("Org cannot be empty")
    if len(org) > 20 or len(org) <= 3:
        parser.error(f'{org} must be between 4 and 20 characters')

    name = args.name
    if not name:
        parser.error("Name cannot be empty")
    if not name.islower():
        parser.error(f'{name} contains uppercase letters')
    if not name.replace("_", "").isalnum():
        parser.error(f'{name} is not alpha-numeric')
    if len(name) > 20 or len(name) <= 3:
        parser.error(f'{name} must be between 4 and 20 characters')

    return args

def dir_has_files(dirname: str):
    for dirpath, dirnames, filenames in os.walk(dirname):
        if filenames:
            return True
    return False

def remove_dup_newlines(lines: list):
    result = []
    last_line_empty = False
    for line in lines:
        stripped = line.strip()
        if stripped or not last_line_empty:
            result.append(line)
        last_line_empty = not stripped
    return result

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

def replace_lines(
    path: str,
    contains: str,
    find: str,
    replace: str,
):
    """ Find/replace text, only within lines containing @contains
        @path:     The file to search
        @contains: Only replace text in lines containing this string
        @find:     Text to be replaced
        @replace:  Text to replace @find with
    """
    lines = []
    with open(path) as f:
        for line in f:
            if contains in line:
                line = line.replace(find, replace)
            lines.append(line)
    lines = remove_dup_newlines(lines)
    text = ''.join(lines)
    with open(path, 'w') as f:
        f.write(text)

def remove_lines(
    path: str,
    string: str,
    contains: bool=True,
    strip: bool=False,
):
    """ Remove entire lines containing specific text

        @path:   The path to a file
        @string: The text to match
        @contains:
            True to remove lines containing the string, False to remove lines
            matching the string
        @strip:
            strip the line before comparing, only makes sense
            if @contains=False
    """
    if not os.path.isfile(path):
        print(f'{path} does not exist, not editing')
        return
    with open(path) as f:
        if contains:
            lines = [x for x in f if string not in x]
        elif strip:
            lines = [x for x in f if string != x.strip()]
        elif not strip:
            lines = [x for x in f if string != x]
        else:
            raise Exception("How did we hit this line?")
    lines = remove_dup_newlines(lines)
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

    lines = remove_dup_newlines(lines)
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
                    line.replace(f'{name}', ''),  # Remove calls to target
                )
    lines = remove_dup_newlines(lines)
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
    lines = remove_dup_newlines(lines)
    with open('Makefile', 'w') as f:
        f.write("".join(lines))

def meta_json(args):
    with open('meta.json') as f:
        j = json.load(f)
    j['org'] = args.org
    j['product'] = args.name
    j['display_name'] = {
        k: v.replace('Python Template', args.display_name)
        for k, v in j['display_name'].items()
        if k == 'all' or getattr(args, k)
    }
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
    dirname = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
        ),
    )
    os.chdir(dirname)

    args = parse_args()

    name = args.name

    # Delete Python bytecode files
    _("find . -name '*.pyc' -delete")

    meta_json(args)
    update_shebang(args.shebang)

    if args.sdl2 and not args.qt:
        replace_lines(
            'windows/nsis.jinja',
            'MUI_FINISHPAGE_RUN',
            '_qt',
            '_sdl2',
        )

    # GUI applications
    if any((args.sdl2, args.qt)):
        remove_lines('tools/rpm.spec', 'PT:GUI')
        remove_lines('windows/nsis.jinja', 'PT:GUI')
    else:
        remove_makefile_target('install_linux_icon')
        remove_makefile_target('install_linux_desktop')
        remove_lines(
            'debian/python3-pytemplate.install',
            '/usr/share/pixmaps/',
        )
        remove_lines(
            'debian/python3-pytemplate.install',
            '/usr/share/applications/',
        )
        remove_lines('debian/control', 'desktop-file-utils')
        remove_lines_range('tools/rpm.spec', 'PT:GUI')
        remove_lines_range('windows/nsis.jinja', 'PT:GUI')

    # Applications that have a CLI
    if any((args.cli, args.qt, args.rest, args.sdl2)):
        pass
    else:
        remove_lines('tools/rpm.spec', '_bindir')

    # Applications that require desktop launchers, use icons
    if any((args.sdl2, args.qt, (args.cli and args.windows))):
        mv('files/icons/pytemplate.png', f'files/icons/{name}.png')
        mv(
            'files/icons/pytemplate-systray.png',
            f'files/icons/{name}-systray.png',
        )
        mv('files/icons/pytemplate.ico', f'files/icons/{name}.ico')
        mv('files/icons/pytemplate.icns', f'files/icons/{name}.icns')
        mv(
            'src/pytemplate/files/icons/pytemplate.png',
            f'src/pytemplate/files/icons/{name}.png',
        )
        mv(
            'src/pytemplate/files/icons/pytemplate-systray.png',
            f'src/pytemplate/files/icons/{name}-systray.png',
        )
        mv(
            'src/pytemplate/files/icons/pytemplate.ico',
            f'src/pytemplate/files/icons/{name}.ico',
        )
    else:
        rm('files/icons', 'src/pytemplate/files/icons')

    if args.qt:
        mv('src/pytemplate_qt', f'src/{name}_qt')
        mv('scripts/pytemplate_qt', f'scripts/{name}_qt')
        mv(
            'appimage/qt/pytemplate_qt.appdata.xml',
            f'appimage/qt/{name}_qt.appdata.xml',
        )
        mv(
            'appimage/qt/pytemplate_qt.desktop',
            f'appimage/qt/{name}_qt.desktop',
        )
        remove_lines('tools/rpm.spec', 'PT:QT')
        remove_lines('windows/nsis.jinja', 'PT:QT')
        remove_lines('macos/Distribution.xml', 'PT:QT')
    else:
        rm(
            'src/pytemplate_qt',
            'scripts/pytemplate_qt',
            'windows/*-qt.spec',
            'macos/*-qt.spec',
            'appimage/qt',
            'requirements/qt.txt',
        )
        remove_lines('Makefile', 'UI=qt')
        remove_lines_range('tools/rpm.spec', 'PT:QT')
        remove_lines_range('windows/nsis.jinja', 'PT:QT')
        remove_lines_range('macos/Distribution.xml', 'PT:QT')
        remove_makefile_target('appimage-qt')

    if args.rest:
        mv('src/pytemplate_rest', f'src/{name}_rest')
        mv('test/pytemplate_rest', f'test/{name}_rest')
        mv('scripts/pytemplate_rest', f'scripts/{name}_rest')
    else:
        rm(
            'src/pytemplate_rest',
            'scripts/pytemplate_rest',
            'test/pytemplate_rest',
            'Dockerfile-rest',
            'requirements/rest.txt',
        )
        remove_lines('Makefile', 'src/pytemplate_rest')
        remove_text('setup.cfg', '--cov=pytemplate_rest ')
        remove_lines('requirements/test.txt', 'sanic')
        remove_lines('tox.ini', 'requirements/rest.txt')
        remove_makefile_target('docker-rest')
        replace_makefile_target('type-check', 'pytemplate_rest', '')

    if args.sdl2:
        mv('src/pytemplate_sdl2', f'src/{name}_sdl2')
        mv('scripts/pytemplate_sdl2', f'scripts/{name}_sdl2')
        remove_lines('tools/rpm.spec', 'PT:SDL2')
        remove_lines('windows/nsis.jinja', 'PT:SDL2')
        remove_lines('macos/Distribution.xml', 'PT:SDL2')
        mv(
            'appimage/sdl2/pytemplate_sdl2.appdata.xml',
            f'appimage/sdl2/{name}_sdl2.appdata.xml',
        )
        mv(
            'appimage/sdl2/pytemplate_sdl2.desktop',
            f'appimage/sdl2/{name}_sdl2.desktop',
        )
    else:
        rm(
            'src/pytemplate_sdl2',
            'scripts/pytemplate_sdl2',
            'windows/*sdl2.spec',
            'macos/*sdl2.spec',
            'appimage/sdl2',
            'requirements/sdl2.txt',
        )
        remove_lines('Makefile', 'UI=sdl2')
        remove_lines_range('tools/rpm.spec', 'PT:SDL2')
        remove_lines_range('windows/nsis.jinja', 'PT:SDL2')
        remove_lines_range('macos/Distribution.xml', 'PT:SDL2')
        remove_makefile_target('appimage-sdl2')

    if args.cli:
        mv('scripts/pytemplate_cli', f'scripts/{name}_cli')
        mv('src/pytemplate_cli', f'src/{name}_cli')
        mv('test/pytemplate_cli', f'test/{name}_cli')
        mv(
            'appimage/cli/pytemplate_cli.appdata.xml',
            f'appimage/cli/{name}_cli.appdata.xml',
        )
        mv(
            'appimage/cli/pytemplate_cli.desktop',
            f'appimage/cli/{name}_cli.desktop',
        )
        remove_lines('windows/nsis.jinja', 'PT:CLI')
    else:
        rm(
            'src/pytemplate_cli',
            'test/pytemplate_cli',
            'scripts/pytemplate_cli',
            'Dockerfile-cli',
            'windows/*-cli.spec',
            'appimage/cli/',
            'requirements/cli.txt',
            'files/linux/manpage',
            'files/linux/manpage.md',
        )
        remove_text('setup.cfg', '--cov=pytemplate_cli ')
        remove_makefile_target('appimage-cli')
        remove_makefile_target('docker-cli')
        remove_makefile_target('manpage-from-argparse')
        remove_makefile_target('markdown-from-manpage')
        remove_makefile_target('manpage-from-markdown')
        remove_makefile_target('install_completions')
        remove_makefile_target('install_man_page')
        remove_lines('Makefile', 'src/pytemplate_cli')
        remove_lines('requirements/devel.txt', 'argparse-manpage')
        remove_lines('Makefile', 'COMPLETIONS')
        remove_lines('tox.ini', 'requirements/cli.txt')
        remove_lines_range('tools/rpm.spec', 'PT:CLI')
        remove_lines_range('windows/nsis.jinja', 'PT:CLI')
        replace_makefile_target('type-check', 'pytemplate_cli', '')

    if args.library:
        if not args.os_module:
            rm(
                'src/pytemplate/os.py',
                'test/pytemplate/test_os.py',
            )
        mv('src/pytemplate', f'src/{name}')
        mv('test/pytemplate', f'test/{name}')
    else:
        remove_text('setup.cfg', ' --cov=pytemplate')
        rm('src/pytemplate', 'test/pytemplate')
        replace_makefile_target('type-check', 'pytemplate ', '')

    if args.systemd:
        remove_lines('tools/rpm.spec', 'PT:SYSTEMD')
    else:
        rm('files/linux/systemd.service')
        remove_makefile_target('install_systemd')
        remove_lines_range('tools/rpm.spec', 'PT:SYSTEMD')
        FILES_TO_UPDATE.remove('files/linux/systemd.service')
        remove_lines(
            'debian/python3-pytemplate.install',
            '/usr/lib/systemd/system/',
        )

    if args.windows_service:
        remove_lines('windows/nsis.jinja', 'PT:SERVICE')
    else:
        remove_lines_range('windows/nsis.jinja', 'PT:SERVICE')

    if not args.deb:
        rm('debian')
        remove_lines('.dockerignore', '/debian')
        remove_text('tools/debian_devel_deps.sh', 'devscripts ')
        remove_makefile_target('deb')
        remove_makefile_target('override_dh_auto_build')
        remove_makefile_target('override_dh_auto_install')
        FILES_TO_UPDATE.remove('debian/control')
    if not args.macos:
        rm('macos/', 'tools/*macos*', 'tools/*homebrew*')
        remove_lines('.dockerignore', '/macos')
    if not args.windows:
        rm('windows/', 'tools/*windows*')
        remove_lines('.dockerignore', '/windows')
        FILES_TO_UPDATE.remove('windows/nsis.jinja')
    if args.appimage:
        _(f'for x in appimage/*/; do mv $x/pytemplate.png $x/{name}.png; done')
    else:
        rm('appimage')
        FILES_TO_UPDATE.remove("appimage/*/*")
        remove_makefile_target('appimage-cli')
        remove_makefile_target('appimage-qt')
        remove_makefile_target('appimage-sdl2')
        remove_lines('.dockerignore', '/appimage')
    if not args.docker:
        rm('Dockerfile*', '.dockerignore')
        remove_makefile_target('docker-cli')
        remove_makefile_target('docker-rest')
        remove_lines('Makefile', 'DOCKER_TAG')
    if not args.vendor:
        rm('tools/vendor.sh', 'pytemplate/setup/vendor.py')
        remove_lines('pytemplate/setup/__init__.py', 'vendor')
        remove_makefile_target('install_linux_vendor')

    if not args.rpm:
        rm('tools/rpm.spec')
        remove_makefile_target('rpm')
        FILES_TO_UPDATE.remove('tools/rpm.spec')
        remove_text('tools/fedora_devel_deps.sh', 'rpm-build ')

    if args.pypi:
        remove_lines('setup.py', 'PT:PYPI')
        remove_lines('requirements/devel.txt', 'PT:PYPI')
    else:
        remove_makefile_target('pypi')
        remove_lines_range('setup.py', 'PT:PYPI')
        remove_lines_range('requirements/devel.txt', 'PT:PYPI')

    if not args.travis_ci:
        rm('.travis.yml')

    if not args.circle_ci:
        rm('.circleci')
        FILES_TO_UPDATE.remove('.circleci/config.yml')

    # After the original, to avoid moving the file when others need to write
    if args.deb:
        mv(
            'debian/python3-pytemplate.install',
            f'debian/python3-{name}.install',
        )

    if platform().startswith('macOS'):
        xargs = 'LANG=C xargs sed -i ""'
    else:
        xargs = 'xargs sed -i'
    _(
        "find appimage/ setup.* src/ test/ scripts/ Dockerfile* "
        "macos/ windows/ Makefile tools/ meta.json debian/ "
        "-type f "
        f"| {xargs} 's/pytemplate/{name}/gI'"
    )

    with open('README.md', 'w') as f:
        f.write(f"# {name}\nTODO")
    with open('LICENSE', 'w') as f:
        f.write('Copyright the authors, all rights reserved\nTODO')

    if not any((args.cli, args.qt, args.sdl2, args.vendor, args.systemd)):
        remove_makefile_target('install_linux')

    for dirname in ('files', 'scripts'):
        if not dir_has_files(dirname):
            rm(f'{dirname}/')

    rm('tools/fork.py')

    # Remove empty line continuations
    remove_lines('Makefile', '\\', contains=False, strip=True)

    if args.git_repo:
        if not args.git_history:
            try:
                remote = subprocess.check_output(
                    ['git', 'remote', 'get-url', 'origin'],
                ).decode()
                if remote.startswith('/'):
                    raise Exception('Cloned from local path')
            except Exception as ex:
                remote = "https://github.com/d3v-t00Lz/python-template.git"
                print(f'Unable to determine original git remote: {ex}')
            rm('.git')
            _('git init --initial-branch=main')
            _('git add .')
        commit_msg = COMMIT_MSG.format(
            name=name,
            commit_hash=COMMIT_HASH,
            argv=sys.argv,
            remote=remote,
        )
        _(f'git commit -am "{commit_msg}"')
        if args.git_origin:
            _(f'git remote add origin {args.git_origin}')
            _(f'git push -u origin main')
    else:
        rm('.git')

    success_msg = SUCCESS_MSG
    success_msg += "\n".join(f'    {x}' for x in FILES_TO_UPDATE)
    print(success_msg)

    with open('TODO-fork', 'w') as f:
        f.write(success_msg)

if __name__ == "__main__":
    main()

