# -*- mode: python ; coding: utf-8 -*-

# 导入 PyInstaller 中的 Analysis 类，用于分析 Python 脚本及其依赖项
from PyInstaller.building.build_main import Analysis
# 导入 PyInstaller 中的 PYZ 类，用于将纯 Python 代码压缩成一个 PYZ 文件
from PyInstaller.building.api import PYZ
# 导入 PyInstaller 中的 EXE 类，用于创建可执行文件
from PyInstaller.building.api import EXE

from PyInstaller.archive.pyz_crypto import PyiBlockCipher

import base64, os

# 创建一个 Analysis 对象，用于分析要打包的 Python 脚本及其依赖项
a = Analysis(
    # 要打包的 Python 脚本列表，这里指定为 'Termination4.py'
    ['Termination4.py'],
    # 搜索模块的路径列表，这里为空，表示使用默认路径
    pathex=[],
    # 要包含的二进制文件列表，这里为空
    binaries=[],
    # 要包含的数据文件列表，格式为 (源文件路径, 目标路径)
    # 这里将 '.\\tools\\tools.dll' 文件复制到打包后的根目录
    datas=[
           ('C:\\Windows\\System32\\ucrtbase.dll', '.'),
           ('.\\ocr\\', '.\\ocr\\'),
           ('.\\TConfig\\version.ini', '.\\TConfig\\'),
           ('.\\TConfig\\EXEConfig.bin', '.\\TConfig\\'),
           ('.\\static\\', '.\\static\\'),
           ('.\\TLUI\\InspirationSong.mid', '.\\static\\'),
           ('.\\.inf\\.bin\\', '.\\PEBinary\\'),
           ('.\\.inf\\.lib\\', '.\\PELibrary\\'),
           ('.\\T2SRFB\\win\\T2SRFB\\T2SRFB4.exe', '.\\PEBinary\\'),
          ],
    # 隐藏导入的模块列表，这些模块不会被自动检测到，需要手动指定
    hiddenimports=[],
    # 钩子文件所在的路径列表，这里为空
    hookspath=[],
    # 钩子配置字典，这里为空
    hooksconfig={},
    # 运行时钩子列表，这里为空
    runtime_hooks=[],
    # 要排除的模块列表，这里为空
    excludes=[],
    # 是否不将文件打包成一个归档文件，设置为 True 表示不打包成归档文件
    noarchive=True,
    # 优化级别，2 表示最高级别的优化
    optimize=2,
    # 排除系统库
    exclude_system_libraries=True,
    #cipher=PyiBlockCipher(key=base64.b64encode(os.urandom(16)).decode('utf-8'))
)

# 创建一个 PYZ 对象，将 Analysis 对象中分析出的纯 Python 代码压缩成一个 PYZ 文件
pyz = PYZ(a.pure)

# 创建一个 EXE 对象，用于生成可执行文件
exe = EXE(
    # 包含纯 Python 代码的 PYZ 对象
    pyz,
    # Analysis 对象中分析出的脚本文件列表
    a.scripts,
    # Analysis 对象中分析出的二进制文件列表
    a.binaries,
    # Analysis 对象中指定的数据文件列表
    a.datas,
    # 要添加到可执行文件中的额外资源列表，这里为空
    [],
    # 生成的可执行文件的名称
    name='Termination4',
    # 是否开启调试模式，设置为 False 表示不开启
    debug=False,
    # 引导加载程序是否忽略信号，设置为 False 表示不忽略
    bootloader_ignore_signals=False,
    # 是否对可执行文件进行 strip 操作，去除不必要的符号信息
    strip=False,
    # 是否使用 UPX 进行压缩，设置为 False 表示不使用
    upx=True,
    upx_level=9,
    # 不使用 UPX 压缩的文件列表，这里为空
    upx_exclude=["libssl-3.dll"],
    # 运行时临时目录，这里设置为 None 表示使用默认临时目录
    runtime_tmpdir=None,
    # 是否以控制台模式运行可执行文件，设置为 False 表示不显示控制台窗口
    console=False,
    # 是否禁用窗口化的错误回溯，设置为 False 表示不禁用
    disable_windowed_traceback=False,
    # 是否模拟命令行参数，设置为 False 表示不模拟
    argv_emulation=False,
    # 目标架构，这里设置为 None 表示使用默认架构
    target_arch=None,
    # 代码签名标识，这里设置为 None 表示不进行代码签名
    codesign_identity=None,
    # 权限文件，这里设置为 None 表示不使用权限文件
    entitlements_file=None,
    #图标
    icon="./Art/icon.ico",
    # manifest
    manifest="./.tmp/App.manifest",
    # 资源文件
    win_resources=[('./.tmp/App.rc', 1)],
)