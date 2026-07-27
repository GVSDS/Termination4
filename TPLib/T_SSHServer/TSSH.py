import socket
import threading

from paramiko.common import AUTH_SUCCESSFUL, AUTH_FAILED, OPEN_SUCCEEDED, OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
from paramiko import ServerInterface
import datetime
import paramiko
import json
import cmd
import re
import os

from unicodedata import east_asian_width
import traceback
import time






CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SHELL_CONFIG_FILE = os.path.join(CONFIG_DIR, "shell.json")
RSA_KEY_PATH = os.path.join(CONFIG_DIR, "rsa_key.pem")

def split_bytes(s, max_bytes, encoding='utf-8'):
    """将字符串按字节数分割，确保每个分片不超过 max_bytes"""

    result = []
    current = ""
    current_bytes = 0

    for char in s:
        char = str(char)
        char_bytes = len(char.encode(encoding))

        # 如果单个字符就超过 max_bytes，直接报错
        if char_bytes > max_bytes:
            return -1

        # 如果加上当前字符会超限，就先保存当前结果，并重置
        if current_bytes + char_bytes > max_bytes:
            result.append(current)
            current = char
            current_bytes = char_bytes
        else:
            current += char
            current_bytes += char_bytes

    # 添加最后剩余的部分
    if current:
        result.append(current)
    return result

def dispose_string(string):
    """处理字符串格式，替换换行符并编码"""
    return string.replace('\n', '\r\n').encode('utf-8')

def traceback_info():
    """获取异常信息"""
    tracebackInfo = traceback.format_exc()
    return tracebackInfo

def string_width(s):
    """获取字符串的显示宽度"""
    if len(s) == 0:
        return 0
    result = 0
    for i in s:
        if east_asian_width(i) in 'FWA':
            result += 2
        else:
            result += 1
    return result














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
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)

    # 加载或创建shell配置文件
    if not os.path.exists(SHELL_CONFIG_FILE):
        with open(SHELL_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_shell_config, f, indent=4)

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




































def custom_strip(s):
    chars_to_remove = [
        '\u0020',  # 普通空格 (Space)
        '\u3000',  # 全角空格 (Ideographic Space)
        '\u0003',  # U+0003 (End of Text, ETX)
        '\u0009',  # 水平制表符 (Tab, \t)
        '\u000A',  # 换行符 (Line Feed, \n)
        '\u000D',  # 回车符 (Carriage Return, \r)
        '\u000B',  # 垂直制表符 (Vertical Tab, \v)
        '\u000C',  # 换页符 (Form Feed, \f)
    ]
    return s.strip(''.join(chars_to_remove))









class FakeShell(cmd.Cmd):
    def __init__(self, config, shell_config, username = 'ubuntu', hshell = None):
        super().__init__()
        self.shell_config = shell_config
        self.config = config
        self.username = username
        self.hshell = hshell
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
        line = custom_strip(line)
        command = line.split()
        if command == "?":
            return "NO ?"
        return super().onecmd(line)

    def motd(self):
        return self.shell_config['messages']['motd'].format(endl='\r\n')

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

    def get_prompt(self):
        dir_display = self._get_display_path(show_home_as_tilde=True)

        # 获取主机名
        HOSTNAME = self.config['settings']['hostname']

        # ANSI颜色代码
        COLOR_USER = '\033[1;32m'
        COLOR_PATH = '\033[1;34m'
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

    def fake_command(self, command):
        return "This command is not available.\r\n"

    def _replace_escape(self, match):
        """替换转义字符"""
        esc = match.group(1)
        escapes = {
            '\\': '\\',
            'a': '\a',
            'b': '\b',
            'c': '',
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
        line = custom_strip(line)
        command = line.split()[0]
        if command == "exit": return True
        def s():
            time.sleep(5)
            self.hshell._send("\nHELLO")
        threading.Thread(target=s, args=()).start()
        return "\r\n"



class HoneypotShell:
    def __init__(self, channel, client_ip: str, config, shell_config, server):
        self.send_motd = False
        self.channel = channel
        self.client_ip = client_ip
        self.server = server
        self.shell = FakeShell(config, shell_config, self.server.username, self)
        self.left_chars = []
        self.right_chars = []
        self.history = []
        self.history_pos = -1
        self._should_exit = False
        self.partial_utf8 = b''
        self.last_left_chars = []
        self.last_right_chars = []
        self.ctrl_c_pressed = False
        self.terminal_lock = threading.Lock()

    def exec_command(self, command):
        try:
            commands = command.split(';')
            commands = list(filter(lambda x: x.strip(), commands))
            cmd_result = ""
            for cmd in commands:
                result = self.shell.onecmd(cmd)
                if result is True:
                    self._logout(None)
                elif result:
                    cmd_result += result

            if not self._should_exit:
                self._send(cmd_result)
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
                print("x", traceback_info())
                print("x", traceback_info())
                print("x", f"{self.client_ip} - {e}")
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
                print("x", traceback_info())
                print("x", f"{self.client_ip} - Failed to send message: {e}")
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
