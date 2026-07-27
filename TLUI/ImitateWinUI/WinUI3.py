import threading
import win32gui
import win32con
import tkinter
import typing
import ctypes
import time


GWL_STYLE = -16
GWL_EXSTYLE = -20
WS_SYSMENU = 0x00080000
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000
SWP_FLAGS = 0x0020 | 0x0002 | 0x0001  # SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE

class WUI3T:
    @staticmethod
    def InterpolateColor(StartColor: str, EndColor: str, Steps: int):
        if StartColor[0] == "#": StartColor = StartColor[1:]
        if EndColor[0] == "#": EndColor = EndColor[1:]
        if len(StartColor) == 3: StartColor = StartColor * 2
        if len(EndColor) == 3: EndColor = EndColor * 2
        StartR, StartG, StartB = int(StartColor[:2], 16), int(StartColor[2:4], 16), int(StartColor[4:], 16)
        EndR, EndG, EndB = int(EndColor[:2], 16), int(EndColor[2:4], 16), int(EndColor[4:], 16)
        StepR, StepG, StepB = (EndR - StartR) / Steps, (EndG - StartG) / Steps, (EndB - StartB) / Steps
        Colors: list[str] = []
        for i in range(Steps + 1):
            Colors.append(f"#{int(StartR + i * StepR):02x}{int(StartG + i * StepG):02x}{int(StartB + i * StepB):02x}")
        return Colors
    @staticmethod
    def CenterWindow(Root: tkinter.Widget | tkinter.Tk | tkinter.Toplevel, Width: float | int, Height: float | int, OffsetWidth: float | int, OffsetHeight: float | int):
        ScreenWidth: float | int = Root.winfo_screenwidth()
        ScreenHeight: float | int = Root.winfo_screenheight()
        X: float | int = (ScreenWidth - Width) // 2
        Y: float | int = (ScreenHeight - Height) // 2
        Root.tk.call("wm", "geometry", Root, f"{Width}x{Height}+{X+OffsetWidth}+{Y+OffsetHeight}")
    @staticmethod
    def SetParent(Child: tkinter.Widget, Parent: tkinter.Widget):
        win32gui.SetParent(Child.winfo_id(), Parent.winfo_id())
    @staticmethod
    def Setopmost(Root: tkinter.Widget | tkinter.Tk | tkinter.Toplevel):
        def _():
            while Root.winfo_exists():
                Root.tk.call("wm", "attributes", Root, "-topmost", True)
                time.sleep(1)
        threading.Thread(target = _, daemon = True).start()
    @staticmethod
    def DisableWindowFocus(HWND: int):
        win32gui.SetWindowLong(HWND, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(HWND, win32con.GWL_EXSTYLE) | win32con.WS_EX_NOACTIVATE)
    @staticmethod
    def GetWindowHandle(Root: tkinter.Widget | tkinter.Tk | tkinter.Toplevel):
        return ctypes.windll.user32.GetParent(Root.winfo_id())
    @staticmethod
    def RefreshWindowStyle(HWND: int):
        ctypes.windll.user32.SetWindowPos(HWND, 0, 0, 0, 0, 0, SWP_FLAGS)
    @staticmethod
    def RemoveSystemMenu(HWND: int):
        Style = ctypes.windll.user32.GetWindowLongPtrW(HWND, GWL_STYLE)
        Style &= ~WS_SYSMENU
        ctypes.windll.user32.SetWindowLongPtrW(HWND, GWL_STYLE, Style)
    @staticmethod
    def RemoveFromTaskbar(HWND: int):
        Style = ctypes.windll.user32.GetWindowLongPtrW(HWND, GWL_STYLE)
        Style &= ~WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongPtrW(HWND, GWL_STYLE, Style)
    @staticmethod
    def RemoveFocus(HWND: int):
        Style = ctypes.windll.user32.GetWindowLongPtrW(HWND, GWL_EXSTYLE)
        Style |= WS_EX_NOACTIVATE
        ctypes.windll.user32.SetWindowLongPtrW(HWND, GWL_EXSTYLE, Style)





THEME_WINDOWSBLUE = {
    "BackGround": "#0078D4",
    "BackGround_White": "#1F88FF",
}
THEME_CLASSIC_WINDOWSBLUE = {
    "BackGround": "#0070d5",
    "BackGround_White": "#0f8fee",
}

class DirectUIButton(tkinter.Label):
    def __init__(self, master: tkinter.Widget | tkinter.Tk | tkinter.Toplevel, command: typing.Callable[[tkinter.Event | None], None] = lambda event: None, **kwargs: typing.Any):
        super().__init__(master, **kwargs, bg=THEME_WINDOWSBLUE["BackGround"], fg="white", relief="flat", highlightbackground="#FFF", highlightcolor="#FFF", highlightthickness=2, width=9, font=("微软雅黑", 12))
        self.Pressed = False
        self.command = command
        self.bind("<Enter>", self.OnEnter)
        self.bind("<Leave>", self.OnLeave)
        self.bind("<ButtonPress-1>", self.ButtonPress)
        self.bind("<ButtonRelease-1>", self.ButtonRelease)
    def OnEnter(self, event: tkinter.Event | None = None):
        Colors = WUI3T.InterpolateColor(THEME_WINDOWSBLUE["BackGround"], THEME_WINDOWSBLUE["BackGround_White"], 10)
        for i in range(10):
            self.config(bg=Colors[i])
            self.master.update()
            time.sleep(0.005)
    def OnLeave(self, event: tkinter.Event | None = None):
        Colors = WUI3T.InterpolateColor(THEME_WINDOWSBLUE["BackGround_White"], THEME_WINDOWSBLUE["BackGround"], 10)
        self.config(fg="#FFF")
        for i in range(10):
            self.config(bg=Colors[i])
            self.master.update()
            time.sleep(0.005)
    def ButtonPress(self, event: tkinter.Event | None = None):
        self.Pressed = True
        self.config(bg="#FFF")
        self.config(fg="#000")
    def ButtonRelease(self, event: tkinter.Event | None = None):
        self.config(bg=THEME_WINDOWSBLUE["BackGround"])
        self.config(fg="#FFF")
        if self.Pressed: self.command(event)
        self.Pressed = False

class ProxyMainWindow(tkinter.Tk):
    def __init__(self, *args: typing.Any, **kwargs: typing.Any):
        super().__init__()
        self.overrideredirect(True)
        self.withdraw()

class StandardWindow(tkinter.Toplevel):
    def __init__(self, master: tkinter.Tk | tkinter.Toplevel | None = None, Width: float | int = 800, Height: float | int = 200, OffsetWidth: float | int = 0, OffsetHeight: float | int = 0):
        super().__init__(master = master)
        WUI3T.CenterWindow(self, Width, Height, OffsetWidth, OffsetHeight)

class FullScreenOverlay(StandardWindow):
    def __init__(self, master: tkinter.Tk | tkinter.Toplevel | StandardWindow | None = None, alpha: float | int = 0.5):
        super().__init__(master = master)
        self.configure(bg = "#000")
        self.tk.call("wm", "attributes", self, "-alpha", alpha)
        self.tk.call("wm", "attributes", self, "-topmost", True)
        self.state("zoomed")
        self.overrideredirect(True)
        self.tk.call("raise", self)

def SpaceLabel(master: tkinter.Widget | tkinter.Tk | tkinter.Toplevel, text: str = " ", bg = "#FFF", size = 15):
        tkinter.Label(master, text = text, bg = bg, font = ("微软雅黑", size)).pack()
