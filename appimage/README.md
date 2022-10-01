# AppImage packaging
AppImage provides single-file portable executables on Linux, similar to
app bundles on MacOS.

# Instructions
```
# Dependencies
pip install -r appimage/requirements.txt

# Build
appimage/release.py cli|qt|sdl2

# *.AppImage files are now in dist/
```
