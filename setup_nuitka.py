# -*- coding: utf-8 -*-
import sys
import os
import platform
import subprocess
import time
import ast


import TLib.T_GodKeys
import TLib.T_Version
import TLib.T_FIO
import TPLib.T_VMDISC.DISCAPI as DISCAPI

class A:
    __static_path__="./"
    @staticmethod
    @property
    def WorkMod():
        return "py"
B=A()
v=TLib.T_Version.Version(B, "./TConfig/version.ini")
g=TLib.T_GodKeys.GodKeys(b"EXMODECONFIGKEYS"*2)
j=ast.literal_eval(TLib.T_FIO.FIO.openr("./TConfig/EXEConfig.dict"))
j["Version"]={"Termination": v.version["Version"], "Compilation": v.version["Compilation"]}
s=b"EXMODECONFIGSTART"+g.encrypt(str(j).encode())+b"EXMODECONFIGEND"
TLib.T_FIO.FIO.openw("./TConfig/EXEConfig.dict", str(j))
TLib.T_FIO.FIO.openw("./TConfig/EXEConfig.bin", s, 2)
TLib.T_FIO.FIO.openw("./.tmp/App.rc", TLib.T_FIO.FIO.openr("./App.rc").replace("%Build_Version", v.version["Compilation"]["Runs"]))
TLib.T_FIO.FIO.openw("./.tmp/App.manifest", TLib.T_FIO.FIO.openr("./App.manifest").replace("%Build_Version", v.version["Compilation"]["Runs"]))

with DISCAPI.DISCFile("./static/Termination.DISC", "w") as df:
    pass




def get_nuitka_options():

    data_files = [
        # ('C:/Windows/System32/ucrtbase.dll', 'ucrtbase.dll'),
        ('./TConfig/version.ini', 'TConfig/version.ini'),
        ('./TConfig/EXEConfig.bin', 'TConfig/EXEConfig.bin'),
        ('./TLUI/InspirationSong.mid', 'static/InspirationSong.mid'),
        ('./TLUI/HA.mp3', 'static/HA.mp3'),
        ('./T2SRFB/win/T2SRFB/T2SRFB4.exe', 'PEBinary/T2SRFB4.exe'),
    ]

    data_options = []
    for src, dest in data_files:
        src=os.path.abspath(src)
        data_options.extend([f'--include-data-file={src}={dest}'])

    data_dirs = [
        ('./ocr/', 'ocr'),
        ('./static/', 'static'),
    ]
    for i in os.listdir("./.inf/.bin"):
        if i.endswith(".exe"):
            data_files.append((f"./.inf/.bin/{i}", f"PEBinary/{i}"))
    for i in os.listdir("./.inf/.lib"):
        if i.endswith(".dll"):
            data_files.append((f"./.inf/.lib/{i}", f"PELibrary/{i}"))


    for src, dest in data_dirs:
        src=os.path.abspath(src)
        data_options.extend([f'--include-data-dir={src}={dest}'])

    # 基础选项
    options = [
        "Termination4.py",
        "--standalone",
        "--onefile",
        "--show-progress",
        "--jobs=32",
        "--mingw64",
        "--follow-imports",
        #"--windows-manifest=./.tmp/App.manifest",
        #"--win-resources=./.tmp/App.rc",
        # "--enable-optimizations",
        "--output-filename=Termination4",
    ]

    if "ONLYC" in sys.argv:
        options.extend(["--generate-c-only"])
    
    # 添加优化或调试选项
    if "NAV" in sys.argv:
        options.extend(["--lto=yes"])
    else:
        options.extend(["--lto=no"])
    
    if "DEBUG" in sys.argv:
        options.extend(["--debug", "--debugger"])
    else:
        options.extend(["--assume-yes-for-downloads"])
    
    # 合并数据文件选项
    options.extend(data_options)
    
    return options

def configure_environment():
    """配置编译环境变量"""
    # 设置MinGW路径
    os.environ["NUITKA_MINGW64"] = "D:\\Build\\mingw64\\"
    
    # 配置系统路径
    if platform.system() == "Windows":
        os.environ["PATH"] = (
            r"C:\Program Files (x86)\Windows Kits\10\bin\x64;"
            r"D:\Microsoft Visual Studio\18\Insiders\VC\Tools\MSVC\14.50.35503\bin\Hostx64\x64;"+ os.environ["PATH"]
        )
    
    # 配置编译 flags
    is_nav = "NAV" in sys.argv
    os.environ["CFLAGS"] = (
        f"-m64 {'-O3 -s' if is_nav else '-O0'} "
        r"-Wl,--stack,0x4000000 "
        r"-L 'D:\msys64\mingw64\include' "
        r"-L 'C:\Users\Lenovo\Desktop\Termination4\.ENV\Lib\site-packages\nuitka\build\include' "
        r"-L 'D:\Python312\include'"
    )

def run_nuitka():
    """执行Nuitka编译"""
    start_time = time.time()
    print("开始使用Nuitka编译...")
    
    try:
        # 获取编译选项
        options = get_nuitka_options()
        
        # 执行编译命令
        subprocess.run(
            [r".\.ENV\SCRIPTS\python.exe", "-m", "nuitka"] + options,
            check=True,
            shell=True
        )
        
        print(f"编译成功！耗时: {time.time() - start_time:.2f}秒")
        
    except subprocess.CalledProcessError as e:
        print(f"编译失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生未知错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    configure_environment()
    run_nuitka()
