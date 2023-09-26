# Description
This document describes the process for building on Mac OS X.

# Code Signing
Update all .spec files with your `codesign_identity`.
Update `release.py`, update any TODO items related to code signing

# Procedure
Note that you will need to install [Homebrew](https://brew.sh/) first, as it
will be used to download dependencies.

### Build and package
```
# Install Homebrew first, visit https://brew.sh
macos/homebrew_deps.sh
pip3 install -r macos/requirements.txt
# See macos/release.py --help for options and required arguments
macos/release.py dmg qt
# A DMG file will be created in [PROJECT ROOT]/dist/
macos/release.py pkg
# A PKG file will be created in [PROJECT ROOT]/dist/
```

