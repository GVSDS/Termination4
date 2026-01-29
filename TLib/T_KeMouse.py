# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_KeMouse
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# It is responsible for simulating movement, clicking the mouse and listening,
# And can find the corresponding position on the screen through the template picture,
# Theoretically it can also be found from the picture,
# But it needs to make certain modifications to the program and use the matching DLL.


from .T_imports import *
from .T_CDLL import *


class KeMouse:
    def __init__(self, cdll: ctypes.CDLL | DLL) -> None:
        self.lib: ctypes.CDLL | DLL = cdll
        self.lib.CaptureScreenGray.restype = ctypes.POINTER(GrayImage)
        self.lib.CaptureScreenGray.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.lib.LoadImageGray.restype = ctypes.POINTER(GrayImage)
        self.lib.LoadImageGray.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        self.lib.FindTemplateOptimized.restype = MatchResult
        self.lib.FindTemplateOptimized.argtypes = [
            ctypes.POINTER(GrayImage), 
            ctypes.POINTER(GrayImage), 
            ctypes.c_double,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int
        ]
        self.lib.FreeGrayImage.restype = None
        self.lib.FreeGrayImage.argtypes = [ctypes.POINTER(GrayImage)]
        self.lib.ClickAt.restype = ctypes.c_int
        self.lib.ClickAt.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.Initialize.restype = ctypes.c_int
        self.lib.Initialize.argtypes = []
        if self.lib.Initialize() != 0: raise RuntimeError("Failed To Init")
        self.user32: ctypes.WinDLL = ctypes.WinDLL('user32', use_last_error=True)
        self.user32.SendInput.restype = ctypes.wintypes.UINT
        self.user32.SendInput.argtypes = (
            ctypes.wintypes.UINT,
            ctypes.POINTER(Input),
            ctypes.c_int
        )
        self.user32.SetCursorPos.restype = ctypes.wintypes.BOOL
        self.user32.SetCursorPos.argtypes = (
            ctypes.wintypes.INT,
            ctypes.wintypes.INT
        )
        self.user32.GetCursorPos.restype = ctypes.wintypes.BOOL
        self.user32.GetCursorPos.argtypes = (
            ctypes.POINTER(ctypes.wintypes.POINT),
        )
    def CaptureScreen(self) -> typing.Optional[GrayImage]:
        ErrorCode: ctypes.c_int = ctypes.c_int(0)
        Screen: GrayImage | typing.Any = self.lib.CaptureScreenGray(ctypes.byref(ErrorCode))
        if ErrorCode.value != 0 or not Screen: raise RuntimeError(f"Failed To Capture Screen, Error Code: {ErrorCode.value}")
        return Screen
    def LoadImage(self, FileName: str) -> typing.Optional[GrayImage]:
        ErrorCode: ctypes.c_int = ctypes.c_int(0)
        try:
            Encoded = FileName.encode('utf-8')
            Target: GrayImage = self.lib.LoadImageGray(Encoded, ctypes.byref(ErrorCode))
            if ErrorCode.value != 0: raise RuntimeError(f"Failed To Load Image, Error Code: {ErrorCode.value}")
            if not Target: raise RuntimeError("Returned NULL Pointer")
            return Target
        except Exception as e: raise RuntimeError(f"Failed To Load Image, Error: {str(e)}")
    def FindTemplate(self, Target: str, Threshold: float = 0.9, SearchArea: typing.Optional[typing.Tuple[int, int, int, int]] = None) -> typing.Tuple[typing.Optional[typing.Tuple[int, int]], float]:
        try:
            Target: str = os.path.abspath(Target)
            if not os.path.isfile(Target):
                raise FileNotFoundError(Target)
            TargetImg: GrayImage = self.load_image(Target)
            Screen: GrayImage = self.capture_screen()
            X1: int
            Y2: int
            X2: int
            Y2: int
            X1, Y1, X2, Y2 = -1, -1, -1, -1
            if SearchArea is not None: X1, Y1, X2, Y2 = SearchArea
            Result: MatchResult = self.lib.FindTemplateOptimized(Screen, TargetImg, Threshold, X1, Y1, X2, Y2)
            self.lib.FreeGrayImage(TargetImg)
            self.lib.FreeGrayImage(Screen)
            if Result.error != 0:
                if Result.error == 202: return None, Result.confidence
                raise RuntimeError(f"ErrorCode: {Result.error}")
            return (Result.x, Result.y), Result.confidence
        except Exception as e: raise RuntimeError(f"Failed To Find Template, Error: {str(e)}")
    def MoveTo(self, X: int, Y: int) -> None:
        if not self.user32.SetCursorPos(X, Y): raise ctypes.WinError(ctypes.get_last_error())
    def GetPosition(self) -> dict[int, int]:
        Point: ctypes.wintypes.POINT = ctypes.wintypes.POINT()
        if not self.user32.GetCursorPos(ctypes.byref(Point)): raise ctypes.WinError(ctypes.get_last_error())
        return (Point.x, Point.y)
    def Click(self, X: int = None, Y: int = None, Button: str = 'left', Double: bool = False, Delay: float = 0.1) -> bool:
        try:
            if X is not None and Y is not None:
                if not self.user32.SetCursorPos(X, Y): raise ctypes.WinError(ctypes.get_last_error())
            Point: ctypes.wintypes.POINT = ctypes.wintypes.POINT()
            if not self.user32.GetCursorPos(ctypes.byref(Point)): raise ctypes.WinError(ctypes.get_last_error())
            X, Y = Point.x, Point.y
            Button = Button.lower()
            DownFlag, UpFlag = {
                'left': (0x0002, 0x0004),  # MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
                'right': (0x0008, 0x0010), # MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
                'middle': (0x0020, 0x0040) # MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
            }.get(Button, (None, None))
            if DownFlag is None:
                return False
            def CreateInput(DwFlags: int) -> Input:
                Inp: Input = Input()
                Inp.type = 0
                Inp.union.mi.dwFlags = DwFlags
                Inp.union.mi.dx = X
                Inp.union.mi.dy = Y
                return Inp
            Inputs: list[Input] = []
            Inputs.append(CreateInput(DownFlag))
            Inputs.append(CreateInput(UpFlag))
            if Double:
                time.sleep(Delay)
                Inputs.append(CreateInput(DownFlag))
                Inputs.append(CreateInput(UpFlag))
            InputArray = (Input * len(Inputs))(*Inputs)
            Sent = self.user32.SendInput(
                len(Inputs),
                InputArray,
                ctypes.sizeof(Input)
            )
            return Sent == len(Inputs)
        except Exception:
            return False
    def ClickTargetPNG(self, Target: str, Button: str='left', Threshold: float = 0.9, Sleep: float = 0, SearchArea: typing.Optional[typing.Tuple[int, int, int, int]] = None) -> bool:
        Pos, Confidence = self.FindTemplate(Target, Threshold, SearchArea)
        if not Pos:
            return False
        _=self.click(Pos[0], Pos[1], button=Button)
        time.sleep(Sleep)
        return _
    def ClickTargetPNGAC(self, Target: str, Button: str='left', Threshold: float = 0.9, Sleep: float = 0, SearchArea: typing.Optional[typing.Tuple[int, int, int, int]] = None, Confidence: float = 0.9) -> bool:
        Pos, Confidence = self.FindTemplate(Target, Threshold, SearchArea)
        if not Pos or Confidence < Confidence:
            return False
        _=self.click(Pos[0], Pos[1], button=Button)
        time.sleep(Sleep)
        return _
    def ScreenshotBytes(self) -> bytes:
        HDesktop = win32gui.GetDesktopWindow()
        Width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        HDC = win32gui.GetWindowDC(HDesktop)
        MfcDc = win32ui.CreateDCFromHandle(HDC)
        SaveDc = MfcDc.CreateCompatibleDC()
        Bitmap = win32ui.CreateBitmap()
        Bitmap.CreateCompatibleBitmap(MfcDc, Width, height)
        SaveDc.SelectObject(Bitmap)
        SaveDc.BitBlt((0, 0), (Width, height), MfcDc, (0, 0), win32con.SRCCOPY)
        bmpinfo = Bitmap.GetInfo()
        bmpstr = Bitmap.GetBitmapBits(True)
        PILIMG = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr,
            'raw',
            'BGRX',
            0, 1
        )
        ImgBytes = io.BytesIO()
        PILIMG.save(ImgBytes, format='PNG')
        p = ImgBytes.getvalue()
        win32gui.DeleteObject(Bitmap.GetHandle())
        SaveDc.DeleteDC()
        MfcDc.DeleteDC()
        win32gui.ReleaseDC(HDesktop, HDC)
        return p