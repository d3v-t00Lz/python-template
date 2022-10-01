# The Rosetta Stone of Python Packaging

This project is meant to be forked into new Python3 projects using the
`tools/fork.py` script.  See `tools/fork.py --help` for the many command line
options available.

# Features
- Comprehensive packaging options for all major desktop platforms, easily
  deploy your cross-platform code to nearly any computer in the world
- 100% unit test coverage out of the box
- Clean separation of business logic from presentation
- Well organized and extensible structure
- Generate tab completion scripts for bash and zsh
- `tools/fork.py`: Project forking script to customize which components
  your project includes
- `tools/vendor.sh` Python package vendoring; Transparently store
  dependencies within your own package, useful when packaging for Linux
  distros that do not have all of the required dependencies / versions
  available in the OS package manager
- `Makefile`: Many development and build tasks are automated using the `make`
   command.  See the `Makefile` source code for details.
- Boilerplate configs for popular public cloud CI services

## Advanced packaging
- AppImage (one-file desktop and CLI portable executables that work on nearly
  all Linux distributions)
- Debian (Debian / Ubuntu / etc...)
- Docker
- MacOS app bundle
- pypi / pip
- RPM (Red Hat / Fedora / OpenSUSE / etc...)
- Windows installer

## Included optional user interfaces
- Shared library
- `command subcommand subcommand` CLI with tab completion
- Qt5 and Qt6 UI, flexibly use either in the same codebase using our
  compatibility layer
- SDL2 game
- RESTful API
- ...or build your own

The `src/pytemplate` module is the base library that should contain all of your
application logic.  User interfaces to the library are created as additional
modules, for example: `src/pytemplate_cli`, `src/pytemplate_qt`,
`src/pytemplate_rest` with corresponding commands in the `scripts/` directory
to invoke each interface

# Usage
See [the documentation folder](doc/)

