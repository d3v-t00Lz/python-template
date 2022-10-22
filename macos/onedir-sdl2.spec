# -*- mode: python ; coding: utf-8 -*-
import json
import os
import platform
ARCH = platform.machine()


block_cipher = None

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(SPECPATH),
        '..',
    )
)
#META_FILE = os.path.join(PROJECT_ROOT, 'meta.json')
META_FILE = 'meta.json'
with open(META_FILE) as f:
    META = json.load(f)
DISPLAY_NAME = META['display_name']['sdl2']

a = Analysis(
    ['../scripts/pytemplate_sdl2'],
    pathex=[
        os.path.join(PROJECT_ROOT, 'src',),
    ],
    datas=[
        ('../files/', 'files'),
    ],
    hiddenimports=[
        'pysdl2-dll',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pytemplate_sdl2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pytemplate_sdl2',
)
app = BUNDLE(
    coll,
    name=f'{DISPLAY_NAME}.app',
    icon='../files/icons/pytemplate.icns',
    bundle_identifier='com.gitlab.pytemplate_sdl2'
)
