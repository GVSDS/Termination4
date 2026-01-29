import paramiko
import socket
import threading
import subprocess
import os
import sys
import select
from paramiko.ssh_exception import SSHException

class RemoteCmdServer:
    def __init__(self, host='0.0.0.0', port=2222, username='admin', password='password'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.server = None
        self.running = False
        self._setup_server_key()
    
    def _setup_server_key(self):
        if not os.path.exists('server.key'):
            key = paramiko.RSAKey.generate(2048)
            key.write_private_key_file('server.key')
        self.host_key = paramiko.RSAKey.from_private_key_file('server.key')
    
    def _handle_client(self, client_socket):
        try:
            transport = paramiko.Transport(client_socket)
            transport.add_server_key(self.host_key)
            
            server = CmdSSHSession(self.username, self.password)
            transport.start_server(server=server)
            
            channel = transport.accept(30)  # 延长超时时间
            if channel is None:
                print("客户端认证超时或失败")
                return
            
            print(f"客户端 {client_socket.getpeername()} 已连接")
            
            # 设置通道为交互模式
            channel.setblocking(0)
            server.handle_shell(channel)
            
        except SSHException as e:
            print(f"SSH错误: {str(e)}")
        except Exception as e:
            print(f"处理客户端时出错: {str(e)}")
        finally:
            try:
                client_socket.close()
            except:
                pass
            print(f"客户端 {client_socket.getpeername()} 已断开连接")
    
    def start(self):
        self.running = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(10)
            print(f"SSH服务器已启动，监听 {self.host}:{self.port}")
            
            while self.running:
                client_socket, addr = self.server.accept()
                client_thread = threading.Thread(target=self._handle_client, args=(client_socket,))
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            print(f"服务器启动失败: {str(e)}")
            self.stop()
    
    def stop(self):
        self.running = False
        if self.server:
            try:
                self.server.close()
            except:
                pass
        print("SSH服务器已停止")


class CmdSSHSession(paramiko.ServerInterface):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.event = threading.Event()
        self.cmd_process = None
        self.channel = None
        self.prompt = "C:\\>"
        self.running = False
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if username == self.username and password == self.password:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    
    def _update_prompt(self):
        try:
            # 发送cd命令获取当前目录
            self.cmd_process.stdin.write(b'cd\n')
            self.cmd_process.stdin.flush()
            
            # 读取输出直到出现换行
            output = b''
            while b'\n' not in output:
                if self.cmd_process.poll() is not None:
                    break
                chunk = self.cmd_process.stdout.read(1)
                if not chunk:
                    break
                output += chunk
            
            # 解析当前目录
            decoded_output = output.decode('gbk', errors='replace').strip()
            if decoded_output:
                self.prompt = decoded_output.split('\n')[-1] + ">"
        except:
            self.prompt = "C:\\>"
    
    def handle_shell(self, channel):
        self.channel = channel
        self.running = True
        
        try:
            # 启动cmd进程，使用正确的参数
            self.cmd_process = subprocess.Popen(
                'cmd.exe',
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                shell=False
            )
            
            # 发送初始提示符
            self._update_prompt()
            channel.send(self.prompt.encode('gbk'))
            
            # 使用select处理非阻塞IO
            while self.running and not channel.closed:
                # 检查是否有数据可读
                rlist, _, _ = select.select([channel, self.cmd_process.stdout], [], [], 0.1)
                
                for ready in rlist:
                    if ready == channel:
                        # 从客户端读取输入
                        try:
                            data = channel.recv(1024)
                            if not data:
                                self.running = False
                                break
                            # 发送到cmd进程
                            self.cmd_process.stdin.write(data)
                            self.cmd_process.stdin.flush()
                        except:
                            self.running = False
                            break
                            
                    elif ready == self.cmd_process.stdout:
                        # 从cmd读取输出
                        output = self.cmd_process.stdout.read(1024)
                        if output:
                            # 转换编码并发送到客户端
                            try:
                                decoded_output = output.decode('gbk')
                            except UnicodeDecodeError:
                                decoded_output = output.decode('utf-8', errors='replace')
                            channel.send(decoded_output)
                            
                            # 命令执行完后显示提示符
                            if decoded_output.endswith('\n'):
                                self._update_prompt()
                                channel.send(self.prompt.encode('gbk'))
            
        except Exception as e:
            print(f"Shell处理错误: {str(e)}")
        finally:
            # 确保资源被正确释放
            self.running = False
            if self.cmd_process:
                try:
                    self.cmd_process.terminate()
                except:
                    pass
            if not channel.closed:
                channel.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 2222
    username = sys.argv[2] if len(sys.argv) > 2 else 'admin'
    password = sys.argv[3] if len(sys.argv) > 3 else 'password'
    
    server = RemoteCmdServer(port=port, username=username, password=password)
    
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
