# The Rosetta Stone of Python Packaging

A testing focused, comprehensively packaged, well organized Python3 project
template.  Python2 is not supported, if you are creating new Python2 projects
in the year 2022+, I invite you to rethink what you are doing.

Note that it is impossible to guarantee that a forked repo will immediately
work on any possible target platform, you may need to adjust dependencies based
on what is available in Linux distro repos, vendor certain repos, choose
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

The `pytemplate` module is the base library.  "Interfaces" to the library
are created as additional modules, for example: `pytemplate_cli`,
`pytemplate_qt`, `pytemplate_rest` with corresponding commands in the
`scripts/` directory to invoke each interface

# How to use
## Forking
Forking is how you create a new repository from this template.  It will
rename everything to the new project name, and optionally remove components
that are not needed.

Run `./fork.py $NEW_NAME`.  See `./fork.py --help` for many different options
to customize the new repository.

## Additional tooling
See the `Makefile` for additional tooling that can be used.  `fork.py` will
remove unused Makefile targets depending on the options that were chosen,
so this may vary by repo.

## Creating a new release
Update `${PROJECT_NAME}/__init__.py:__version__`, commit and then tag a new
release with that version.  Package as required.

## How to run the unit tests
```
make test
# to open the coverage report:
firefox htmlcov/index.html
```

## Vendoring Dependencies
Adds vendored dependencies to the shared library, storing packages from
pip locally in the project, instead of installing to the system or venv.

Generally, this is considered a bad practice as it increases
the maintenance burden of enforcing security updates, but
has the advantages of creating stability, and making testing updates
more explicit (no surprises in production because a package was updated
on a host or container image without warning).

Packages go into pytemplate/vendor/ and can be imported from there
```
./vendor.sh package-name-1 package-name-2
```

# Packaging
## Docker
```
# Build the desired image
make docker-cli
make docker-rest
# Or
ORG=my-docker-registry.something.org make docker-cli

# Upload to your registry
# (requires that you first tag the image appropriately for the Docker registry)
docker push $DOCKER_TAG

# Run locally, the Dockerfile is designed to take arguments as a CLI,
# change the Dockerfile as needed for your use-case
docker run someorg/pytemplate-cli version
```

## Windows
From a Windows computer:
```
# First read windows/README.md for instructions on how to install dependencies

# Create a single file .exe
# Or use any other spec
pyinstaller windows/onefile-qt.spec

# Create an installer
python windows/release.py
```

## MacOS
From a MacOS computer:
```
# Install depdencies, first time only
./macos/homebrew_deps.sh

# Create an app bundle packaged in a DMG for MacOS
python3 macos/release.py
```

## Linux
### RPM distros (Red Hat, CentOS, Fedora, Rocky, Alma, etc...)
```
# Remember to edit rpm.spec to include the correct information and dependencies
make rpm
```

### DEB distros (Debian, Ubuntu, etc...)
```
# Remember to edit DEBIAN/control to include the correct information
# and dependencies
make deb
```

### pypi / pip
```
# Upload your package to PyPi so that anybody can install using pip.
#
# NOTE: This means the entire public internet.  Do not enable the pypi
#       option in fork.py for private/proprietary Python packages.
#
# Requires `twine` to be installed, and a local twine config with your
# pypi username and password
make pypi
```

