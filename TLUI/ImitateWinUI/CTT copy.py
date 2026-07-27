import tkinter as tk
import WinUI3
import typing
import time
import os


if typing.TYPE_CHECKING:
    from . import WinUI3


class CTIP():
    def __init__(self):
        self.Width: int = 800
        self.Height: int = 230
        self.ProxyMainWindow = WinUI3.ProxyMainWindow()
        self.FullScreenOverlay: WinUI3.FullScreenOverlay = WinUI3.FullScreenOverlay(master = self.ProxyMainWindow)
        WinUI3.WUI3T.DisableWindowFocus(self.FullScreenOverlay.winfo_id())
        self.FullScreenOverlay.bind("<Button-3>", lambda x: os._exit(0))
        self.Tip: WinUI3.StandardWindow = WinUI3.StandardWindow(master = self.ProxyMainWindow, Width = self.Width, Height = self.Height)
        self.Tip.config(bg = WinUI3.THEME_WINDOWSBLUE["BackGround"])
        self.FullScreenOverlay.bind("<Button-1>", lambda x: self.Tip.tk.call("wm", "attributes", self.Tip, "-topmost", True))
        WinUI3.WUI3T.Setopmost(self.Tip)
        tk.Label(
            self.Tip,
            text="Windows 终止了你的安全许可",
            font=("微软雅黑", 24),
            bg=WinUI3.THEME_WINDOWSBLUE["BackGround"],
            fg="white",
            anchor="w"
        ).pack(pady=(20, 5), padx=20, fill="x")
        tk.Label(
            self.Tip,
            text="""
由于设备的违法调整，Windows 即日起终止你的安全许可，你将无法继续本产品，请尝试联系设备管理
员并更换本产品。""",
            font=("微软雅黑", 12),
            bg=WinUI3.THEME_WINDOWSBLUE["BackGround"],
            fg="white",
            anchor="w",
            justify="left"
        ).pack(pady=(0, 0), padx=20, fill="x")
        self.CloseBtn: WinUI3.DirectUIButton = WinUI3.DirectUIButton(
            self.Tip,
            text="关闭",
            command = self.Close
        )
        self.CloseBtn.place(x=self.Width-120-10, y=self.Height-50-10, height=35)
        self.CloseBtn.destroy()
        self.Tip.mainloop()
        self.FullScreenOverlay.mainloop()
        self.ProxyMainWindow.mainloop()
    def Close(self, event: tk.Event | None = None):
        for i in range(100, 0, -1):
            self.Tip.tk.call("wm", "attributes", self.Tip, "-alpha", i/100)
            self.Tip.update()
            time.sleep(0.0001)
        self.Tip.destroy()
        self.FullScreenOverlay.destroy()
        self.ProxyMainWindow.destroy()

if __name__ == "__main__":
    _ = CTIP()
