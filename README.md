# The Rosetta Stone of Python Packaging

This project is meant to be forked into new Python3 projects using the
`tools/fork.py` script.  See `tools/fork.py --help` for the many command line
options available.

Note that it is impossible to guarantee that a forked repo will immediately
work on any possible target platform, you may need to adjust dependencies based
on what is available in Linux distro repos, vendor certain packages, choose
dependencies that work on your platform, etc...  This repo is only meant to
give customizable, high quality boilerplate configs and structure.  It is up to
you to develop, test and integrate your solutions on every platform you wish to
target.

# Features
- 100% unit test coverage out of the box
- All of the boilerplate in the world
- Clean separation of business logic from presentation
- Clean, well organized and extensible structure
- `tools/fork.py`: Project forking script to customize which components
  your project includes
- Generate tab completion scripts for bash and zsh
- Advanced packaging for
  - AppImage (portable container images for all Linux distributions)
  - Debian (Debian / Ubuntu / etc...)
  - Docker
  - MacOS
  - pypi / pip
  - RPM (Red Hat / Fedora / OpenSUSE / etc...)
  - Windows

The `src/pytemplate` module is the base library.  "Interfaces" to the library
are created as additional modules, for example: `src/pytemplate_cli`,
`src/pytemplate_qt`, `src/pytemplate_rest` with corresponding commands in the
`scripts/` directory to invoke each interface

# Usage
See [the documentation folder](doc/)

