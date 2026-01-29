# 快速索引文档

## 表层文件

|文件名|类型|作用|权限|
|:-|:-|:-|:-|
\_\_pycache\_\_|文件夹|Python Pyc 缓存文件|读写|
|.ENV|文件夹|Python 虚拟环境|读写|
|.tmp|文件夹|编译时临时文件|读写|
|.inf|文件夹|T C 扩展文件|读写|
|.vscode|文件夹|VSCode 配置文件|读写|
|Art|文件夹|美术相关文件|读写|
|build|文件夹|Pyinstaller 打包时目录|读写|
|dist|文件夹|Pyinstaller 打包输出目录|读写|
|ocr|文件夹|OCR 光学识别 相关文件（半废弃）|读写|
|Prompt|文件夹|AI 提示词相关文件|读写|
|SSLib|文件夹|Pyinstaller 编译时 SSL 补充动态链接库|读写|
|static|文件夹|静态资源文件|读写|
|T2SRFB|文件夹|T2S VNC 项目文件|读写|
|TConfig|文件夹|T 配置文件与版本记录文件|读写|
|Termination4.build|文件夹|Nuitka 编译时 调试中间文件|读写|
|Termination4.dist|文件夹|Nuitka 编译 二进制分发目录|读写|
|Termination4.onefile-build|文件夹|Nuitka 编译时 单文件调试中间文件|读写|
|Test|文件夹|T 技术栈测试文件夹|读写|
|TFrp|文件夹|T PyFrp 项目文件夹|读写|
|TLhread|文件夹|T 线程 / 进程 代码目录|读写|
|TLib|文件夹|T 库文件目录|读写|
|TLUI|文件夹|T 界面相关代码目录|读写|
|TPcc|文件夹|T C 快速编译项目文件|读写|
|TPLib|文件夹|T 高级扩展库代码文件夹|读写|
|upx|文件夹|T UPX 压缩工具文件夹|读写|
|.idea|文件|T 新想法记录|读写|
|App.manifest|文件|微软应用程序分发清单（动态版本）|读写|
|App.rc|文件|微软应用程序资源文件（动态版本）|读写|
|index.md|文件|快速索引文档|读写|
|kitest.py|文件|微软应用程序文件二次分发测试文件|读写|
|line.py|文件|代码行数字数统计文件|读写|
|script.spec|文件|Pyinstaller 打包清单文件|读写|
|setup_nuitka.py|文件|以 Nuitka 方式进行编译|读写|
|setup_pack.py|文件|以 Pyinstaller 方式进行打包|读写|
|Termination4.exe|文件|T 主程序文件（Nuitka 编译输出）|读写|
|Termination4.py|文件|T 主程序文件（Python 源代码，入口点）|读写|
|TerminationLib.py|文件|T 实际逻辑文件（面向对象）|读写|

## .tmp 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|.tmp|文件夹|编译时临时文件|读写|
|.tmp/App.manifest|文件|微软应用程序分发清单（静态版本）|读写|
|.tmp/App.rc|文件|微软应用程序资源文件（静态版本）|读写|
|.tmp/App.res|文件|微软应用程序资源文件（二进制）|读写|

## .Art 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|.Art/icon.ico|文件|应用程序图标|读写|
|.Art/icon.png|文件|应用程序图标图像源文件|读写|
|.Art/T.png|文件|应用程序图标图像设计文件|读写|

## .inf 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|.inf|文件夹|T C 扩展文件|读写|
|.inf/.bin|文件夹|编译输出目录|读写|
|.inf/.Ico|文件夹|T 对于 ICO 篡改技术的源代码|读写|
|.inf/.lib|文件夹|编译动态链接库输出目录|读写|
|.inf/.lib-stb|文件夹|STB_IMAGE 库|读写|
|.inf/.Links|文件夹|链接库|读写|
|.inf/.static|文件夹|编译静态链接库输出目录|读写|
|.inf/.vscode|文件夹|VSCode 配置文件|读写|
|.inf/CMakeFiles|文件夹|CMake 编译时文件|读写|
|.inf/Install|文件夹|安装程序（隐藏 T 实际位置）|读写|
|.inf/Install/installt.c|文件|安装程序 源代码|读写|
|.inf/RegistryOverride|文件夹|注册表重写文件|读写|
|.inf/RegistryOverride/RegistryOverride.c|文件|注册表重写文件 源代码|读写|
|.inf/Service|文件夹|T 核心服务相关文件|读写|
|.inf/Service/service.c|文件|T 核心服务相关文件 源代码|读写|
|.inf/SubstituteExecution|文件夹|T 被感染代偿启动文件|读写|
|.inf/SubstituteExecution/bmain3.c|文件|T 被感染代偿启动文件 源代码|读写|
|.inf/TemplateMatcher|文件夹|T 快速模板比较|读写|
|.inf/TemplateMatcher/TemplateMatcher.c|文件|T 快速模板比较 源代码|读写|
|.inf/Test|文件夹|T 技术栈测试|读写|
|.inf/Test/test.c|文件|T 技术栈测试 源代码|读写|
|.inf/Tools|文件夹|T 工具|读写|
|.inf/Tools/tools.c|文件|T 工具 源代码|读写|
|.inf/Update|文件夹|T 更新程序|读写|
|.inf/Update/update.c|文件|T 更新程序 源代码|读写|
|.inf/*/CMakeFiles|文件夹|CMake 编译时文件|读写|
|.inf/*/App.manifest|文件|微软应用程序分发清单|读写|
|.inf/*/App.rc|文件|微软应用程序资源文件|读写|
|.inf/*/cmake_install.cmake|文件|CMake 安装脚本|读写|
|.inf/*/CMakeLists.txt|文件|CMake 项目文件|读写|
|.inf/.ninja_deps|文件|Ninja 编译时依赖文件|读写|
|.inf/.ninja_log|文件|Ninja 编译时日志文件|读写|
|.inf/build.ninja|文件|Ninja 编译脚本|读写|
|.inf/cmake_install.cmake|文件|CMake 安装脚本|读写|
|.inf/CMakeCache.txt|文件|CMake 缓存文件|读写|
|.inf/CMakeLists.txt|文件|CMake 项目文件|读写|

## build 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|build|文件夹|Pyinstaller 打包时目录|读写|
|build/script|文件夹|Pyinstaller 编译时文件|读写|
|build/script/...|文件夹|参考 Pyinstaller|读写|

## dist 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|dist|文件夹|Pyinstaller 打包输出目录|读写|
|dist/Termination4.exe|文件|T 主程序文件（Pyinstaller 打包输出）|读写|
|dist/Termination.bin|文件|T 主程序文件（放置在 Ftp 的二进制更新分发文件）|读写|

## ocr 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|ocr|文件夹|OCR 光学识别 相关文件（半废弃）|读写|
|ocr/AcceptAll.png|文件|360 - 允许程序所有操作 - 匹配模板|读写|
|ocr/AddToBelive.png|文件|360 - 添加信任 - 匹配模板|读写|
|ocr/CloseBeliveWindow.png|文件|360 - 关闭按钮 - 匹配模板|读写|
|ocr/Down.png|文件|360 - 木马提示向下箭头 - 匹配模板|读写|
|ocr/NFTB.png|文件|360 - 暂不处理 - 匹配模板|读写|

## Prompt 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|Prompt|文件夹|AI 提示词相关文件|读写|
|Prompt/forai|文件|AI 预先要求提示词，使其按照 T 项目标准书写格式来编写代码|读写|
|Prompt/pyfrp.txt|文件|AI 对于 PyFrp 项目的首次提示词|读写|

## SSLib 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|SSLib|文件夹|Pyinstaller 编译时 SSL 补充动态链接库|读写|
|SSLib/libcrypto-3.dll|文件|OpenSSL 底层加密算法 动态链接库|读写|
|SSLib/libcrypto-3.pdb|文件|OpenSSL 底层加密算法 动态链接库 调试符号文件|读写|
|SSLib/libssl-3.dll|文件|OpenSSL 高层安全通信协议 动态链接库|读写|
|SSLib/libssl-3.pdb|文件|OpenSSL 高层安全通信协议 动态链接库 调试符号文件|读写|

## static 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|static|文件夹|静态资源文件|读写|
|static/HA.mp3|文件|“哈哈哈”笑声|读写|
|static/System.ttf|文件|点阵字体|读写|
|static/Termination.DISC|文件|主程序 虚拟磁盘|读写|

## T2SRFB 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|T2SRFB|文件夹|T2S VNC 项目文件|读写|
|T2SRFB/*|-|内容过多|读写|

## TConfig 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|TConfig|文件夹|T 配置文件与版本记录文件|读写|
|TConfig/\_\_init\_\_.py|文件|标识 Python 包|读写|
|TConfig/EXEConfig.dict|文件|EXE 内嵌配置 Python 字典格式|读写|
|TConfig/EXEConfig.bin|文件|EXE 内嵌配置 GodKeys 序列化格式|读写|
|TConfig/version.ini|文件|T 版本内嵌 配置文件|读写|

## Termination4.build 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|Termination4.build|文件夹|Nuitka 编译时 调试中间文件|读写|
|Termination4.build/*|-|Nuitka 编译时 调试中间文件|读写|

## Termination4.dist 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|Termination4.dist|文件夹|Nuitka 编译 二进制分发目录|读写|
|Termination4.dist/*|-|Nuitka 编译 二进制分发目录|读写|

## Termination4.onefile-build 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|Termination4.onefile-build|文件夹|Nuitka 编译时 单文件调试中间文件|读写|
|Termination4.onefile-build/*|-|Nuitka 编译时 单文件调试中间文件|读写|

## Test 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|Test|文件夹|T 技术栈测试文件夹|读写|
|Test/*|-|T 技术栈测试文件|读写|

## TFrp 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|TFrp|文件夹|T PyFrp 项目文件夹|读写|
|TFrp/\_\_pycache\_\_|文件夹|Python Pyc 缓存文件|读写|
|TFrp/A|文件夹|第一版 PyFrp|读写|
|TFrp/\_\_init\_\_.py|文件|标识 Python 包|读写|
|TFrp/client.py|文件|PyFrp 客户端|读写|
|TFrp/server.py|文件|PyFrp 服务器|读写|

## TLhread 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|TLhread|文件夹|T 线程 / 进程 代码目录|读写|
|TLhread/\_\_pycache\_\_|文件夹|Python Pyc 缓存文件|读写|
|TLhread/\_\_init\_\_.py|文件|标识 Python 包|读写|
|TLhread/Thread_AntiVirusSoftware.py|文件|T 对抗 杀毒软件 线程|读写|
|TLhread/Thread_AutoRun.py|文件|T 自动运行 服务配置 线程|读写|
|TLhread/Thread_EasterEgg.py|文件|T 彩蛋 线程|读写|
|TLhread/Thread_InfectionWorker.py|文件|T 感染 线程|读写|
|TLhread/Thread_LW3T.py|文件|T 本地 & 网络 任务表 线程|读写|
|TLhread/Thread_Process.py|文件|T 进程 线程|读写|
|TLhread/Thread_AutoRun.py|文件|T 自动运行 服务配置 线程|读写|
|TLhread/Thread_TWNT.py|文件|T TWNetworkTransit 网络 线程|读写|
|TLhread/Thread_TWNTWork.py|文件|T TWNetworkTransit 网络 线程 工作线程|读写|
|TLhread/Thread_Web.py|文件|T 其它网络 相关服务 线程|读写|

## TLib 下的文件
|文件名|类型|作用|权限|
|:-|:-|:-|:-|
|TLhread|文件夹|T 线程 / 进程 代码目录|读写|
|TLhread/\_\_pycache\_\_|文件夹|Python Pyc 缓存文件|读写|
|TLhread/\_\_init\_\_.py|文件|标识 Python 包|读写|
|TLhread/T_AdministratorMode.py|文件|T 提升管理员模式 库|读写|
|TLhread/T_CDLL.py|文件|T CAPI -> PythonAPI 对接定义 库|读写|
|TLhread/T_EXEConfig.py|文件|T 应用程序 内嵌配置 库|读写|
|TLhread/T_FIO.py|文件|T 文件 I/O 操作 库|读写|
|TLhread/T_Fuck.py|文件|T 格式化列表文本输出 库|读写|
|TLhread/T_GodKeys.py|文件|T GodKeys 弱对称加密算法 库|读写|
|TLhread/T_Hardcoded.py|文件|T 硬编码 库|读写|
|TLhread/T_imports.py|文件|T 库列表 库|读写|
|TLhread/T_KeMouse.py|文件|T 键盘鼠标 模拟操作 库|读写|
|TLhread/T_Lock.py|文件|T 互斥锁 库|读写|
|TLhread/T_LW3T.py|文件|T 本地 & 网络 任务表 库|读写|
|TLhread/T_Process.py|文件|T 进程 / 线程 支持 库|读写|
|TLhread/T_Std.py|文件|T STDOUT/ STDERR 修改 库|读写|
|TLhread/T_TDLL.py|文件|T 工具动态链接库 加载 库|读写|
|TLhread/T_This.py|文件|T 本程序介绍 库（无业务代码）|读写|
|TLhread/T_Tools.py|文件|T 工具 库|读写|
|TLhread/T_Version.py|文件|T 版本记录 & 更新 库|读写|
|TLhread/T_WSD.py|文件|T WorkSpaceDeployer 工作目录部署 库|读写|
