# The Rosetta Stone of Python Packaging

A testing focused, comprehensively packaged, well organized Python3 project
template.  Python2 is not supported, if you are creating new Python2 projects
in the year 2022+, I invite you to rethink what you are doing.

Note that it is impossible to guarantee that a forked repo will immediately
work on any possible target platform, you may need to adjust dependencies based
on what is available in Linux distro repos, vendor certain packages, choose
dependencies that work on your platform, etc...  This repo is only meant to
give customizable, high quality boilerplate configs and structure.  It is up to
you to develop, test and integrate your solutions on every platform you wish to
target.

# Features
- All of the boilerplate in the world
- Clean separation of business logic from presentation
- 100% unit test coverage out of the box
- Clean, well organized and extensible structure
- Advanced packaging for Docker, Windows, MacOS, PyPi/pip,
  RPM (Red Hat/Fedora/OpenSUSE/etc...) and Debian (Debian/Ubuntu/etc...)
- Project forking script to customize which components your project includes
- Generate tab completion scripts for bash and zsh

The `src/pytemplate` module is the base library.  "Interfaces" to the library
are created as additional modules, for example: `src/pytemplate_cli`,
`src/pytemplate_qt`, `src/pytemplate_rest` with corresponding commands in the
`scripts/` directory to invoke each interface

# Usage
See [the documentation folder](doc/)

