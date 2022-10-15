# -*- mode: python ; coding: utf-8 -*-

import importlib
import os
import pkgutil


block_cipher = None

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(SPECPATH),
        '..',
    )
)

def recurse_modules(
    root_name: str='pytemplate_cli.cmd',
):
    yield root_name
    root_mod = importlib.import_module(root_name)
    for sub_info in pkgutil.iter_modules(root_mod.__path__):
        sub_name = '.'.join((root_name, sub_info.name))
        yield sub_name
        sub_mod = importlib.import_module(sub_name)
        if sub_info.ispkg:
            for mod_name in recurse_modules(sub_name):
                yield mod_name

CMD_MODULES = list(recurse_modules())

a = Analysis(
    ['..\\scripts\\pytemplate_cli'],
    pathex=[
        os.path.join(PROJECT_ROOT, 'src',),
    ],
    binaries=[
    ],
    datas=[
    ],
    hiddenimports=[] + CMD_MODULES,
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
    name='pytemplate_cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    icon='..\\files\\icons\\pytemplate.ico',
    entitlements_file=None,
)
