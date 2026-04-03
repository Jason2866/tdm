# -*- mode: python ; coding: utf-8 -*-

import setuptools_scm
import sys
import platform

arduino_platform_names = {'Darwin'   : {32 : 'i386-apple-darwin',   64 : 'x86_64-apple-darwin'},
                          'DarwinARM': {32 : 'arm64-apple-darwin',  64 : 'arm64-apple-darwin'},
                          'Linux'    : {32 : 'i686-pc-linux-gnu',   64 : 'x86_64-pc-linux-gnu'},
                          'LinuxARM' : {32 : 'arm-linux-gnueabihf', 64 : 'aarch64-linux-gnu'},
                          'Windows'  : {32 : 'i686-mingw32',        64 : 'x86_64-mingw32'}}
bits = 32
if sys.maxsize > 2**32:
    bits = 64
sys_name = platform.system()
sys_platform = platform.platform()
if 'Darwin' in sys_name and (sys_platform.find('arm') > 0 or sys_platform.find('arm64') > 0):
    sys_name = 'DarwinARM'
if 'Linux' in sys_name and (sys_platform.find('arm') > 0 or sys_platform.find('aarch64') > 0):
    sys_name = 'LinuxARM'
if ('CYGWIN_NT' in sys_name) or ('MSYS_NT' in sys_name) or ('MINGW' in sys_name):
    sys_name = 'Windows'

_version = setuptools_scm.get_version(local_scheme='no-local-version')
_suffix = str(sys_name) + str(bits)
filename = "tdmgr"

block_cipher = None

a = Analysis(['tdmgr/run.py'],
             binaries=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# GUI version (no console)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=filename,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='tdmgr.icns')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name=filename)

# Create macOS .app bundle for GUI version
if sys_name in ('Darwin', 'DarwinARM'):
    app = BUNDLE(coll,
                 name='tdmgr.app',
                 icon='tdmgr.icns',
                 bundle_identifier=None)

# Console version (with terminal)
exe_console = EXE(pyz,
                  a.scripts,
                  [],
                  exclude_binaries=True,
                  name=filename + '-console',
                  debug=False,
                  bootloader_ignore_signals=False,
                  strip=False,
                  upx=True,
                  console=True,
                  disable_windowed_traceback=False,
                  target_arch=None,
                  codesign_identity=None,
                  entitlements_file=None,
                  icon='tdmgr.icns')

coll_console = COLLECT(exe_console,
                       a.binaries,
                       a.zipfiles,
                       a.datas,
                       strip=False,
                       upx=True,
                       upx_exclude=[],
                       name=filename + '-console')
