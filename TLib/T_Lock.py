# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_Lock
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# The logic is slightly more complex than normal window creation by creating a hidden window.
# So that other instances do not exist, and the code that gets all windows can be slightly optimized.


from .T_imports import *
from .T_CDLL import *


class LockMe():
    def __init__(self, ID: str | int, EXE: str) -> None:
        self.EXE: str = EXE
        self.ID: str | int = ID
        self.__init_set__()
    def __init_set__(self) -> None:
        self.hWnd: ctypes.wintypes.HWND | bool | int = False
        self.temp: str = os.getenv("temp")
        self.__python_suffix__: list[str] = ["py", "pyw", "pyc", "pyz", "pyi"]
        self.__python_exe__: list[str] = ["python.exe", "pythonw.exe"]
        self.__exec_suffix__: list[str] = ["exe"]
        self.LockName: str = f"Lock_{self.ID}_[{os.getpid()}].lock"
        self.LockReName: str = f"Lock_{self.ID}_"+r"\[(\d+)\].lock"
    def SearchLockWindow(self, lst: list, mat: str) -> list:
        result: list = []
        for s in lst:
            if (_ := re.match(mat, s)): 
                result.append(_.group(1))
        return result
    def SearchLockWindowWithDict(self, lst: list, mat: str, key: str) -> list:
        result: list = []
        for s in lst:
            if (_ := re.match(mat, s["name"])):
                result.append(s[key] if key else s)
        return result
    def IsOtherLock(self) -> bool:
        result: int = 0
        if self.IsSelfLock(): result = 1
        SLF: list = self.SearchLockWindow(self.GetAllWindowInfo("listname"), self.LockReName)
        return len(SLF) > result
    def GetOtherLockPid(self) -> list:
        return self.SearchLockWindowWithDict(self.GetAllWindowInfo("dict"), self.LockReName, "pid")
    def IsSelfLock(self) -> bool | int:
        return user32.IsWindow(self.hWnd)
    def lock(self) -> None:
        if self.IsOtherLock(): os._exit(0)
        else:
            try: self.CreateHideWindow(self.LockName)
            except: print("WINDOW LOCK ERROR, BUT WE DON'T KILL SELF")
    def CreateHideWindow(self, title: str) -> None:
        def WndProc(hWnd: ctypes.wintypes.HWND, msg: ctypes.wintypes.UINT, wParam: ctypes.wintypes.WPARAM, lParam: ctypes.wintypes.LPARAM) -> ctypes.c_long | int:
            if msg == WM_DESTROY: user32.PostQuitMessage(0)
            return user32.DefWindowProcW(hWnd, msg, wParam, lParam)
        def _CreateWindow() -> None:
            wc: WNDCLASSW = WNDCLASSW()
            wc.style = CS_HREDRAW | CS_VREDRAW
            wc.lpfnWndProc = WNDPROC(WndProc)
            wc.hInstance = kernel32.GetModuleHandleW(None)
            wc.hCursor = user32.LoadCursorW(None, IDC_ARROW)
            wc.hIcon = user32.LoadIconW(None, IDI_APPLICATION)
            wc.lpszClassName = ctypes.c_wchar_p("HiddenWindowClass")
            class_atom: ctypes.wintypes.ATOM | int = user32.RegisterClassW(ctypes.byref(wc))
            if class_atom == 0: return False
            self.hWnd = user32.CreateWindowExW(0, wc.lpszClassName, ctypes.c_wchar_p(title),
                WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
                300, 200,
                None, None, wc.hInstance, None
            )
            if not self.hWnd: return False
            user32.ShowWindow(self.hWnd, SW_HIDE)
            msg: ctypes.wintypes.MSG = ctypes.wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0):
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        thread: threading.Thread = threading.Thread(target=_CreateWindow)
        thread.start()
    def unlock(self) -> None:
        if self.IsSelfLock():
            if user32.IsWindow(self.hWnd):
                user32.SendMessageW(self.hWnd, 0x0010, 0, 0)
    def GetAllWindowInfo(self, mod: typing.Literal["dict", "listname"] = "dict") -> list[dict]:
        l = []
        def EnumWindowsProc(hwnd: ctypes.wintypes.HWND, lParam: ctypes.wintypes.LPARAM):
            title_length: int = user32.GetWindowTextLengthW(hwnd)
            if title_length > 0:
                title: str | int | None = ctypes.create_unicode_buffer(title_length + 1)
                user32.GetWindowTextW(hwnd, title, title_length + 1)
                pid: ctypes.wintypes.DWORD = ctypes.wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                if mod == "dict":
                    try:
                        process: psutil.Process = psutil.Process(pid.value)
                        EXEPath: str = process.exe()
                        l.append({"name": title.value, "pid": pid.value, "exe": EXEPath})
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                if mod == "listname":
                    l.append(title.value)
            return True
        user32.EnumWindows(WNDENUMPROC(EnumWindowsProc), 0)
        return l