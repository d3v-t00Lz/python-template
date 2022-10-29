# -*- mode: python ; coding: utf-8 -*-
import json
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
#META_FILE = os.path.join(PROJECT_ROOT, 'meta.json')
META_FILE = 'meta.json'
with open(META_FILE) as f:
    META = json.load(f)
PRODUCT = META['product']

def recurse_modules(
    root_name: str='pytemplate_cli.cmd',
):
    """ Recursively list submodules of @root_name
        Necessary because of the machinery used to implement subcommands,
        importlib.import_module is not seen by pyinstaller, therefore
        we need to enumerate the submodules here.
    """
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
        ('../files/', 'files'),
    ],
    hiddenimports=[
    ] + CMD_MODULES,
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
    name=f'{PRODUCT}_cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='pytemplate_cli',
)
