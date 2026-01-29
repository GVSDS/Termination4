from utils import *
from cmds import FakeShell
import paramiko, datetime

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