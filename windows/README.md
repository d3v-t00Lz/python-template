# Overview
This is the procedure for creating the Windows portable executable and
installer.

The following components must be setup and configured prior to building:
- Python
- NSIS

The build steps proceed as follows:
- Pull the source code
- Run pyinstaller to create the portable executable or directory
- Run NSIS to create the Windows installer

# Initial Setup
## Create a fresh 64 bit Windows 10 VM
(or install Windows to your hard drive if you are `into that`).
The VM should have at least 100GB of hard disk space

- Install [Python3 64bit](https://www.python.org/downloads/windows/), be sure
  to select the option to add Python to PATH / environment variables
- Install [NSIS](https://nsis.sourceforge.io/Download)
- Install the [EnVar NSIS plugin](https://nsis.sourceforge.io/EnVar_plug-in)
  (note that a version is kept in the /windows/ directory for safe keeping)

## Windows cmd.exe
```
cd %DIRECTORY_OF_GIT_REPO%
python -m venv venv
venv\Scripts\activate.bat
python -m pip install -r windows/requirements.txt
python -m pip install -e .
```

# Creating a new release
## Windows cmd.exe
```
cd %DIRECTORY_OF_GIT_REPO%
venv\Scripts\activate.bat
# Build the portable exe or installer exe
python windows\release.py [name-of-spec-file]
```

The release artifacts are now in `dist/`

