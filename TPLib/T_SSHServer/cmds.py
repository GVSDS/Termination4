from utils import *
from getpass import getuser
import cmd
import datetime, os, re

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
