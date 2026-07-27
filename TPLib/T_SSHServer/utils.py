from time import strftime, localtime
import os, binascii, traceback
from unicodedata import east_asian_width


LOG_NAME = f'./logs/ssh-honeypot-{strftime("%Y%m%d%H%M%S", localtime())}.log'

LOG_COLORS = {
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'purple': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'RESET': '\033[0m'

}
LOG_COLOR_MAP = {
    '!': LOG_COLORS['yellow'],      # 黄色 - 警告
    '*': '',                        # 默认 - 普通信息
    '+': LOG_COLORS['blue'],        # 蓝色 - 成功
    '-': '',                        # 默认 - 失败
    'x': LOG_COLORS['red'],         # 红色 - 错误
    '@': '',                        # 默认 - 作者信息
    '#': '',                        # 默认 - 代码信息
    'RESET': LOG_COLORS['RESET'],   # 重置颜色
}

# [!] 警告 warning 黄色
# [*] 普通 info
# [+] 加入成功 join success 蓝色
# [-] 加入失败 join fail
# [x] 错误 红色
# [@] 作者相关信息
# [#] 代码相关信息

LOG_DIR = "logs"

def log_init():
    """初始化日志文件"""
    global LOG_NAME
    os.makedirs(LOG_DIR, exist_ok=True)


def dispose_string(string):
    """处理字符串格式，替换换行符并编码"""
    return string.replace('\n', '\r\n').encode('utf-8')


def get_log_color(log_type):
    try:
        return LOG_COLOR_MAP[log_type]
    except KeyError:
        return LOG_COLOR_MAP['RESET']


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

def send_log(log_type, log_message, color = "auto"):
    """发送日志到文件和控制台"""

    log_message = custom_strip(str(log_message))

    log_time = f"[{strftime('%Y-%m-%d %H:%M:%S', localtime())}]"
    log = ""

    # 处理颜色
    color = color.lower()
    if color == "auto":
        color = get_log_color(log_type)
    else:
        if color in LOG_COLORS:
            color = LOG_COLORS[color]
        else:
            color = LOG_COLORS['RESET']

    if "\n" in log_message:
        log_messages = log_message.split("\n")
        for i in range(len(log_messages)):
            if i == 0:
                log += f"{log_time} [{log_type}] {log_messages[i]}"
            else:
                log += f"{string_width(log_time) * ' '} [{log_type}] {log_messages[i]}"
            log += '\n'

    else:
        log += f"{log_time} [{log_type}] {log_message}"
    # 如果目录不存在则创建

    if not os.path.exists(LOG_DIR):
        log_init()

    with open(LOG_NAME, 'a') as f:
        f.write(log + '\n')

    print(f"{color}{log}{LOG_COLOR_MAP['RESET']}")


def traceback_info():
    """获取异常信息"""
    tracebackInfo = traceback.format_exc()
    return tracebackInfo

def is_linux_executable(filepath):
    """
    检测文件是否为Linux可执行文件
    :param filepath: 文件路径
    :return: bool - 是否是Linux可执行文件
    """

    if not os.path.isfile(filepath):
        return False

    try:
        if filepath.endswith('.bashrc') or filepath.endswith('.sh'):
            return True

        with open(filepath, 'rb') as f:
            # 读取文件前4个字节
            header = f.read(4)
            if not header:
                return False

            # 将字节转换为十六进制表示
            hex_header = binascii.hexlify(header).decode('ascii').lower()

            # ELF文件魔数: 7f 45 4c 46
            if hex_header.startswith('7f454c46'):
                return True

            # 也可以检查shebang (#!/bin/bash等)
            if header.startswith(b'#!'):
                # 读取第一行检查是否是有效的shebang
                f.seek(0)
                first_line = f.readline().decode('utf-8', errors='ignore').strip()
                if first_line.startswith('#!') and ('bash' in first_line or 'sh' in first_line or
                                                    'python' in first_line or 'perl' in first_line):
                    return True

    except (IOError, PermissionError):
        return False

    return False


if __name__ == '__main__':
    send_log('test', 'Running successfully!')
