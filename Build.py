#-*-coding:utf-8 -*-
import PyInstaller.__main__
import os

filename = input("请输入文件名字")
if not filename.endswith('.py'):
    filename += '.py'


package_name = filename.split('.py')[0]

PyInstaller.__main__.run(
    [
        '--name=%s' % package_name,
        '--onefile',
        '--hidden-import=NodeGraphQt.vendor.Qt',
        #'--windowed',
        #'--add-binary=%s' % os.path.join('resource', 'path', '*.png'),
        #'--add-data=%s' % os.path.join('resource', 'path', '*.txt'),
        #'--icon=%s' % os.path.join('resource', 'path', 'icon.ico'),
        os.path.join('', filename),
    ]
)