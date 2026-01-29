import subprocess
import time
import sys
import os
import platform

def setup_environment():
    """设置编译所需的环境变量"""
    # 根据操作系统类型设置PATH
    if platform.system() == "Windows":
        os.environ["PATH"] = (
            r"C:\Program Files (x86)\Windows Kits\10\bin\x64;" +
            r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64;" +
            r"D:\mingw64\bin;" +
            os.environ["PATH"]
        )
    else:
        print("警告: 此脚本主要针对Windows环境优化")
    
    # 设置CFLAGS
    if "NAV" in sys.argv:
        os.environ["CFLAGS"] = (
            r"-march=native -O3 -s -march=native "
            r"-L 'D:\mingw64\x86_64-w64-mingw32\include' "
            r"-L 'C:\Users\Lenovo\Desktop\Termination4\TESTWORK\.ENV\Lib\site-packages\nuitka\build\include' "
            r"-L 'D:\Python312\include' -no-pie"
        )
    else:
        os.environ["CFLAGS"] = (
            r"-march=native -O0 "
            r"-L 'D:\mingw64\x86_64-w64-mingw32\include' "
            r"-L 'C:\Users\Lenovo\Desktop\Termination4\TESTWORK\.ENV\Lib\site-packages\nuitka\build\include' "
            r"-L 'D:\Python312\include' -no-pie"
        )

def get_nuitka_options():
    """获取Nuitka编译选项"""
    options = [
        "--standalone",
        "--onefile",
        "--lto=yes" if "NAV" in sys.argv else "--lto=no",
        "--show-progress",
        "--jobs=8",
        #"--clang",
        "--mingw64",
        "--standalone",
        "--follow-imports",
        "--debug",
        "test.py"
    ]
    
    # 调试模式选项
    if "DEBUG" in sys.argv:
        options.extend([
            "--debug",
            #"--no-strip",
            "--verbose"
        ])
    else:
        options.extend([
            "--assume-yes-for-downloads",  # 自动确认下载
            "--remove-output",             # 编译前清理输出目录
        ])
    
    return options

def run_nuitka_compilation(options):
    """运行Nuitka编译过程"""
    start_time = time.time()
    print("开始编译...")
    
    try:
        # 构建并执行Nuitka命令
        result = subprocess.run(
            [r".\.ENV\SCRIPTS\python.exe", "-m", "nuitka"] + options,
        )
        
        print("编译成功!")
    except subprocess.CalledProcessError as e:
        print(f"编译失败: {e}")
        if e.stdout:
            print(f"错误详情: {e.stdout}")
        sys.exit(1)
    except Exception as e:
        print(f"发生未知错误: {e}")
        sys.exit(1)
    finally:
        print(f"编译耗时: {time.time() - start_time:.2f}秒")

if __name__ == "__main__":
    setup_environment()
    options = get_nuitka_options()
    run_nuitka_compilation(options)