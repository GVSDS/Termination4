import socket
import threading

from utils import *

from paramiko.common import AUTH_SUCCESSFUL, AUTH_FAILED, OPEN_SUCCEEDED, OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
from paramiko import ServerInterface
import datetime
import paramiko
import json
import cmd
import re








CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SHELL_CONFIG_FILE = os.path.join(CONFIG_DIR, "shell.json")
RSA_KEY_PATH = os.path.join(CONFIG_DIR, "rsa_key.pem")


def load_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # 默认配置
    default_config = {
        "settings": {
            "port": 22,
            "banner": "SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.1",
            "hostname": "ubuntu"
        },
        "users": [
            {
                "username": "root",
                "password": "password",
                "home_dir": "root"
            },
            {
                "username": "ubuntu",
                "password": "password",
                "home_dir": "ubuntu"
            }
        ],
        "output": {
            "login_success": "{ip} - Successful login attempt | Username: {username} | Password: {password}",
            "login_failed": "{ip} - Failed login attempt | Username: {username} | Password: {password}",
            "new_connection": "{ip} - New SSH connection established",
            "no_channel_msg": "{ip} - SSH channel negotiation failed (timeout/protocol error)",
            "connection_closed_msg": "{ip} - Connection closed{reason}",
            "connection_error_msg": "{ip} - Connection error: {error}",
            "shutdown_msg": "Server - Shutting down honeypot service",
            "startup_msg": "Server - SSH Honeypot started on {host}:{port}",
            "rsa_key_error": "Server - Invalid RSA key detected: {reason}, generating new key",
            "rsa_key_loaded": "Server - Loaded existing RSA key from {path}",
            "rsa_key_created": "Server - Created new RSA key at {path}",
            "run_command": "{ip} - Executed command: {command}"
        }
    }

    default_shell_config = {
        "messages": {
            "motd": """Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-76-generic x86_64)

* Documentation:  https://help.ubuntu.com
* Management:     https://landscape.canonical.com
* Support:        https://ubuntu.com/advantage
{endl}""",
            "prompt": "{COLOR_USER}{username}@{hostname}:{COLOR_PATH}{path}{RESET}${space}",
            "root_prompt": "root@{hostname}:{path}#{space}"
        }
    }

    # 加载或创建主配置文件
    if not os.path.exists(CONFIG_FILE):
        send_log("+", f"Creating new config file: {CONFIG_FILE}")
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
        send_log("*", f"Server - Config file created: {CONFIG_FILE}")

    # 加载或创建shell配置文件
    if not os.path.exists(SHELL_CONFIG_FILE):
        send_log("+", f"Creating new shell config file: {SHELL_CONFIG_FILE}")
        with open(SHELL_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_shell_config, f, indent=4)
        send_log("*", f"Server - Shell config file created: {SHELL_CONFIG_FILE}")

    # 读取配置文件
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    with open(SHELL_CONFIG_FILE, 'r', encoding='utf-8') as f:
        shell_config = json.load(f)

    # 处理RSA密钥
    rsa_key = None
    if os.path.exists(RSA_KEY_PATH):
        try:
            rsa_key = paramiko.RSAKey(filename=RSA_KEY_PATH)
        except Exception as e:
            rsa_key = paramiko.RSAKey.generate(2048)
            rsa_key.write_private_key_file(RSA_KEY_PATH)
    else:
        rsa_key = paramiko.RSAKey.generate(2048)
        rsa_key.write_private_key_file(RSA_KEY_PATH)

    return config, shell_config, rsa_key















































CMDS = [
    "ls", "cd", "pwd", "mkdir", "rm", "cp", "mv", "touch",
    "cat", "less", "more", "head", "tail", "find", "grep", "ssh",
    "ifconfig", "netstat", "whoami", "hostname", "uname", "df",
    "free", "ps", "kill", "killall", "shutdown", "reboot", "date",
    "history", "alias", "unalias", "echo", "printf", "env", "set",
    "help", "rsync", "ping", "curl", "wget", 'll', 'la', 'ifconfig',
    'uptime', 'reset', 'history', 'exec', 'sshd', 'iptables', 'route',
    'netstat', 'iftop', 'tcpdump', 'traceroute', 'whois', 'dig', 'sh'
]


class FakeShell(cmd.Cmd):
    def __init__(self, config, shell_config, username = 'ubuntu'):
        super().__init__()
        self.shell_config = shell_config
        self.config = config
        self.username = username  # 从配置获取用户名
        if self.username == 'root':
            self.home_path = f"vdisk/root"
            self.restricted_dirs = ['/sys', '/tmp', '/usr', '/var', '/dev']
        else:
            self.home_path = f"vdisk/home/{self.username}"
            self.restricted_dirs = ['/sys', '/tmp', '/usr', '/var', '/dev', '/root']

        self.path = self.home_path  # 当前路径

        self.vdisk_root = "vdisk"
        self.intro = self.motd()
        self.use_rawinput = False
        self.case_sensitive_path = True

    def onecmd(self, line):
        """拦截 '?' 并阻止其调用 do_help"""
        line = custom_strip(line)
        command = line.split()
        if command == "?":
            return self.error_msg("?")  # 返回 "?: command not found"
        return super().onecmd(line)

    def get_prompt(self):
        dir_display = self._get_display_path(show_home_as_tilde=True)

        # 获取主机名
        HOSTNAME = self.config['settings']['hostname']

        # ANSI颜色代码
        COLOR_USER = '\033[1;32m'  # 绿色加粗（用户名）
        COLOR_PATH = '\033[1;34m'  # 蓝色加粗（路径）
        RESET = '\033[0m'  #

        if self.username == 'root':
            return self.shell_config['messages']['root_prompt'].format(
                username=self.username,
                endl='',
                path=dir_display,
                space=' ',
                hostname=HOSTNAME,
            )

        return self.shell_config['messages']['prompt'].format(
            username=self.username,
            endl='',
            path=dir_display,
            space=' ',
            hostname=HOSTNAME,
            COLOR_USER=COLOR_USER,
            COLOR_PATH=COLOR_PATH,
            RESET=RESET
        )

    def motd(self):
        return self.shell_config['messages']['motd'].format(endl='\r\n')

    def error_msg(self, command):
        return f"{command}: command not found\r\n"

    def fake_command(self, command):
        return "This command is not available.\r\n"

    def _normalize_path(self, path):
        """规范化路径，处理相对路径和绝对路径"""
        # 处理~表示home目录
        if path.startswith('~'):
            path = self.home_path
        elif path.startswith('/'):
            # 处理绝对路径
            path = os.path.join(self.vdisk_root, path.lstrip('/'))
        else:
            # 处理相对路径
            path = os.path.join(self.path, path)

        # 规范化路径，解析..和.
        normalized = os.path.normpath(path)

        # 确保路径仍在虚拟磁盘内
        abs_vdisk = os.path.abspath(self.vdisk_root)
        if not os.path.abspath(normalized).startswith(abs_vdisk):
            normalized = self.vdisk_root  # 退回到虚拟根目录

        # 如果是大小写敏感的，检查路径是否存在（精确匹配大小写）
        if self.case_sensitive_path:
            dirname, basename = os.path.split(normalized)
            if dirname and os.path.exists(dirname):
                # 检查目录中的文件名是否大小写匹配
                try:
                    actual_names = os.listdir(dirname)
                    found = False
                    for name in actual_names:
                        if name == basename:  # 精确匹配大小写
                            found = True
                            break
                    if not found and basename:  # 如果没找到且basename不为空
                        return normalized  # 仍然返回原始路径，但后续操作会失败
                except OSError:
                    pass

        return normalized

    def _is_safe_path(self, path):
        """检查路径是否在允许的虚拟磁盘范围内"""
        try:
            abs_path = os.path.abspath(path)
            abs_vdisk = os.path.abspath(self.vdisk_root)

            # 检查是否在虚拟磁盘范围内
            if not abs_path.startswith(abs_vdisk):
                return False

            # 如果是大小写敏感的，检查路径是否存在（精确匹配大小写）
            if self.case_sensitive_path:
                dirname, basename = os.path.split(abs_path)
                if dirname and os.path.exists(dirname):
                    try:
                        actual_names = os.listdir(dirname)
                        if basename and basename not in actual_names:
                            return False  # 大小写不匹配
                    except OSError:
                        pass

            # 检查是否试图访问限制目录
            rel_path = os.path.relpath(abs_path, abs_vdisk)
            rel_path_parts = rel_path.split(os.sep)

            for restricted_dir in self.restricted_dirs:
                # 检查路径的任何部分是否匹配限制目录
                if restricted_dir.lstrip('/') in rel_path_parts:
                    return False

            return True
        except:
            return False

    def _get_display_path(self, path=None, show_home_as_tilde=True):
        """获取用于显示的路径
        :param path: 要显示的路径，None表示当前路径
        :param show_home_as_tilde: 是否将home目录显示为~
        """
        if path is None:
            path = self.path

        # 获取home目录路径
        if self.username == 'root':
            home_path = os.path.join(self.vdisk_root, "root")
        else:
            home_path = os.path.join(self.vdisk_root, "home", self.username)
        abs_home = os.path.abspath(home_path)
        abs_path = os.path.abspath(path)

        # 如果是home目录且需要显示为~
        if show_home_as_tilde and abs_path == abs_home:
            return "~"

        # 如果是home目录的子目录且需要显示为~
        if show_home_as_tilde and abs_path.startswith(abs_home):
            rel_path = os.path.relpath(abs_path, abs_home)
            return f"~/{rel_path}" if rel_path != "." else "~"

        # 处理普通路径
        rel_path = os.path.relpath(path, self.vdisk_root)

        # 处理根目录情况
        if rel_path == ".":
            return "/"

        return "/" + rel_path.replace('\\', '/')

    def _replace_escape(self, match):
        """替换转义字符"""
        esc = match.group(1)
        escapes = {
            '\\': '\\',
            'a': '\a',
            'b': '\b',
            'c': '',  # -c 标志会忽略剩余输出
            'e': '\x1b',
            'f': '\f',
            'n': '\n',
            'r': '\r',
            't': '\t',
            'v': '\v',
            '0': '\0',
            '"': '"'
        }
        return escapes.get(esc, esc)

    def default(self, line):
        """处理未知命令"""
        line = custom_strip(line)
        command = line.split()[0]
        if command in CMDS:
            return "\r\n"
        return self.error_msg(command)

    def do_apt(self, arg):
        """处理apt命令"""
        if arg and custom_strip(arg)[0] == '-get':
            return 'apt-get : Permission denied\r\n'
        return 'apt: Permission denied: /usr/bin/apt\r\n'

    def do_cat(self, arg):
        """输出文件内容，如果是目录则显示错误"""
        args = arg.split()
        result = ""

        if not args:  # 如果没有参数，从标准输入读取（这里不支持）
            return "\r\n"

        for a in args:
            file_path = self._normalize_path(a)

            if os.path.isdir(file_path):
                display_path = self._get_display_path(file_path, False)
                result += f"\ncat: {display_path}: Is a directory"
                continue
            elif not os.path.exists(file_path):
                display_path = self._get_display_path(file_path, False)
                result += f"\ncat: {display_path}: No such file or directory"
                continue

            # 检查是否试图访问限制目录
            if not self._is_safe_path(file_path):
                display_path = self._get_display_path(file_path, False)
                result += f"\ncat: {display_path}: Permission denied"
                continue

            else:
                try:
                    with open(file_path, "r") as f:
                        content = f.read()
                        result += '\n' +content
                except UnicodeDecodeError:
                    display_path = self._get_display_path(file_path)
                    result += f"\ncat: {display_path}: Is a binary file"
                except PermissionError:
                    display_path = self._get_display_path(file_path)
                    result += f"\ncat: {display_path}: Permission denied"
                except:
                    display_path = self._get_display_path(file_path)
                    result += f"\ncat: {display_path}: Error reading file"

        if result.startswith('\n'):  # 移除第一个换行符
            result = result[1:]

        return result + '\r\n'

    def do_cd(self, arg):
        """改变命令位置"""
        args = arg.split()
        if len(args) > 1:
            return "bash: cd: too many arguments\r\n"

        try:
            # 处理无参数情况（回到home目录）
            if not args:
                target = "~"
            else:
                target = args[0]

            # 处理home目录情况
            if target == "~":
                target = f"~/{target[1:]}" if len(target) > 1 else "~"

            # 处理根目录情况
            if target == "/":
                self.path = os.path.join(self.vdisk_root)
                return ""

            # 处理特殊路径
            if target == "-":
                return "bash: cd: OLDPWD not set\r\n"

            # 规范化路径
            new_path = self._normalize_path(target)

            # 确保路径在虚拟磁盘内
            abs_vdisk = os.path.abspath(self.vdisk_root)
            if not os.path.abspath(new_path).startswith(abs_vdisk):
                new_path = self.vdisk_root

            # 检查路径存在性和类型
            if not os.path.exists(new_path):
                return f"bash: cd: {self._get_display_path(new_path)}: No such file or directory\r\n"

            # 如果是大小写敏感的，检查精确匹配
            if self.case_sensitive_path and os.path.basename(new_path):
                dirname = os.path.dirname(new_path)
                basename = os.path.basename(new_path)
                if os.path.exists(dirname):
                    actual_names = os.listdir(dirname)
                    if basename not in actual_names:
                        return f"bash: cd: {self._get_display_path(new_path)}: No such file or directory\r\n"

            if not os.path.isdir(new_path):
                return f"bash: cd: {self._get_display_path(new_path)}: Not a directory\r\n"

            # 检查路径安全性
            if not self._is_safe_path(new_path):
                display_path = self._get_display_path(new_path)
                return f"bash: cd: {display_path}: Permission denied\r\n"

            # 更新当前路径
            self.path = new_path
            return ""

        except Exception as e:
            return f"cd: {str(e)}\r\n"

    def do_clear(self, arg):
        """处理clear命令"""
        return '\033[H\033[2J'

    def do_echo(self, arg):
        """实现echo命令，支持引号字符串和转义字符"""
        # 使用正则表达式解析参数（支持单双引号）
        pattern = re.compile(r'''
            ([^\s"']+           # 非空白非引号字符
            |"(?:[^"\\]|\\.)*"  # 双引号字符串
            |'(?:[^'\\]|\\.)*')
            ''', re.VERBOSE)

        tokens = []
        for match in pattern.finditer(arg):
            token = match.group(1)
            # 处理引号包裹的字符串
            if len(token) >= 2:
                if token.startswith('"') and token.endswith('"'):
                    token = token[1:-1].replace('\\"', '"')
                elif token.startswith("'") and token.endswith("'"):
                    token = token[1:-1].replace("\\'", "'")
            tokens.append(token)

        # 解析参数选项
        output = []
        interpret_escapes = False
        no_newline = False
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.startswith('-'):
                if token == '-n':
                    no_newline = True
                elif token == '-e':
                    interpret_escapes = True
                elif token == '-E':
                    interpret_escapes = False
                else:  # 未知选项结束解析
                    output.extend(tokens[i:])
                    break
                i += 1
            else:
                output.extend(tokens[i:])
                break

        # 处理转义字符（仅双引号字符串需要处理）
        processed = []
        for token in output:
            if interpret_escapes:
                token = re.sub(r'\\([\\abcefnrtv0"])', self._replace_escape, token)
            processed.append(token)

        result = ' '.join(processed)

        # 处理空字符串情况
        if not result and (arg.strip().startswith('"') or arg.strip().startswith("'")):
            result = ''  # 允许输出空字符串

        # 添加换行符
        if no_newline:
            return result

        return result + '\r\n'

    def do_exit(self, arg):
        """处理exit命令"""
        return True  # 返回True表示退出shell

    def do_help(self, arg):
        """处理help命令"""
        return 'help: Permission denied: command is not available\r\n'

    def do_la(self, arg):
        """列出目录内容（长格式，显示隐藏文件）"""
        return self.do_ls(f"-la {arg}")

    def do_ll(self, arg):
        """列出目录内容（长格式）"""
        return self.do_ls(f"-l {arg}")

    def do_logout(self, arg):
        """处理logout命令"""
        return True  # 返回True表示退出shell

    def do_ls(self, arg):
        """列出目录内容"""
        args = arg.split()
        path = self.path
        show_all = False  # -a 显示隐藏文件
        show_dirs = False  # -A 显示隐藏文件，不包括 . 和 ..
        long_format = False  # -l 长格式
        color = True  # 默认启用颜色

        # 颜色定义（文件夹名称蓝色，/符号不染色）
        COLORS = {
            'dir': '\033[1;34m',  # 蓝色加粗（目录名称）
            'exec': '\033[1;32m',  # 绿色加粗（可执行文件）
            'link': '\033[1;36m',  # 青色加粗（链接）
            'reset': '\033[0m'  # 重置颜色
        }

        # 解析参数
        for a in args:
            if a.startswith("-"):
                if "a" in a:
                    show_all = True
                    show_dirs = True
                if "A" in a:
                    show_all = True
                    show_dirs = False
                if "l" in a:
                    long_format = True
            elif a not in (".", ".."):
                path = self._normalize_path(a)

        try:
            # 安全路径检查
            if not self._is_safe_path(path):
                display_path = self._get_display_path(path)
                return f"ls: cannot access '{display_path}': Permission denied\r\n"

            # 获取目录内容（手动添加.和..）
            items = []
            if show_dirs:
                items.extend([".", ".."])
            items.extend(os.listdir(path))

            if not show_all:
                items = [i for i in items if not i.startswith(".")]

            # 处理显示项目
            items_display = []
            for item in items:
                item_path = os.path.join(path, item)
                try:
                    is_dir = os.path.isdir(item_path)
                    is_exec = is_linux_executable(item_path) and not is_dir
                    is_link = os.path.islink(item_path)

                    # 处理显示名称（文件夹名称和/符号分开染色）
                    display_name = item
                    suffix = ""
                    if is_dir:
                        suffix = "/"

                    if color:
                        if is_dir:
                            display_name = f"{COLORS['dir']}{display_name}{COLORS['reset']}{suffix}"
                        elif is_exec:
                            display_name = f"{COLORS['exec']}{display_name}*{COLORS['reset']}"
                        elif is_link:
                            display_name = f"{COLORS['link']}{display_name}@{COLORS['reset']}"
                    else:
                        display_name = f"{display_name}{suffix}"

                    items_display.append(display_name)

                except:
                    items_display.append(item)  # 出错时显示原始名称

            # 长格式处理
            if long_format:
                result = []
                total_blocks = 0  # 改用累加文件大小计算total

                for item in items:
                    item_path = os.path.join(path, item)
                    try:
                        stat = os.stat(item_path)
                        total_blocks += stat.st_size / 512  # 模拟block计算

                        # 文件类型和权限
                        mode = stat.st_mode
                        permissions = (
                            'd' if os.path.isdir(item_path) else
                            'l' if os.path.islink(item_path) else
                            '-'
                        )
                        permissions += ''.join([
                            'r' if mode & 0o400 else '-',
                            'w' if mode & 0o200 else '-',
                            'x' if mode & 0o100 else '-',
                            'r' if mode & 0o040 else '-',
                            'w' if mode & 0o020 else '-',
                            'x' if mode & 0o010 else '-',
                            'r' if mode & 0o004 else '-',
                            'w' if mode & 0o002 else '-',
                            'x' if mode & 0o001 else '-',
                        ])

                        # 时间格式
                        mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
                        now = datetime.datetime.now()
                        if (now - mtime).days > 180:  # 超过6个月显示年份
                            time_str = mtime.strftime('%b %d  %Y')
                        else:
                            time_str = mtime.strftime('%b %d %H:%M')

                        # 文件名处理（名称和符号分开染色）
                        name_part = item
                        suffix = ""
                        if os.path.isdir(item_path):
                            suffix = "/"
                        elif is_linux_executable(item_path):
                            suffix = "*"
                        elif os.path.islink(item_path):
                            suffix = "@"

                        if color:
                            if os.path.isdir(item_path):
                                name_part = f"{COLORS['dir']}{name_part}{COLORS['reset']}"
                            elif is_linux_executable(item_path):
                                name_part = f"{COLORS['exec']}{name_part}{COLORS['reset']}"
                            elif os.path.islink(item_path):
                                name_part = f"{COLORS['link']}{name_part}{COLORS['reset']}"

                        line = (
                            f"{permissions} "
                            f"{stat.st_nlink:>2} "
                            f"{stat.st_uid:<8} "
                            f"{stat.st_gid:<8} "
                            f"{stat.st_size:>8} "
                            f"{time_str} "
                            f"{name_part}{suffix}"
                        )
                        result.append(line)
                    except:
                        result.append(f"?????????? ? ?       ?       ?         ? ? {item}")

                # 添加total行（使用计算得到的blocks）
                if result:
                    result.insert(0, f"total {int(total_blocks)}")
                    return "\n".join(result) + '\r\n'
                else:
                    return ""
            else:
                # 普通格式输出（80字符宽）
                if not items_display:
                    return ""

                term_width = 80  # 固定宽度
                max_len = max(len(item) for item in items_display) + 2
                col_width = min(max_len, term_width)
                num_cols = max(1, term_width // col_width)
                num_rows = (len(items_display) + num_cols - 1) // num_cols

                # 格式化输出
                output = []
                for row in range(num_rows):
                    line = []
                    for col in range(num_cols):
                        idx = row + col * num_rows
                        if idx < len(items_display):
                            item = items_display[idx]
                            line.append(f"{item:<{col_width}}")
                    output.append(''.join(line))
                return "\n".join(output) + '\r\n'

        except FileNotFoundError:
            display_path = self._get_display_path(path)
            return f"ls: cannot access '{display_path}': No such file or directory\r\n"
        except PermissionError:
            display_path = self._get_display_path(path)
            return f"ls: cannot open directory '{display_path}': Permission denied\r\n"

    def do_passwd(self, arg):
        """处理passwd命令"""
        return "passwd: Authentication token manipulation error.\r\n"

    def do_pwd(self, arg):
        """打印当前工作目录"""
        return self._get_display_path(show_home_as_tilde=False) + '\r\n'

    def do_su(self, arg):
        """处理su命令"""
        return "su: faild to execute /bin/bash: Permission denied.\r\n"

    def do_sudo(self, arg):
        """处理sudo命令"""
        return f"{self.username} is not in the sudoers file. This incident will be reported.\r\n"

    def do_whoami(self, arg):
        """返回当前用户名"""
        return self.username + '\r\n'


class HoneypotShell:
    def __init__(self, channel, client_ip: str, config, shell_config, server):
        self.send_motd = False
        self.channel = channel
        self.client_ip = client_ip
        self.server = server
        self.shell = FakeShell(config, shell_config, self.server.username)
        self.left_chars = []   # 光标左侧字符列表
        self.right_chars = []  # 光标右侧字符列表
        self.history = []
        self.history_pos = -1
        self._should_exit = False
        self.partial_utf8 = b''
        self.last_left_chars = []
        self.last_right_chars = []
        self.ctrl_c_pressed = False

    def exec_command(self, command):
        """执行命令"""
        try:
            commands = command.split(';')
            commands = list(filter(lambda x: x.strip(), commands))  # 去掉重复项

            cmd_result = ""

            for cmd in commands:
                result = self.shell.onecmd(cmd)
                if result is True:
                    self._logout(None)
                elif result:
                    cmd_result += result

            if not self._should_exit:  # 如果用户没有退出
                self._send(cmd_result)  # 输出命令执行结果
        finally:
            self._close_channel()



    def run(self):
        self._send(self.shell.motd())
        self._send_prompt()
        while not self._should_exit:
            try:
                data = self.channel.recv(1)
                if not data:
                    break

                # 处理Ctrl+C
                if data == b'\x03':
                    self._handle_ctrl_c()
                    continue

                # UTF-8解码
                try:
                    self.partial_utf8 += data
                    char = self.partial_utf8.decode("utf-8")
                    self.partial_utf8 = b''
                except UnicodeDecodeError:
                    if len(self.partial_utf8) >= 4:
                        self.partial_utf8 = b''
                    continue

                # 控制序列处理
                if char == '\x1b':
                    seq = self.channel.recv(1024)
                    if seq == b'[A':    # 上箭头
                        self._handle_arrow_up()
                    elif seq == b'[B':  # 下箭头
                        self._handle_arrow_down()
                    elif seq == b'[C':   # 右箭头
                        self._move_right()
                    elif seq == b'[D':  # 左箭头
                        self._move_left()
                    elif seq == b'[H':   # Home
                        self._move_home()
                    elif seq == b'[F':   # End
                        self._move_end()
                    elif seq == b'[3~': # Del
                        self._handle_del()
                    continue

                # 退格键
                if char in ('\x7f', '\x08'):
                    self._handle_backspace()
                    continue

                # 回车键
                if char in ("\r", "\n"):
                    self._handle_enter()
                    continue

                # 普通字符输入
                self._insert_char(char)

            except (paramiko.SSHException, EOFError, UnicodeDecodeError) as e:
                send_log("x", traceback_info())
                send_log("x", traceback_info())
                send_log("x", f"{self.client_ip} - {e}")
                break

    def _send(self, message, size = 1024, std = True):
        """发送消息 (替代channel.send)，分块发送防止socket爆炸"""
        if not std:
            self.channel.send(message)
            return

        messages = split_bytes(message, size)

        for msg in messages:
            msg = dispose_string(msg)

            try:
                # 发送消息
                self.channel.send(msg)

            except Exception as e:
                send_log("x", traceback_info())
                send_log("x", f"{self.client_ip} - Failed to send message: {e}")
                continue

    def _close_channel(self):
        """关闭通道"""
        self.channel.shutdown_write()
        self.channel.shutdown_read()
        self.channel.shutdown(how="send")
        self.channel.send_exit_status(0)
        self.channel.close()
        return

    def _send_prompt(self):
        """发送提示符（不换行）"""
        self._send(self.shell.get_prompt())

    def _update_display(self, is_full_redraw=False):
        """更新终端显示"""
        if is_full_redraw:
            # 整行重绘（用于命令执行、历史记录切换等）
            self._send(b'\r\x1b[K', std = False)
            self._send_prompt()
            self._send(''.join(self.left_chars + self.right_chars))
        else:
            # 局部刷新（普通编辑时）
            if self.right_chars:
                # 输出右侧字符并移回光标
                self._send(''.join(self.right_chars))
                self._send(f'\x1b[{string_width(self.right_chars)}D', std = False)

    def _insert_char(self, char):
        """插入字符（仅发送新增字符）"""
        self.left_chars.append(char)
        self._send(char)
        self._update_display()

    def _handle_backspace(self):
        """退格键处理（局部删除）"""
        if self.left_chars:
            deleted_char = self.left_chars.pop()
            char_len = string_width(deleted_char)
            self._send(f'\x1b[{char_len}D\x1b[K', std = False)
            self._update_display()

    def _handle_del(self):
        """Del键处理"""
        if self.right_chars:
            self.right_chars.pop(0)
            self._send(b'\x1b[K', std = False)
            self._update_display()

    def _move_left(self):
        """光标左移"""
        if self.left_chars:
            self.right_chars.insert(0, self.left_chars.pop())
            char = self.right_chars[0]
            char_len = string_width(char)
            self._send(f'\x1b[{char_len}D', std = False)

    def _move_right(self):
        """光标右移"""
        if self.right_chars:
            self.left_chars.append(self.right_chars.pop(0))
            char = self.left_chars[-1]
            char_len = string_width(char)
            self._send(f'\x1b[{char_len}C', std = False)

    def _move_home(self):
        """光标移到行首"""
        move_len = string_width(self.left_chars)
        if move_len > 0:
            self._send(f'\x1b[{move_len}D', std = False)
        self.right_chars = self.left_chars + self.right_chars
        self.left_chars = []


    def _move_end(self):
        """光标移到行尾"""
        move_len = string_width(self.right_chars)
        if move_len > 0:
            self._send(f'\x1b[{move_len}C', std = False)
        self.left_chars = self.left_chars + self.right_chars
        self.right_chars = []

    def _handle_arrow_up(self):
        """上箭头（历史记录）"""
        if self.history:
            if self.history_pos == -1:
                self.last_left_chars = self.left_chars.copy()
                self.last_right_chars = self.right_chars.copy()
                self.history_pos = len(self.history) - 1
            elif self.history_pos > 0:
                self.history_pos -= 1
            self.left_chars = list(self.history[self.history_pos])
            self.right_chars = []
            self._update_display(is_full_redraw=True)

    def _handle_arrow_down(self):
        """下箭头（历史记录）"""
        if self.history:
            if self.history_pos < len(self.history) - 1:
                self.history_pos += 1
                self.left_chars = list(self.history[self.history_pos])
                self.right_chars = []
                self._update_display(is_full_redraw=True)
            elif self.history_pos == len(self.history) - 1:
                self.history_pos = -1
                self.left_chars = self.last_left_chars.copy()
                self.right_chars = self.last_right_chars.copy()
                self._update_display(is_full_redraw=True)

    def _handle_enter(self):
        """回车键执行命令"""
        if self.ctrl_c_pressed:
            self.ctrl_c_pressed = False
            self.left_chars = []
            self.right_chars = []
            self._send(b'\r\n')
            self._send_prompt()
            return

        input_str = ''.join(self.left_chars + self.right_chars)
        command = custom_strip(input_str)

        if command:
            self.history_pos = -1
            self.history.append(input_str)
            print("run_command", self.client_ip, command)

            commands = command.split(';')
            commands = list(filter(lambda x: x.strip(), commands))  # 去掉重复项


            cmd_result = "\r\n"

            for cmd in commands:
                result = self.shell.onecmd(cmd)
                if result is True:
                    self._logout(None)
                elif result:
                    cmd_result += result

            if not self._should_exit: # 如果用户没有退出
                self._send(cmd_result) # 输出命令执行结果

        else:
            self._send('\n')

        if not self._should_exit:
            self.left_chars = []
            self.right_chars = []
            self._send_prompt()

    def _handle_ctrl_c(self):
        """Ctrl+C处理"""
        if not self.left_chars and not self.right_chars:
            self._send("^C\n")
            self._send_prompt()
        else:
            self.left_chars.extend(list("^C"))
            self._send("^C\n")
            self.ctrl_c_pressed = True
            self.left_chars = []
            self.right_chars = []
            self._send_prompt()

    def _logout(self, arg):
        self._send("\n")

        self._send("exit\n")
        self._should_exit = True
        print("connection_closed", self.client_ip, "User logged out")
        self._close_channel()





class FakeSSHServer(ServerInterface):
    def __init__(self, config, client_ip):
        self.username = None
        self.password = None
        self.command = None
        self.config = config
        self.channel_ready = threading.Event()
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        self.username = username
        self.password = password

        for user in self.config['users']:
            if (username == user['username'] and
                    password == user['password']):
                print("login success", self.client_ip, username, password)
                return AUTH_SUCCESSFUL

        print("login failed", self.client_ip, username, password)
        return AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return OPEN_SUCCEEDED
        return OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.channel_ready.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixel_width, pixel_height, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        self.channel_ready.set()
        self.command = command.decode('utf-8')
        print("RUNCOMMAND: ", self.client_ip, self.command)
        return True

    def get_allowed_auths(self, username):
        return "password"



def handle_connection(client_sock, client_addr, config, shell_config, rsa_key):
    client_ip = client_addr[0]
    print("CON:", client_ip)

    transport = None
    channel = None

    try:
        transport = paramiko.Transport(client_sock)
        transport.local_version = config['settings']['banner']
        transport.add_server_key(rsa_key)
        server = FakeSSHServer(config, client_ip)

        try:
            transport.start_server(server=server)
            channel = transport.accept(60)
            transport.banner_timeout = 60
            transport.handshake_timeout = 30

        except paramiko.SSHException as e:
            print(client_ip, "Invalid SSH banner (possible telnet/HTTP/scan tool)", "-")
        except (ConnectionResetError, ConnectionError):
            print(client_ip, "Connection reset by peer", "-")
        except EOFError:
            print(client_ip, "Connection closed by client (possible telnet/HTTP/scan tool)", "-")
        except Exception as e:
            print("x", traceback_info())
            return

        if channel is None:
            print(client_ip)
            print(client_ip, "Timeout or Connection closed by client")
            return

        shell = HoneypotShell(channel, client_ip, config, shell_config, server)
        server.channel_ready.wait()
        if server.command is None:
            shell.run()
        else:
            shell.exec_command(server.command)

    except Exception as e:
        print("x", traceback_info())
    else:
        print(client_ip, "Client disconnected", "!")
    finally:
        if transport:
            transport.close()




class SSHServer(socket.socket):
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        config, shell_config, rsa_key = load_config()
        self.config = config
        self.shell_config = shell_config
        self.rsa_key = rsa_key

    def Start(self):
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((self.host, self.port))
        self.listen(100)
        self.settimeout(0.5)

        try:
            while True:
                try:
                    client_sock, client_addr = self.accept()
                    threading.Thread(
                        target=handle_connection,
                        args=(client_sock, client_addr, self.config, self.shell_config, self.rsa_key),
                        daemon=True
                    ).start()
                except socket.timeout:
                    pass
                except Exception as e:
                    pass

        except KeyboardInterrupt:
            print("shutdown_server")
        finally:
            self.close()

con = SSHServer("0.0.0.0", 22)
con.Start()
