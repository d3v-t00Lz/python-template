# -*- mode: python ; coding: utf-8 -*-
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

a = Analysis(
    ['../scripts/pytemplate_qt'],
    pathex=[
        os.path.join(PROJECT_ROOT, 'src',),
    ],
    datas=[
        ('../files/', 'files'),
    ],
    hiddenimports=[
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
    name='pytemplate',
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
    name='pytemplate',
)
app = BUNDLE(
    coll,
    name='pytemplate.app',
    icon='../files/icons/pytemplate.icns',
    bundle_identifier='com.gitlab.pytemplate'
)
