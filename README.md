# The Rosetta Stone of Python Packaging

This project is meant to be forked into new Python3 projects using the
`tools/fork.py` script.  See `tools/fork.py --help` for the many command line
options available.

# Features
- 100% unit test coverage out of the box
- All of the boilerplate in the world
- Clean separation of business logic from presentation
- Clean, well organized and extensible structure
- Generate tab completion scripts for bash and zsh
- `tools/fork.py`: Project forking script to customize which components
  your project includes
- `tools/vendor.sh` Python package vendoring; Transparently store
  dependencies within your own package, useful when packaging for Linux
  distros that do not have all of the required dependencies / versions
  available in the OS package manager
- Advanced packaging for
  - AppImage (one-file desktop and CLI portable executables for all
    Linux distributions)
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

