import socket

SERVER_ADDRESS = ('localhost', 12345)

def send_client_message(message):
    """作为客户端发送消息到服务器"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(SERVER_ADDRESS)
        client_socket.sendall(message.encode('utf-8'))
        response = b""
        while True:
            part = client_socket.recv(4096)
            response += part
            if len(part) < 4096:
                break
        return response.decode('utf-8')
        
    except ConnectionRefusedError:
        return "错误: 无法连接到服务器，请确保服务器已启动"
    except Exception as e:
        return f"客户端错误: {str(e)}"
    finally:
        client_socket.close()

def repl_client():
    """启动交互式REPL客户端"""
    print(f"连接到服务器 {SERVER_ADDRESS} 的交互式客户端")
    print("输入要执行的命令，或输入 'exit' 退出")
    print("-" * 50)
    
    while True:
        try:
            # 读取用户输入
            user_input = input(">>> ")
            
            # 检查退出条件
            if user_input.strip().lower() == 'exit':
                print("退出客户端...")
                break
            
            # 发送消息并获取响应
            response = send_client_message(user_input)
            
            # 打印响应
            print("服务器响应:")
            print(response)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n接收到中断信号，退出客户端...")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")
            print("-" * 50)

if __name__ == "__main__":
    repl_client()

import socketio

# Termination.TWNT.Socket.connect(f"{Termination.TWNT.PATFile['X']}://{Termination.TWNT.PATFile['Host']}:{Termination.TWNT.PATFile['Port']}", headers={"data": Termination.TWNT.GodKeys.encrypt_16({"PCMachineGUID": Termination.TWNT.PCMachineGUID,"PCVersion": Termination.TWNT.__version__,"PCompilation": str(Termination.TWNT.master.Version.version["Compilation"]["Runs"]),"PCName": socket.gethostname(),"PCreateUserName": os.getenv('USERNAME'),"PCSystemINFO": json.dumps(Termination.TWNT.ComputerINFO),})},wait_timeout=10,namespaces=["/Termination4SocketIOSpace"],transports=['websocket'],socketio_path="/socket.io")