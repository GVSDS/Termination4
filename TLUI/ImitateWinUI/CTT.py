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
        self.Height: int = 400
        self.ProxyMainWindow = WinUI3.ProxyMainWindow()
        self.FullScreenOverlay: WinUI3.FullScreenOverlay = WinUI3.FullScreenOverlay(master = self.ProxyMainWindow)
        FSOHAND: int = WinUI3.WUI3T.GetWindowHandle(self.FullScreenOverlay)
        WinUI3.WUI3T.RemoveFocus(FSOHAND)
        WinUI3.WUI3T.DisableWindowFocus(self.FullScreenOverlay.winfo_id())
        WinUI3.WUI3T.RefreshWindowStyle(FSOHAND)
        self.FullScreenOverlay.bind("<Button-3>", lambda x: os._exit(0))
        self.Tip: WinUI3.StandardWindow = WinUI3.StandardWindow(master = self.ProxyMainWindow, Width = self.Width, Height = self.Height)
        self.Tip.overrideredirect(True)
        self.Tip.config(bg = WinUI3.THEME_WINDOWSBLUE["BackGround"])
        self.FullScreenOverlay.bind("<Button-1>", lambda x: self.Tip.tk.call("wm", "attributes", self.Tip, "-topmost", True))
        WinUI3.WUI3T.Setopmost(self.Tip)
        tk.Label(
            self.Tip,
            text="九州同庆，四海欢歌",
            font=("微软雅黑", 24),
            bg=WinUI3.THEME_WINDOWSBLUE["BackGround"],
            fg="white",
            anchor="w"
        ).pack(pady=(20, 5), padx=20, fill="x")
        tk.Label(
            self.Tip,
            text="""
值此中华人民共和国国庆节来临之际，我们向广大用户、合作伙伴及社会各界致以诚挚的节日祝福！技术
的价值在于赋能每一个人、每一个组织。过去，我们始终以全球技术创新贴合中国市场需求，与大家携手
推进数字化转型；国庆既是共庆收获的时刻，也是蓄力前行的起点。

面向个人与家庭，Microsoft 365 是效率与创造力的好帮手：借助 Copilot 副驾驶 ®，Word、Excel、
PowerPoint 能快速生成内容、优化成果，OneDrive 云端存储支持多设备协作，家庭版还可多人共享，
让假期事务处理更灵活。

未来，我们以更优产品与服务陪伴大家探索机遇。再次祝愿大家国庆假期愉快，阖家幸福！""",
            font=("微软雅黑", 12),
            bg=WinUI3.THEME_WINDOWSBLUE["BackGround"],
            fg="white",
            anchor="w",
            justify="left"
        ).pack(pady=(0, 0), padx=20, fill="x")
        self.CloseBtn = WinUI3.DirectUIButton(
            self.Tip,
            text="关闭",
            command = self.Close
        ).place(x=self.Width-120-10, y=self.Height-50-10, height=35)
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
