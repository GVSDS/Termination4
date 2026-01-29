# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_Process
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Due to the particularity of this project,
# This project needs to execute multiple asynchronous tasks at the same time and needs appropriate management,
# This file is the communication between multiple threads, mounting, starting, stopping, etc.,
# Using ctypes to report an error winerror to force stop the thread.


from .T_imports import *
from . import T_Log
from . import T_Std


def Synchronized(LockAttr: str):
    def Decorator(func: typing.Callable):
        def Wrapper(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            lock: threading.Lock = getattr(self, LockAttr)
            with lock:
                return func(self, *args, **kwargs)
        return Wrapper
    return Decorator

class CallbackManager:
    def __init__(self) -> None:
        self._CallBacks: dict = {}
        self._CallBackIDCounter: int = 0
        self._Lock = threading.Lock()
    @Synchronized('_Lock')
    def AddCallBack(self, CallBack: typing.Callable) -> int:
        self._CallBackIDCounter += 1
        CallBackID: int = self._CallBackIDCounter
        self._CallBacks[CallBackID] = CallBack
        return CallBackID
    @Synchronized('_Lock')
    def RemoveCallBack(self, CallBackID: int) -> bool:
        if CallBackID in self._CallBacks:
            del self._CallBacks[CallBackID]
            return True
        return False
    @Synchronized('_Lock')
    def ClearCallBacks(self) -> None:
        self._CallBacks.clear()
    @Synchronized('_Lock')
    def ExecuteCallBacks(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        for CallBack in self._CallBacks.values():
            try: CallBack(*args, **kwargs)
            except Exception as e: print(T_Std.ErrorFormat(e, "Execute Callbacks Error"))

class TProcess(threading.Thread):
    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__()
        self.Args: tuple = args
        self.Kwargs: dict = kwargs
        self._StopEvent: threading.Event = threading.Event()
        self._Manager: TProcessManager | None = None
        self.desc: str = ""
        self.progress: int = 0
        self.editor: list[dict] = []
    def AddEditor(self, name: str, key: str, type: typing.Literal["str", "int", "float", "radio", "multiple", "bool"], choices: list=[]) -> None:
        self.editor.append({"name": name, "key": key, "type": type, "choices": choices})
    def SetManager(self, Manager: 'TProcessManager') -> None:
        self._Manager: TProcessManager | None = Manager
    def Run(self) -> None:
        raise NotImplementedError("Subclasses must implement Run method")
    def run(self) -> None:
        self.logger = T_Log.LoggerChild(self._Manager.master.Log, self.name) if self._Manager else None # 报错
        try:
            if self._Manager: self._Manager._OnThreadStart(self.name)
            self.Run(*self.Args, **self.Kwargs)
        except SystemExit: pass
        except Exception as e: print(T_Std.ErrorFormat(e, "Thread Run Error"))
        finally: self._CleanUp()
    def join(self, timeout: int | None = None):
        super().join(timeout)
        self._CleanUp()
    def Stop(self) -> None:
        self._StopEvent.set()
        self.join()
    def ShouldStop(self) -> bool:
        return self._StopEvent.is_set()
    def _CleanUp(self):
        if self._Manager: # and not self.is_alive():
            self._Manager._OnThreadEnd(self.name)
            self._Manager.RemoveThread(self.name)

class TProcessManager:
    def __init__(self, master: 'Termination4.Termination') -> None:
        self._Threads: typing.Dict[str, TProcess] = {}
        self._Lock = threading.Lock()
        self._StartCallBacks: CallbackManager = CallbackManager()
        self._EndCallBacks: CallbackManager = CallbackManager()
        self.master: 'Termination4.Termination' = master
    def _OnThreadStart(self, ThreadName: str) -> None:
        self._StartCallBacks.ExecuteCallBacks(ThreadName)
    def _OnThreadEnd(self, ThreadName: str) -> None:
        self._EndCallBacks.ExecuteCallBacks(ThreadName)
    def AddStartCallBack(self, CallBack: typing.Callable[[str], None]) -> int:
        return self._StartCallBacks.AddCallBack(CallBack)
    def AddEndCallBack(self, CallBack: typing.Callable[[str], None]) -> int:
        return self._EndCallBacks.AddCallBack(CallBack)
    def RemoveStartCallBack(self, CallBackID: int) -> bool:
        return self._StartCallBacks.RemoveCallBack(CallBackID)
    def RemoveEndCallBack(self, CallBackID: int) -> bool:
        return self._EndCallBacks.RemoveCallBack(CallBackID)
    def ClearStartCallBacks(self):
        self._StartCallBacks.ClearCallBacks()
    def ClearEndCallBacks(self):
        self._EndCallBacks.ClearCallBacks()
    @Synchronized('_Lock')
    def AddThread(self, Thread: TProcess, Name: typing.Optional[str] = None) -> bool:
        ThreadName = Name if Name else Thread.name
        if ThreadName in self._Threads: return False
        Thread.name = ThreadName
        Thread.SetManager(self)
        self._Threads[ThreadName] = Thread
        return True
    @Synchronized('_Lock')
    def RemoveThread(self, Name: str) -> bool:
        if Name not in self._Threads: return False
        if self._Threads[Name]._Manager == self: self._Threads[Name]._Manager = None
        del self._Threads[Name]
        return True
    @Synchronized('_Lock')
    def GetThread(self, Name: str) -> typing.Optional[TProcess]:
        return self._Threads.get(Name)
    @Synchronized('_Lock')
    def GetAllThreads(self) -> typing.Dict[str, TProcess]:
        return self._Threads.copy()
    def StopThread(self, Name: str) -> bool:
        Thread = self.GetThread(Name)
        if Thread:
            Thread.Stop()
            return True
        return False
    def SafeCallWithTimeout(self, TargetFunc: typing.Callable, timeout: float = 1.0) -> tuple[bool, typing.Optional[Exception]]:
        result = {"success": False, "exception": None}
        def _thread_wrapper():
            try:
                TargetFunc()
                result["success"] = True
            except Exception as e: result["exception"] = e
        ExecThread = threading.Thread(target=_thread_wrapper, daemon=True)
        ExecThread.start()
        ExecThread.join(timeout=timeout)
        if ExecThread.is_alive():
            return False, None
        return result["success"], result["exception"]
    def KillThread(self, Name: str) -> bool:
        Thread = self.GetThread(Name)
        if not Thread: return False
        Thread._StopEvent.set()
        try:
            if getattr(Thread, "_Handle_Stop", None):
                self.SafeCallWithTimeout(Thread._Handle_Stop, 5)
        except: pass
        self._OnThreadEnd(Name)
        if not Thread.is_alive():
            self.RemoveThread(Name)
            return True
        ThreadID: int | None = Thread.ident
        if not ThreadID: return False
        res: int | bool = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(ThreadID), ctypes.py_object(SystemExit))
        if res == 0: return False
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ThreadID, None)
            self.TerminateThreadUseSystemAPI(Thread)
            return False
        self.RemoveThread(Name)
        return True
    def StopAllThreads(self) -> None:
        for Name in list(self.GetAllThreads().keys()):
            self.StopThread(Name)
    def KillAllThreads(self) -> None:
        for Name in list(self.GetAllThreads().keys()):
            try: self.KillThread(Name)
            except: print(f"EKill: [{Name}]")
    def TerminateThreadUseSystemAPI(self, Thread: threading.Thread) -> bool:
        if not Thread.is_alive():
            return True
        if os.name == "nt":
            ThreadHandle = ctypes.windll.kernel32.OpenThread(
                1,
                False,
                Thread.ident
            )
            if ThreadHandle == 0: return False
            Result = ctypes.windll.kernel32.TerminateThread(ThreadHandle, 0)
            ctypes.windll.kernel32.CloseHandle(ThreadHandle)
            return Result != 0
        elif os.name == "posix":
            LibpThread = ctypes.CDLL("libpthread.so.0")
            Result = LibpThread.pthread_kill(Thread.ident, 15)
            return Result == 0
        return False

# Description:
# Use For Process (No Threading)

def Mp_Synchronized(lockAttr: str) -> typing.Callable:
    def Decorator(func: typing.Callable):
        def Wrapper(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            lock = getattr(self, lockAttr)
            with lock:
                return func(self, *args, **kwargs)
        return Wrapper
    return Decorator

class Mp_TProcess(mp.Process):
    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__()
        self.Args: tuple = args
        self.Kwargs: dict = kwargs
        self._StopEvent = mp.Event()
        self.desc: str = ""
        self.progress: int = 0
        self.editor: list[dict] = []
        self._LogQueue = mp.Queue() if 'master' in kwargs else None
    def AddEditor(self, name: str, key: str, type: typing.Literal["str", "int", "float", "radio", "multiple", "bool"], choices: list=[]) -> None:
        self.editor.append({"name": name, "key": key, "type": type, "choices": choices})
    def Run(self) -> None:
        raise NotImplementedError("Subclasses must implement Run method")
    def run(self) -> None:
        self.logger = T_Log.Mp_LoggerChild(self._LogQueue, self.name) if self._LogQueue else None
        try:
            self.Run(*self.Args, **self.Kwargs)
        except SystemExit: pass
        except Exception as e: print(T_Std.ErrorFormat(e, "Process Run Error"))
        finally: self._CleanUp()
    def join(self, timeout: int | None = None):
        super().join(timeout)
        self._CleanUp()
    def Stop(self) -> None:
        self._StopEvent.set()
        self.join()
    def ShouldStop(self) -> bool:
        return self._StopEvent.is_set()
    def _CleanUp(self):
        pass

class Mp_TProcessManager:
    def __init__(self, master: 'Termination4.Termination') -> None:
        self._Processes: typing.Dict[str, Mp_TProcess] = {}
        self._Lock = mp.Lock()
        self.master: 'Termination4.Termination' = master
        self._LogQueue = mp.Queue()
    @Mp_Synchronized('_Lock')
    def AddProcess(self, Process: Mp_TProcess, Name: typing.Optional[str] = None) -> bool:
        ProcessName = Name if Name else Process.name
        if ProcessName in self._Processes: return False
        Process.name = ProcessName
        Process._LogQueue = self._LogQueue
        self._Processes[ProcessName] = Process
        return True
    @Mp_Synchronized('_Lock')
    def RemoveProcess(self, Name: str) -> bool:
        if Name not in self._Processes: return False
        del self._Processes[Name]
        return True
    @Mp_Synchronized('_Lock')
    def GetProcess(self, Name: str) -> typing.Optional[Mp_TProcess]:
        return self._Processes.get(Name)
    @Mp_Synchronized('_Lock')
    def GetAllProcesses(self) -> typing.Dict[str, Mp_TProcess]:
        return self._Processes.copy()
    def StopProcess(self, Name: str) -> bool:
        process = self.GetProcess(Name)
        if process:
            process.Stop()
            return True
        return False
    def SafeCallWithTimeout(self, TargetFunc: typing.Callable, timeout: float = 1.0) -> tuple[bool, typing.Optional[Exception]]:
        result = {"success": False, "exception": None}
        def _process_wrapper():
            try:
                TargetFunc()
                result["success"] = True
            except Exception as e: result["exception"] = e
        execProcess = mp.Process(target=_process_wrapper, daemon=True)
        execProcess.start()
        execProcess.join(timeout=timeout)
        if execProcess.is_alive():
            self.KillProcess(execProcess.name)
            return False, None
        return result["success"], result["exception"]
    def KillProcess(self, Name: str) -> bool:
        process = self.GetProcess(Name)
        if not process: return False
        process._StopEvent.set()
        try:
            if getattr(process, "_Handle_Stop", None):
                self.SafeCallWithTimeout(process._Handle_Stop, 5)
        except: pass
        if not process.is_alive():
            self.RemoveProcess(Name)
            return True
        pid = process.pid
        if not pid: return False
        try:
            os.kill(pid, 9)
            self.RemoveProcess(Name)
            return True
        except Exception:
            return self.TerminateProcessUseSystemAPI(process)
    def StopAllProcesses(self) -> None:
        for Name in list(self.GetAllProcesses().keys()):
            self.StopProcess(Name)
    def KillAllProcesses(self) -> None:
        for Name in list(self.GetAllProcesses().keys()):
            try: self.KillProcess(Name)
            except: print(f"EKill: [{Name}]")
    def TerminateProcessUseSystemAPI(self, process: Mp_TProcess) -> bool:
        if not process.is_alive():
            return True
        if os.name == "nt":
            processHandle = ctypes.windll.kernel32.OpenProcess(
                1,
                False,
                process.pid
            )
            if processHandle == 0:
                return False
            result = ctypes.windll.kernel32.TerminateProcess(processHandle, 0)
            ctypes.windll.kernel32.CloseHandle(processHandle)
            return result != 0
        elif os.name == "posix":
            try:
                os.kill(process.pid, 9)
                return True
            except:
                return False
        return False
