# -*- mode: python ; coding: utf-8 -*-
import json
import os

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
PRODUCT = META['product']

import sdl2dll
sdl2dll_path = sdl2dll.get_dllpath()

a = Analysis(
    ['..\\scripts\\pytemplate_sdl2'],
    pathex=[
        os.path.join(PROJECT_ROOT, 'src',),
    ],
    binaries=[
        (f'{sdl2dll_path}\\*.dll', '.'),
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
    icon='..\\files\\icons\\pytemplate.ico',
    name=f'{PRODUCT}_sdl2',
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
