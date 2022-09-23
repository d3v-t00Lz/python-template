# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(SPECPATH),
        '..',
    )
)

a = Analysis(
    ['..\\scripts\\pytemplate_qt'],
    pathex=[
        os.path.join(PROJECT_ROOT, 'src',),
    ],
    binaries=[
    ],
    datas=[
    ],
    hiddenimports=[],
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
    a.binaries,
    Tree('files', prefix='files\\'),
    a.zipfiles,
    a.datas,
    [],
    name='pytemplate_qt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    icon='..\\files\\icons\\pytemplate.ico',
    entitlements_file=None,
)
