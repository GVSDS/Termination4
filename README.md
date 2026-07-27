# Termination4

> **开源 · 大规模 APT 武器病毒 · 教学示范**
>
> 一个面向网络安全教学与攻防研究的大型 APT（高级持续性威胁）武器化病毒开源项目。
> 原生基于 Python 实现，受限于 Python 运行效率，仅作为教学示范；
> 经 **Viper** 工具链改装后，可提供更接近真实 APT 行为特性的高质量教学效果。

---

## 一、项目简介

### 1.1 项目定位

Termination4（全称 *Termination Generally Use Cyber Virus Puppet Weapons*）是一个**开源的大规模 APT 武器病毒**项目，目标是完整复现真实 APT 攻击链路，供安全研究人员、红蓝对抗学习者、高校网络安全教学使用。

项目覆盖 APT 杀伤链的全部核心阶段：

- **初始投放与感染**（Initial Access & Infection）
- **持久化驻留**（Persistence）
- **命令与控制**（Command & Control, C2）
- **横向移动与传播**（Lateral Movement & Propagation）
- **信息收集与回传**（Collection & Exfiltration）
- **反检测与对抗**（Defense Evasion）
- **远程控制**（Remote Control）

### 1.2 为什么是"教学示范"

本项目**完整实现了 APT 的行为模型与代码结构**，但存在一个根本性瓶颈：

> **Python 的运行效率不足以支撑真实大规模 APT 武器的实战需求。**

具体表现为：

| 瓶颈维度 | Python 原生实现的局限 |
|:-|:-|
| **执行效率** | 解释执行，CPU 密集型任务（加密、压缩、图像处理）吞吐量低 |
| **内存占用** | 对象模型开销大，大规模并发感染时内存膨胀严重 |
| **启动速度** | 解释器初始化 + 模块导入耗时，影响投递后的快速响应 |
| **隐蔽性** | 进程特征明显，易于被 EDR 通过解释器特征识别 |
| **分发体积** | 携带完整运行时，体积大、特征强 |

因此，**Python 原生版本仅适合作为静态代码阅读、行为分析、攻防原理教学使用**，不具备实战部署能力。这恰好满足"教学示范"的核心诉求：**结构清晰、可读性高、行为可追溯、便于在隔离环境中观察分析。**

### 1.3 Viper 改装：从教学示范到高质量教学

为弥补 Python 效率瓶颈，项目引入 **Viper** 工具链进行改装。Viper 是一套将 Python 源码编译为高效本地代码的工具链，改装后带来以下教学增益：

| 改装方向 | Viper 改装后的教学价值 |
|:-|:-|
| **性能接近真实 APT** | 本地编译执行，CPU/IO 吞吐量显著提升，使教学演示中的时序、规模更贴近实战 |
| **行为时序还原** | 解决 Python 版因效率失真导致的"演示不像真 APT"问题，让学员观察到真实的感染速率、回传频率 |
| **二进制分析教学** | 编译产物可作为逆向工程样本，支撑二进制静态分析、特征码识别教学 |
| **反检测对抗教学** | 失去 Python 解释器特征后，可在受控环境中演示更真实的 EDR 对抗场景 |
| **跨阶段联调** | 高效执行使全链路联动（感染 → 驻留 → C2 → 回传）成为可演示的整体 |

> **教学建议**：静态代码阅读与原理讲解使用 Python 原生源码；动态行为演示与时序分析使用 Viper 改装版本。两者配合可获得最佳教学效果。

---

## 二、版本信息

- **当前版本**：4.2.0
- **编译版本**：407
- **作者**：Veyra
- **项目地址**：https://github.com/GVSADS/Termination4
- **配套项目**：https://github.com/GVSADS/Termination（未完全同步）

---

## 三、技术架构

### 3.1 核心技术栈

- **主语言**：Python 3.12
- **改装工具链**：Viper（Python → 本地代码编译）
- **打包编译**：Nuitka / PyInstaller
- **C 扩展构建**：CMake + Ninja
- **运行时 C 编译**：TinyCC（见 `TPcc/`，用于运行期快速编译 C 扩展）
- **网络通信**：Socket.IO / WebSocket
- **加密体系**：OpenSSL + 自研 GodKeys 弱对称加密
- **系统接口**：C 扩展（CDLL 调用）

### 3.2 APT 杀伤链模块映射

| 杀伤链阶段 | 对应模块 | 说明 |
|:-|:-|:-|
| **初始投放** | `.inf/Install/`、`.inf/SubstituteExecution/` | 安装器、被感染文件代偿启动 |
| **持久化** | `TLhread/Thread_AutoRun.py`、`.inf/Service/`、`.inf/RegistryOverride/` | 服务注册、注册表劫持、自启动 |
| **C2 通信** | `TLhread/Thread_TWNT.py`、`TPLib/T_SSHServer/`、`TFrp/` | Socket.IO 主通道、SSH 备用通道、内网穿透 |
| **横向传播** | `TLhread/Thread_InfectionWorker.py`、`.inf/TemplateMatcher/` | 移动设备感染、磁盘索引、快速模板匹配 |
| **信息收集** | `TLib/T_KeMouse.py`、`TPLib/T_WMI/`、`TPLib/T_Browser/`、`TPLib/T_DOC/` | 键鼠监听、WMI 系统信息、浏览器数据、文档采集 |
| **屏幕监控** | `TLhread/Thread_TWNTWork.py`（CoverScreen/ListenKM）、`T2SRFB/` | 截图回传、VNC 远程桌面 |
| **凭证窃取** | `TPLib/T_SigThiever/` | 数字签名窃取（SigThief 技术） |
| **反检测** | `TLhread/Thread_AntiVirusSoftware.py`、`TPLib/T_VMDISC/`、`ocr/` | 杀软识别、虚拟机检测、360 弹窗模板匹配 |
| **任务调度** | `TLhread/Thread_LW3T.py`、`TLib/T_LW3T.py` | 本地与网络任务表、定时调度 |
| **远程命令** | `TLhread/Thread_TWNTWork.py`（TWNETProcess） | Python / CMD / PowerShell 命令执行 |
| **更新机制** | `.inf/Update/`、`TLib/T_Version.py` | SHA256 校验、自动更新分发 |

### 3.3 工作线程模型

`TLhread/Thread_TWNTWork.py` 中定义了核心工作线程群：

- **MonitorWorker**：CPU、内存、网络流量硬件监控
- **ListenKMWorker**：键盘 / 鼠标事件捕获与屏幕区域截图
- **TWNTProcessSynchronousWorker**：进程与线程状态同步
- **TWNTCoverScreen**：定时截图与图像压缩上传
- **TWNETProcess**：远程命令解析与执行（Python / CMD / PowerShell）

---

## 四、项目结构

```
Termination4/
├── Termination4.py              # 主程序入口
├── TerminationLib.py            # 核心逻辑（面向对象）
├── TLhread/                     # 线程 / 进程模块
│   ├── Thread_TWNT.py           # 网络传输主线程
│   ├── Thread_TWNTWork.py       # 工作线程群
│   ├── Thread_LW3T.py           # 任务表线程
│   ├── Thread_InfectionWorker.py# 感染线程
│   ├── Thread_AntiVirusSoftware.py # 杀软对抗
│   ├── Thread_AutoRun.py        # 自启动配置
│   ├── Thread_Process.py        # 进程线程
│   ├── Thread_Web.py            # 其他网络服务
│   └── Thread_EasterEgg.py      # 彩蛋
├── TLib/                        # 核心库
│   ├── T_GodKeys.py             # GodKeys 自研加密
│   ├── T_FIO.py                 # 文件 I/O
│   ├── T_Process.py             # 进程 / 线程支持
│   ├── T_KeMouse.py             # 键鼠模拟
│   ├── T_AdministratorMode.py   # 提权
│   ├── T_EXEConfig.py           # 内嵌配置
│   ├── T_Version.py             # 版本与更新
│   ├── T_WSD.py                 # WorkSpaceDeployer 工作目录部署
│   └── ...
├── TPLib/                       # 高级扩展库
│   ├── T_SSHServer/             # SSH C2 通道
│   ├── T_WMI/                   # WMI 信息收集
│   ├── T_VMDISC/                # 虚拟机检测
│   ├── T_Browser/               # 浏览器数据采集
│   ├── T_DOC/                   # 文档采集
│   ├── T_SigThiever/            # 数字签名窃取
│   ├── T_Pyftpdlib/             # 内置 FTP 服务
│   ├── T_IndexEspionageProgram/ # 索引间谍程序
│   └── T_MCDrink/               # 扩展模块
├── T2SRFB/                      # VNC 远程桌面（C++ 实现）
├── TFrp/                        # 内网穿透（PyFrp）
├── TPcc/                        # TinyCC 运行时 C 编译器
├── .inf/                        # C 语言扩展
│   ├── Install/                 # 安装程序
│   ├── Service/                 # 核心服务
│   ├── Update/                  # 更新程序
│   ├── RegistryOverride/        # 注册表重写
│   ├── SubstituteExecution/     # 被感染代偿启动
│   ├── TemplateMatcher/         # 快速模板比较
│   ├── Tools/                   # 工具库
│   └── Test/                    # 技术栈测试
├── TConfig/                     # 配置文件
│   ├── version.ini              # 版本信息
│   ├── EXEConfig.bin            # 加密内嵌配置
│   └── EXEConfig.dict           # 字典格式配置
├── TLUI/                        # 界面相关代码
├── SSLib/                       # OpenSSL 动态链接库
├── static/                      # 静态资源
├── ocr/                         # 360 杀软弹窗匹配模板
├── Art/                         # 美术资源
├── Test/                        # 技术栈测试
├── Prompt/                      # AI 提示词
├── setup_nuitka.py              # Nuitka 编译脚本
├── setup_pack.py                # PyInstaller 打包脚本
└── script.spec                  # PyInstaller 清单
```

---

## 五、编译与运行

### 5.1 Python 原生模式（教学阅读用）

```bash
python Termination4.py
```

> 仅推荐用于源码阅读、行为分析、隔离环境下的功能验证。

### 5.2 Nuitka 编译模式

```bash
python setup_nuitka.py
```

### 5.3 PyInstaller 打包模式

```bash
python setup_pack.py
```

### 5.4 Viper 改装模式（高质量教学用）

使用 Viper 工具链将 Python 源码编译为本地代码，具体使用方式参见 Viper 工具链文档。

> Viper 改装版本适合用于：动态行为演示、时序分析、二进制逆向教学、反检测对抗教学。

---

## 六、配置说明

### 6.1 服务器配置

程序启动时从以下地址拉取 C2 配置：

- `http://wytyh.space3v.work/T.json`
- `https://raw.githubusercontent.com/GVSADS/Termination/refs/heads/main/T.json`

配置文件格式：

```json
{
    "X": "https",
    "Host": "server.example.com",
    "Port": 443
}
```

### 6.2 本地配置

| 文件 | 作用 |
|:-|:-|
| `TConfig/version.ini` | 版本信息 |
| `TConfig/EXEConfig.bin` | 加密内嵌配置（GodKeys 序列化） |
| `TConfig/EXEConfig.dict` | 字典格式配置 |

### 6.3 调试 REPL

程序内置 REPL 调试服务器：

- **地址**：`localhost:12345`
- **功能**：远程执行 Python 代码
- **状态**：Python 模式下启用（编译版本默认关闭）

---

## 七、功能特性

### 7.1 网络功能
- Socket.IO 实时通信与自动重连
- WebSocket 加密传输
- SSH / FTP 备用通道
- 内网穿透（PyFrp）

### 7.2 监控功能
- 系统资源（CPU / 内存 / 网络）监控
- 进程与线程状态监控
- 屏幕截图与 VNC 远程桌面
- 键鼠输入监听

### 7.3 任务管理
- 本地与网络任务表（LW3T）
- 定时任务调度
- 任务执行回调与追踪

### 7.4 系统集成
- Windows 服务集成
- 注册表操作与劫持
- 进程权限管理
- 文件系统操作

### 7.5 对抗能力
- 杀毒软件识别（含 360 弹窗模板匹配）
- 虚拟机与沙箱检测
- 数字签名窃取

---

## 八、开发环境

### 8.1 系统要求

- **操作系统**：Windows 10 / 11
- **Python 版本**：3.12+（避免使用内置 3.10）
- **权限要求**：管理员权限
- **C 编译器**：MSVC / MinGW（用于 C 扩展）

### 8.2 主要依赖

- `socketio-client`：实时通信
- `requests`：HTTP 客户端
- `psutil`：系统监控
- `pynput`：输入监听
- `cryptography`：加密
- `pillow`：图像处理
- `pywin32`：Windows API

---

## 九、安全与法律声明

> **⚠️ 严肃警告**

1. **本项目仅用于网络安全教学、攻防研究与隔离环境测试。**
2. **严禁将本项目用于任何未经授权的真实网络环境或真实目标。**
3. **使用者须遵守所在国家 / 地区的网络安全法律法规。** 在中华人民共和国境内，未经授权传播、使用病毒木马程序违反《中华人民共和国网络安全法》《刑法》第二百八十五条、第二百八十六条等相关规定。
4. **运行前必须在完全隔离的环境中部署**（独立虚拟机、断网、无敏感数据）。
5. **作者不对任何违规使用后果承担责任。**

### 教学使用建议

- ✅ 在隔离虚拟机中观察 APT 行为链
- ✅ 阅读源码理解各攻击阶段实现原理
- ✅ 在红蓝对抗训练中作为红队道具（受控环境）
- ✅ 作为逆向工程与特征识别的样本
- ❌ 严禁连接公网或他人网络
- ❌ 严禁投递至真实主机
- ❌ 严禁用于勒索、破坏、窃密等违法目的

---

## 十、更新机制

1. 检查远程版本 SHA256
2. 下载更新文件
3. 验证文件完整性
4. 执行更新程序（`.inf/Update/`）

---

## 十一、技术支持

- **项目地址**：https://github.com/GVSADS/Termination4
- **配套仓库**：https://github.com/GVSADS/Termination
- **版本**：4.2.0
- **编译次数**：407
- **作者**：Veyra

---

## 十二、许可证

本项目仅供学习与研究使用，不得用于商业用途或任何违法违规用途。使用即代表您已阅读并同意上述安全与法律声明。

```
本项目为教育用途开源项目
Copyright (c) Veyra
Educational Use Only
```
