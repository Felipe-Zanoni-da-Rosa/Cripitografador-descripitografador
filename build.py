import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=main',
    '--onefile',
    '--windowed',
    'main.pyw'
])