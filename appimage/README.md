# AppImage packaging
AppImage provides single-file application distribution on Linux.

# Instructions
## Dependencies
```
# Dependencies
pip install -r appimage/requirements.txt

# Set to build from local git repository instead of remote
appimage/release.py localrepo
git diff
git commit -a

# Build
appimage/release.py build cli|qt|sdl2

# *.AppImage files are now in dist/
```
