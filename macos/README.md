# Description
This document describes the process for building on Mac OS X.

# Procedure
Note that you will need to install [Homebrew](https://brew.sh/) first, as it
will be used to download dependencies.

### Build and package
```
pip3 -r tools/macos_requirements.txt
tools/homebrew_deps.sh
macos/release.py
# A DMG file will be created in [PROJECT ROOT]/dist/
```

