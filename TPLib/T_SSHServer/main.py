import socket
import threading

from config import load_config
from output import Output
from server import handle_connection
from utils import *

# 版本号
VERSION = "2.1"

# 小版本号
MINOR_VERSION = 4748

'''

import ctypes
import sys

kernel32 = ctypes.windll.kernel32


# 创建新控制台
kernel32.FreeConsole()  # 先释放现有控制台
if kernel32.AllocConsole():

    sys.stdout = open("CONOUT$", "w")
    sys.stdin = open("CONIN$", "r")

    print("新控制台输出")
    input("输入任意键退出...")

    kernel32.FreeConsole()
    sys.stdout = sys.__stdout__
    sys.stdin = sys.__stdin__
'''


def main():
    send_log("#", f"Starting SSH Honeypot V{VERSION}.{MINOR_VERSION}...")
    send_log("@", "By yrzd6")
    send_log("#", f"Work directory: {os.getcwd()}")

    config, shell_config, rsa_key = load_config()
    output = Output(config)

    # 从配置获取端口
    PORT = int(config['settings']['port'])
    host = "0.0.0.0"


    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, PORT))
    server_sock.listen(100)
    server_sock.settimeout(0.5)
    output.startup(host, PORT)

    try:
        send_log("#", "Server running...")
        while True:
            try:
                client_sock, client_addr = server_sock.accept()

                threading.Thread(
                    target=handle_connection,
                    args=(client_sock, client_addr, config, shell_config, rsa_key, output),
                    daemon=True
                ).start()
            except socket.timeout:
                pass
            except Exception as e:
                send_log("x", traceback_info())
                send_log("x", f"Server - Error: {e}")

    except KeyboardInterrupt:
        output.shutdown_server()
    finally:
        server_sock.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        send_log("x", "A catastrophic unexpected error occurred in the program.")
        send_log("x", traceback_info())
        send_log("x", f"Error: {e}")