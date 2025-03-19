# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Agregar las dependencias necesarias en hiddenimports
hidden_imports = [
    'cv2',
    'numpy',
    'pygame',
    'requests',
    'yt_dlp',
]

# Ruta a los archivos de OpenCV (ajusta según tu sistema)
# En Windows, la ruta típica es: C:\PythonXX\Lib\site-packages\cv2
# En Linux/macOS, la ruta típica es: /usr/local/lib/pythonX.X/site-packages/cv2
import cv2
cv2_path = cv2.__file__

# Agregar los archivos de OpenCV a datas
datas = [
    (cv2_path, 'cv2'),  # Incluir la carpeta cv2 completa
]

a = Analysis(
    ['index.py'],
    pathex=[],
    binaries=[],
    datas=datas,  # Incluir los archivos de datos
    hiddenimports=hidden_imports,  # Incluir las dependencias
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='index',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)