from PIL import Image, ImageTk
import tkinter as tk
import WinUI3
import typing
import time
import os


if typing.TYPE_CHECKING:
    from . import WinUI3


class CTIP():
    def __init__(self):
        self.Width: int = 600
        self.Height: int = 300
        self.ProxyMainWindow = WinUI3.ProxyMainWindow()
        self.Tip: WinUI3.StandardWindow = WinUI3.StandardWindow(master = self.ProxyMainWindow, Width = self.Width, Height = self.Height)
        self.Tip.title("Termination 4.2.0 Work Procedure Static GUI (Enterprise: GVSDS) (PIC: Veyra)")
        self.Tip.config(bg = "#FFF")
        WinUI3.WUI3T.Setopmost(self.Tip)
        self.Tip.update_idletasks()
        FSOHAND: int = WinUI3.WUI3T.GetWindowHandle(self.Tip)
        WinUI3.WUI3T.RemoveSystemMenu(FSOHAND)
        WinUI3.WUI3T.RemoveFromTaskbar(FSOHAND)
        WinUI3.WUI3T.RefreshWindowStyle(FSOHAND)

        WinUI3.SpaceLabel(self.Tip, size = 20)

        self.GVSDSPNG = Image.open("./static/GVSDS.png").resize([self.Width // 2, self.Height // 2 + 20])
        self.GVSDSPNGTk = ImageTk.PhotoImage(self.GVSDSPNG)
        self.GVSDSLABLE = tk.Label(self.Tip, image = self.GVSDSPNGTk, bg = "#FFF")
        self.GVSDSLABLE.pack()

        self.Bottom = tk.Frame(self.Tip, bg = "#FAFAFA")
        self.Bottom.pack(side = tk.BOTTOM, fill = tk.X)

        self.Working = tk.Label(self.Bottom, text="正在加载核心组件...     - C:\\Test\\A.dll", bg = "#FAFAFA")
        self.Working.pack(side = tk.LEFT, padx = 10, pady = 10)

        self.Progress = tk.Label(self.Bottom, text="进度：57%... (1/6)", bg = "#FAFAFA")
        self.Progress.pack(side = tk.RIGHT, padx = 10, pady = 10)

        self.ProxyMainWindow.mainloop()
    def Close(self, event: tk.Event | None = None):
        for i in range(100, 0, -1):
            self.Tip.tk.call("wm", "attributes", self.Tip, "-alpha", i/100)
            self.Tip.update()
            time.sleep(0.0001)
        self.Tip.destroy()
        self.ProxyMainWindow.destroy()

if __name__ == "__main__":
    _ = CTIP()
