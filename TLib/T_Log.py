# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_Log
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# The built-in log system has no advantage over other third-party log systems,
# But it is more suitable for this project than other log systems,
# And it can better adapt to this project by using the module loader of this project.


from .T_imports import *
from . import T_Process, T_Std
from TLhread import Thread_TWNT
import os

class Logger(T_Process.TProcess):
    def Run(self, MainName: str, LogFilePath: str, Echo: bool = True) -> None:
        self.desc: str = "Historian, Record Procedural Events"
        self.MainName: str = MainName
        self.LogFilePath: str = LogFilePath
        self.Echo: int = Echo
        self.LogQueue: queue.Queue = queue.Queue()
        self._pid = os.getpid()
        self._ppid = os.getppid()
        self.TWNT: Thread_TWNT.TWNetworkTransit | None = None
        self.Mp_TProcessManager: T_Process.Mp_TProcessManager | None = None
        LogDir: str = os.path.dirname(LogFilePath)
        self.AddEditor("MainName", "MainName", "str")
        self.AddEditor("LogFilePath", "LogFilePath", "str")
        self.AddEditor("Echo", "Echo", "bool")
        if not os.path.exists(LogDir):
            os.makedirs(LogDir)
        threading.Thread(target=self.HandleMpLog, daemon=True).start()
        while not self.ShouldStop():
            LogEntry: dict | str | None = self.LogQueue.get()
            if LogEntry is None: break
            if LogEntry == "Reset":
                with open(self.LogFilePath, "w", encoding="utf-8") as F: F.write("")
            self.HandleLogEntry(LogEntry)
            self.LogQueue.task_done()
    def HandleMpLog(self):
        while not self.ShouldStop():
            if not self.Mp_TProcessManager:
                time.sleep(1)
                continue
            LogEntry: dict | str | None = self.Mp_TProcessManager._LogQueue.get()
            if LogEntry is None: break
            if LogEntry == "Reset":
                with open(self.LogFilePath, "w", encoding="utf-8") as F: F.write("")
            self.HandleLogEntry(LogEntry)
    def HandleLogEntry(self, LogEntry: dict | str | None):
        if type(LogEntry) == dict:
            try:
                LogLine: str = self._FormatTime(LogEntry["Component"], LogEntry["Message"], LogEntry["LogLevel"], Colored=False)
                try:
                    with open(self.LogFilePath, "a", encoding="utf-8") as F: F.write(LogLine + "\n")
                except Exception as E: self.Error(T_Std.ErrorFormat(E, f"Error Writing To Log File"), "Log", False)
                if LogEntry["Echo"]:
                    try: self.SendTWNTLog(self._CleanColorCodes(LogLine))
                    except Exception as E: self.Error(T_Std.ErrorFormat(E, f"Error Sending Log To Server"), "Log", False)
            except Exception as E:
                self.Error(T_Std.ErrorFormat(E, f"Error WS Log"), "Log", False)
    def SetTWNT(self, TWNT: Thread_TWNT.TWNetworkTransit) -> None:
        self.TWNT: Thread_TWNT.TWNetworkTransit | None = TWNT
    def SendTWNTLog(self, Message: str) -> None:
        if self.TWNT and hasattr(self.TWNT, "Socket") and self.TWNT.IsConnected:
            try: self.TWNT.emit("T4Message", PCMachineGUID = self.TWNT.PCMachineGUID, Message = Message)
            except Exception as E: self.Error(T_Std.ErrorFormat(E, f"Error Sending Log To Server"), "Log", False)
    def _CleanColorCodes(self, text: str) -> str:
        AnsiEscapp: re.Pattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return AnsiEscapp.sub('', text)
    def _EnqueueLog(self, Message: str, LogType: str, Name: str = None, Echo: bool = True) -> str:
        Name: str = Name if Name else self.MainName
        LogEntry: dict = {
            "Component": Name,
            "Message": Message,
            "LogLevel": LogType,
            "Echo": Echo,
        }
        self.LogQueue.put(LogEntry)
        return self._FormatTime(Name, Message, LogType, Colored=True)
    def Error(self, ErrorMessage: str | dict, Name: str = None, Echo: bool = True) -> str:
        Name: str = Name if Name else self.MainName
        FormattedMessage: str = self._EnqueueLog(ErrorMessage, "ERROR", Name, Echo)
        if self.Echo and Echo:
            print(self._ApplyLogLevelColor(FormattedMessage, "ERROR") + colorama.Style.RESET_ALL)
        return FormattedMessage
    def Info(self, InfoMessage: str, Name: str = None, Echo: bool = True) -> str:
        FormattedMessage: str = self._EnqueueLog(InfoMessage, "INFO", Name, Echo)
        if self.Echo and Echo:
            print(self._ApplyLogLevelColor(FormattedMessage, "INFO") + colorama.Style.RESET_ALL)
        return FormattedMessage
    def Warning(self, WarningMessage: str, Name: str = None, Echo: bool = True) -> str:
        FormattedMessage: str = self._EnqueueLog(WarningMessage, "WARNING", Name, Echo)
        if self.Echo and Echo:
            print(self._ApplyLogLevelColor(FormattedMessage, "WARNING") + colorama.Style.RESET_ALL)
        return FormattedMessage
    def Debug(self, DebugMessage: str, Name: str = None, Echo: bool = True) -> str:
        FormattedMessage: str = self._EnqueueLog(DebugMessage, "DEBUG", Name, Echo)
        if self.Echo and Echo:
            print(self._ApplyLogLevelColor(FormattedMessage, "DEBUG") + colorama.Style.RESET_ALL)
        return FormattedMessage
    def Success(self, SuccessMessage: str, Name: str = None, Echo: bool = True) -> str:
        FormattedMessage: str = self._EnqueueLog(SuccessMessage, "SUCCESS", Name, Echo)
        if self.Echo and Echo:
            print(self._ApplyLogLevelColor(FormattedMessage, "SUCCESS") + colorama.Style.RESET_ALL)
        return FormattedMessage
    def _FormatTime(self, Component: str, Message: str, LogLevel: str, Colored: bool = False) -> str:
        TimeStr: str = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime())
        LogLevelStr: str = f"[{LogLevel}]"
        PidStr: str = f"[{self._pid}/{self._ppid}]"
        if Colored:
            TimePart: str = f"{colorama.Fore.BLUE}{TimeStr}{colorama.Style.RESET_ALL}"
            ComponentPart: str = f"{colorama.Fore.YELLOW}[{Component}]{colorama.Style.RESET_ALL}"
            PidPart: str = f"{colorama.Fore.CYAN}{PidStr}{colorama.Style.RESET_ALL}"
        else:
            TimePart: str = TimeStr
            ComponentPart: str = f"[{Component}]"
            PidPart: str = PidStr
        return f"{TimePart} {ComponentPart} {PidPart} {LogLevelStr}: {str(Message)}"
    def _ApplyLogLevelColor(self, Message: str, LogLevel: str) -> str:
        ColorMap: dict = {
            "ERROR": colorama.Fore.RED,
            "INFO": colorama.Fore.WHITE,
            "WARNING": colorama.Fore.YELLOW,
            "DEBUG": colorama.Fore.LIGHTYELLOW_EX,
            "SUCCESS": colorama.Fore.GREEN
        }
        Color: str = ColorMap.get(LogLevel, "")
        LevelStart: str = Message.find(f"[{LogLevel}]")
        if LevelStart != -1:
            LevelEnd: int = LevelStart + len(f"[{LogLevel}]")
            return Message[:LevelStart] + Color + Message[LevelStart:LevelEnd] + colorama.Style.RESET_ALL + Message[LevelEnd:]
        return Message
    def FormatTimeCustom(self, TimeFormat: str = None) -> str:
        return time.strftime(TimeFormat if TimeFormat else "%Y-%m-%d-%H-%M-%S", time.localtime())

class LoggerChild:
    def __init__(self, Master: Logger, Name: str) -> None:
        self.Master: Logger = Master
        self.Name: str = Name
    def Error(self, ErrorMessage: str, Echo: bool = True) -> str:
        return self.Master.Error(ErrorMessage, self.Name, Echo)
    def Info(self, InfoMessage: str, Echo: bool = True) -> str:
        return self.Master.Info(InfoMessage, self.Name, Echo)
    def Warning(self, WarningMessage: str, Echo: bool = True) -> str:
        return self.Master.Warning(WarningMessage, self.Name, Echo)
    def Debug(self, DebugMessage: str, Echo: bool = True) -> str:
        return self.Master.Debug(DebugMessage, self.Name, Echo)
    def Success(self, SuccessMessage: str, Echo: bool = True) -> str:
        return self.Master.Success(SuccessMessage, self.Name, Echo)

class Mp_LoggerChild:
    def __init__(self, Master: mp.Queue, Name: str) -> None:
        self.Master: mp.Queue = Master
        self.Name: str = Name
        self.Echo: bool = False
        self._pid = os.getpid()
        self._ppid = os.getppid()
    def _ApplyLogLevelColor(self, Message: str, LogLevel: str) -> str:
        ColorMap: dict = {
            "ERROR": colorama.Fore.RED,
            "INFO": colorama.Fore.WHITE,
            "WARNING": colorama.Fore.YELLOW,
            "DEBUG": colorama.Fore.LIGHTYELLOW_EX,
            "SUCCESS": colorama.Fore.GREEN
        }
        Color: str = ColorMap.get(LogLevel, "")
        LevelStart: str = Message.find(f"[{LogLevel}]")
        if LevelStart != -1:
            LevelEnd: int = LevelStart + len(f"[{LogLevel}]")
            return Message[:LevelStart] + Color + Message[LevelStart:LevelEnd] + colorama.Style.RESET_ALL + Message[LevelEnd:]
        return Message
    def _FormatTime(self, Component: str, Message: str, LogLevel: str, Colored: bool = False) -> str:
        TimeStr: str = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime())
        LogLevelStr: str = f"[{LogLevel}]"
        PidStr: str = f"[{self._pid}/{self._ppid}]"
        if Colored:
            TimePart: str = f"{colorama.Fore.BLUE}{TimeStr}{colorama.Style.RESET_ALL}"
            ComponentPart: str = f"{colorama.Fore.YELLOW}[{Component}]{colorama.Style.RESET_ALL}"
            PidPart: str = f"{colorama.Fore.CYAN}{PidStr}{colorama.Style.RESET_ALL}"
        else:
            TimePart: str = TimeStr
            ComponentPart: str = f"[{Component}]"
            PidPart: str = PidStr
        return f"{TimePart} {ComponentPart} {PidPart} {LogLevelStr}: {str(Message)}"
    def _CleanColorCodes(self, text: str) -> str:
        AnsiEscapp: re.Pattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return AnsiEscapp.sub('', text)
    def _EnqueueLog(self, Message: str, LogType: str, Name: str = None, Echo: bool = True) -> str:
        LogEntry: dict = {
            "Component": Name,
            "Message": Message,
            "LogLevel": LogType,
            "Echo": Echo,
        }
        self.Master.put(LogEntry)
        return self._FormatTime(Name, Message, LogType, Colored=True)
    def Error(self, ErrorMessage: str | dict, Name: str = None, Echo: bool = True) -> str:
        FormattedMessage: str = self._EnqueueLog(ErrorMessage, "ERROR", Name, Echo)
        if self.Echo and Echo:
            print(self._ApplyLogLevelColor(FormattedMessage, "ERROR") + colorama.Style.RESET_ALL)
        return FormattedMessage
    def Info(self, InfoMessage: str, Name: str = None, Echo: bool = True) -> str:
        FormattedMessage: str = self._EnqueueLog(InfoMessage, "INFO", Name, Echo)
        if self.Echo and Echo:
            print(self._ApplyLogLevelColor(FormattedMessage, "INFO") + colorama.Style.RESET_ALL)
        return FormattedMessage
    def Warning(self, WarningMessage: str, Name: str = None, Echo: bool = True) -> str:
        FormattedMessage: str = self._EnqueueLog(WarningMessage, "WARNING", Name, Echo)
        if self.Echo and Echo:
            print(self._ApplyLogLevelColor(FormattedMessage, "WARNING") + colorama.Style.RESET_ALL)
        return FormattedMessage
    def Debug(self, DebugMessage: str, Name: str = None, Echo: bool = True) -> str:
        FormattedMessage: str = self._EnqueueLog(DebugMessage, "DEBUG", Name, Echo)
        if self.Echo and Echo:
            print(self._ApplyLogLevelColor(FormattedMessage, "DEBUG") + colorama.Style.RESET_ALL)
        return FormattedMessage
    def Success(self, SuccessMessage: str, Name: str = None, Echo: bool = True) -> str:
        FormattedMessage: str = self._EnqueueLog(SuccessMessage, "SUCCESS", Name, Echo)
        if self.Echo and Echo:
            print(self._ApplyLogLevelColor(FormattedMessage, "SUCCESS") + colorama.Style.RESET_ALL)
        return FormattedMessage
