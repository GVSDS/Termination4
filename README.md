# Termination4

## 项目简介

Termination4 是一个基于 Python 的网络测试与数据采集框架，用于内网环境中的大规模网络行为测试和数据收集。

## 版本信息

- **当前版本**: 4.2.0
- **编译版本**: 407
- **作者**: Veyra

## 技术架构

### 核心技术栈

- **编程语言**: Python 3.12
- **编译工具**: Nuitka / PyInstaller
- **网络通信**: Socket.IO
- **加密方式**: OpenSSL + 自定义加密
- **系统接口**: C 扩展 (CDLL)

### 主要组件

#### 1. 网络传输模块 (TWNT)

- Socket.IO 客户端通信
- WebSocket 加密传输
- 自动重连机制
- 远程命令执行

#### 2. 工作线程模块 (TWNTWork)

- **MonitorWorker**: 系统硬件监控
  - CPU 使用率
  - 内存使用情况
  - 网络流量统计

- **ListenKMWorker**: 输入设备监听
  - 键盘事件捕获
  - 鼠标事件捕获
  - 屏幕区域截图

- **TWNTProcessSynchronousWorker**: 进程同步
  - 线程状态监控
  - 进程状态监控

- **TWNTCoverScreen**: 屏幕监控
  - 定时截图上传
  - 图像压缩传输

- **TWNETProcess**: 命令处理
  - Python 代码执行
  - CMD 命令执行
  - PowerShell 命令执行

#### 3. 任务表模块 (LW3T)

- 本地任务管理
- 定时任务调度
- 任务执行回调

#### 4. 感染模块 (InfectionWorker)

- 移动设备检测
- 文件感染标记
- 磁盘索引

#### 5. 辅助模块

- **AntiVirusSoftware**: 安全软件检测
- **AutoRun**: 自启动配置
- **AdministratorMode**: 权限管理
- **WorkSpaceDeployer**: 工作目录部署

## 项目结构

```
Termination4/
├── Termination4.py          # 主程序入口
├── TerminationLib.py        # 核心逻辑
├── TLhread/                 # 线程模块
│   ├── Thread_TWNT.py       # 网络传输
│   ├── Thread_TWNTWork.py   # 工作线程
│   ├── Thread_LW3T.py       # 任务表
│   ├── Thread_InfectionWorker.py  # 感染功能
│   ├── Thread_AntiVirusSoftware.py # 安全检测
│   └── Thread_AutoRun.py    # 自启动
├── TLib/                    # 核心库
│   ├── T_Process.py          # 进程管理
│   ├── T_Log.py             # 日志系统
│   ├── T_FIO.py             # 文件操作
│   ├── T_GodKeys.py         # 加密模块
│   └── ...
├── TPLib/                   # 扩展库
│   ├── T_IndexEspionageProgram/ # 索引程序
│   ├── T_SSHServer/         # SSH 服务
│   └── T_Pyftpdlib/        # FTP 服务
├── .inf/                    # C 语言扩展
│   ├── Install/             # 安装程序
│   ├── Service/             # 服务程序
│   ├── Update/              # 更新程序
│   └── Tools/              # 工具库
├── T2SRFB/                  # VNC 远程桌面
├── TFrp/                    # 内网穿透
├── TConfig/                  # 配置文件
└── SSLib/                   # SSL 库
```

## 编译方式

### 使用 Nuitka 编译

```bash
python setup_nuitka.py
```

### 使用 PyInstaller 打包

```bash
python setup_pack.py
```

## 运行方式

### Python 模式

```bash
python Termination4.py
```

### 编译后的可执行文件

```bash
Termination4.exe
```

## 配置说明

### 服务器配置

程序会从以下地址获取配置：

- `http://wytyh.space3v.work/T.json`
- `https://raw.githubusercontent.com/GVSDS/Termination/refs/heads/main/T.json`

配置文件格式：

```json
{
    "X": "https",
    "Host": "server.example.com",
    "Port": 443
}
```

### 本地配置

- `TConfig/version.ini` - 版本信息
- `TConfig/EXEConfig.bin` - 程序配置（加密）

## 功能特性

### 网络功能

- Socket.IO 实时通信
- WebSocket 加密传输
- 自动重连和故障恢复
- 远程命令执行

### 监控功能

- 系统资源监控
- 进程和线程监控
- 屏幕截图
- 输入设备监听

### 任务管理

- 本地任务表
- 定时任务调度
- 任务执行追踪

### 系统集成

- Windows 服务集成
- 注册表操作
- 进程权限管理
- 文件系统操作

## 开发环境

### 系统要求

- **操作系统**: Windows 10/11
- **Python 版本**: 3.12+
- **权限要求**: 管理员权限

### 依赖库

主要依赖包括：

- `socketio-client`
- `requests`
- `psutil`
- `pynput`
- `cryptography`
- `pillow`
- `pywin32`

## 调试模式

程序内置 REPL 调试服务器：

- **地址**: localhost:12345
- **功能**: 远程执行 Python 代码
- **状态**: Python 模式下启用

## 更新机制

程序支持自动更新：

1. 检查远程版本 SHA256
2. 下载更新文件
3. 验证文件完整性
4. 执行更新程序

## 注意事项

1. 本程序仅用于内网测试环境
2. 需要管理员权限运行
3. 建议在隔离环境中测试
4. 使用前请配置正确的服务器地址

## 技术支持

- **项目地址**: https://github.com/GVSADS/Termination4
- **版本**: 4.2.0
- **编译次数**: 407

## 许可证

本项目仅供学习和研究使用。
