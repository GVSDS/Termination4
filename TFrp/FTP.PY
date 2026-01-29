import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class Thread_FTP:
    def __init__(self, 
                 Welcome: str = "T_Pyftpdlib Based FTP Server Ready.", 
                 Port: int = 36667,
                 Users: list = [{"UserName": "UserName", "Password": "Password", "Path": r"C:\\", "Perm": "elradfmwMT"}],
                 max_cons: int = 256,
                 max_cons_per_ip: int = 5):
        """初始化FTP服务器配置"""
        self.Welcome: str = Welcome
        self.Port: int = Port
        self.lock: threading.Lock = threading.Lock()
        self.Users: list = Users  # 注意这里原代码写的dict实际应该是list
        self.max_cons: int = max_cons
        self.max_cons_per_ip: int = max_cons_per_ip
        self.server = None
        self.authorizer = None
        self.handler = None
        self.address = None
        
        # 初始化服务器
        self._SetupRoute()

    def _SetupRoute(self):
        """设置FTP服务器路由和权限"""
        self.authorizer = DummyAuthorizer()
        
        # 添加用户
        for user in self.Users:
            username = user["UserName"]
            password = user["Password"]
            path = user["Path"]
            perm = user["Perm"]
            
            if not username and not password:
                # 添加匿名用户
                self.authorizer.add_anonymous(path, perm=perm)
            else:
                # 添加普通用户
                self.authorizer.add_user(username, password, path, perm=perm)
        
        # 配置FTP处理器
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        self.handler.banner = self.Welcome
        self.address = ('0.0.0.0', self.Port)

    def _StartServer(self):
        """启动FTP服务器"""
        if self.server is None:
            self.server = FTPServer(self.address, self.handler)
            self.server.max_cons = self.max_cons
            self.server.max_cons_per_ip = self.max_cons_per_ip
        
        print(f"Starting FTP server on port {self.Port}...")
        print(f"Welcome message: {self.Welcome}")
        print(f"Max connections: {self.max_cons}, Max per IP: {self.max_cons_per_ip}")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer is shutting down...")
            self.server.close_all()

    def start(self):
        """在新线程中启动服务器"""
        self.thread = threading.Thread(target=self._StartServer, daemon=True)
        self.thread.start()
        print("FTP server thread started")

    def Handle_Welcome(self, Value):
        """更新欢迎信息"""
        with self.lock:
            self.Welcome = Value
            # 注意：实时更新欢迎信息需要重新创建handler，这里仅更新存储的值

    def Handle_Port(self, Value):
        """更新端口（需要重启服务器才能生效）"""
        with self.lock:
            self.Port = Value
            self.address = ('0.0.0.0', self.Port)

    def Handle_Users(self, Value):
        """更新用户列表（需要重启服务器才能生效）"""
        with self.lock:
            self.Users = Value
            self._SetupRoute()  # 重新设置权限

    def Handle_max_cons(self, Value):
        """更新最大连接数"""
        with self.lock:
            if self.server:
                self.server.max_cons = Value

    def Handle_max_cons_per_ip(self, Value):
        """更新每个IP的最大连接数"""
        with self.lock:
            if self.server:
                self.server.max_cons_per_ip = Value

if __name__ == "__main__":
    # 示例配置
    ftp_server = Thread_FTP(
        Welcome="Welcome to My FTP Server!",
        Port=36667,
        Users=[
            {"UserName": "user1", "Password": "pass1", "Path": r"C:\\", "Perm": "elradfmwMT"},
            {"UserName": "", "Password": "", "Path": r"C:\\", "Perm": "elr"}  # 匿名用户
        ],
        max_cons=100,
        max_cons_per_ip=3
    )
    
    # 启动服务器
    ftp_server.start()
    
    # 保持主线程运行
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("Main program exiting...")
