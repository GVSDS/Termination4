if __name__ == "__main__":
    import UI_Hardcoded
    import ctypes
    import tkinter
    import io
    from PIL import Image, ImageTk
    import win32api
    import base64
    import random
    import time
    import os
    import playsound3 as playsound
else:
    from TLib.T_imports import *
    from . import UI_Hardcoded



class Tool:
    def __init__(self):
        pass

    def PlaySound(self, soundPath):
        self.WinMM = ctypes.WinDLL('winmm.dll')
        self.WinMM.sndPlaySoundW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint]
        self.WinMM.sndPlaySoundW.restype = ctypes.c_int
        success = self.WinMM.sndPlaySoundW(soundPath, 0x0001 | 0x00020000)
        return success

    @staticmethod
    def InstallFont(fontPath):
        ctypes.windll.gdi32.AddFontResourceExW(fontPath, 0x10, 0)

def hide_cursor():
    while ctypes.windll.user32.ShowCursor(False) >= 0: pass

def show_cursor():
    while ctypes.windll.user32.ShowCursor(True) < 0: pass


class BlueScreenApp:
    def __init__(self, fontPath, soundPath, callback=None):
        hide_cursor()
        ctypes.windll.user32.BlockInput(True)
        self.FontPath = fontPath
        self.SoundPath = soundPath
        self.Callback = callback
        self.ProgressPercentage = 1
        self.YPosition = 0
        self.LineIndex = 0
        
        Tool.InstallFont(self.FontPath)
        self.Tool = Tool()

        self.Root = tkinter.Tk()
        self.Root.attributes('-transparentcolor','#f0f0f0')
        self.Root.title('Windows')
        self.Root.overrideredirect(True)
        self.Root.wm_attributes('-topmost', 1)
        self.Root.state("zoomed")
        self.Root.bind("<Key>", self.HandleKeyPress)
        self.Root.protocol("WM_DELETE_WINDOW", lambda: None)

        self.Sentences = UI_Hardcoded.Sentence
    def SetupCanvas(self):
        self.Canvas.config(bg="#0078D7")
        leftPadding = self.Root.winfo_screenwidth() * 0.1
        faceX = leftPadding + 200
        faceY = self.Root.winfo_screenheight() * 0.2
        self.FaceSize = 110
        # 创建表情符号
        self.Face1 = self.Canvas.create_text(
            faceX, faceY, text=":", 
            font=("微软雅黑", int(self.FaceSize)), 
            fill='white', anchor=tkinter.NW
        )
        self.Face2 = self.Canvas.create_text(
            faceX + 50, faceY + 10, text="(", 
            font=("微软雅黑", int(self.FaceSize)), 
            fill='white', anchor=tkinter.NW
        )
        # 创建大段文字
        bigTextX = faceX
        bigTextY = faceY + self.FaceSize * 2
        self.BigText = self.Canvas.create_text(
            bigTextX, bigTextY, anchor=tkinter.NW,
            font=("微软雅黑", 25), fill='white',
            width=self.Root.winfo_screenwidth() * 0.9
        )
        # 创建QR码
        qrX = faceX + self.FaceSize * 0.2
        qrY = bigTextY + self.Root.winfo_screenheight() * 0.2
        photo1 = base64.b64decode(UI_Hardcoded.QR)
        dataStream = io.BytesIO(photo1)
        self.pilImage = Image.open(dataStream)
        self.photo = self.pilImage.resize((110, 110))
        self.QrImage = ImageTk.PhotoImage(self.photo)
        self.QrCode = self.Canvas.create_image(qrX, qrY, image=self.QrImage, anchor=tkinter.NW)
        # 创建小段文字
        smallTextX = qrX + 200
        smallTextY = qrY
        self.SmallText = self.Canvas.create_text(
            smallTextX, smallTextY, anchor=tkinter.NW,
            font=("微软雅黑", 15), fill='white',
            width=self.Root.winfo_screenwidth() * 0.5
        )
        self.DisplayInitialText()
    def DisplayInitialText(self):
        self.Canvas.itemconfig(self.BigText,
            text="你的电脑遇到问题，需要重新启动。\n我们只收集某些错误信息，然后为你重新启动。\n0%完成")
        self.Canvas.itemconfig(self.SmallText,
            text="有关此问题的详细信息和可能的解决方法，请访问 http://windows/stopcode\n如果致电支持人员，请向他们提供一下信息\n终止代码：SYSTEM_SERVICE_EXCEPTION")
    def DisplayAlternateText(self):
        self.Canvas.itemconfig(self.BigText,
            text="你的电脑遇到问题，需要重新启动。\n我们不只收集某些错误信息，还有一些其它信息，然后可能会重新启动。\n0%完成")
        self.Canvas.itemconfig(self.SmallText,
            text="有关此问题的详细信息和可能的解决方法，请访问 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n如果致电GVS人员，请向他们提供一下信息\n终止代码：TERMINATION_BLUE_EXCEPTION")
    def HandleKeyPress(self, event):
        if event.keycode == 27:
            self.Root.destroy()
    def ChangeToRedTheme(self):
        self.Canvas.config(bg="#000")
        self.Canvas.itemconfig(self.Face1, fill="red", font=("ipix_12px", int(self.FaceSize)))
        self.Canvas.itemconfig(self.Face2, fill="red", font=("ipix_12px", int(self.FaceSize)))
        self.Canvas.move(self.Face2, 30, 0)
        self.Canvas.itemconfig(self.BigText, fill="red", font=("ipix_12px", 25))
        self.Canvas.itemconfig(self.SmallText, fill="red", font=("ipix_12px", 15))
        self.Canvas.itemconfig(self.QrCode, image="")
        self.Root.update()
    def ShowTextAnimation(self):
        if self.LineIndex < 2 or self.LineIndex > 30:
            text = "HA " * 50
        else:
            text = "".join(random.choice(self.Sentences) for _ in range(5))
        self.Canvas.create_text(
            10, self.YPosition, text=text, 
            fill="red", font=("ipix_12px", 30), 
            anchor=tkinter.NW
        )
        self.YPosition += 30
        self.LineIndex += 1
        if self.LineIndex > self.Canvas.winfo_height() // 15:
            self.Canvas.delete("all")
            self.SetupCanvas()
            self.ChangeToRedTheme()
            self.YPosition = 0
            self.LineIndex = 0
        self.Root.after(1, self.ShowTextAnimation)
    def Animation3(self):
        self.ChangeToRedTheme()
        playsound.playsound(self.SoundPath)
        self.Root.after(3500, self.ShowTextAnimation)
        self.Root.after(3500+16500, self.EndProgram)

    def DrawLine(self, x1, y1, x2, y2, color):
        self.Canvas.create_line(x1, y1, x2, y2, fill=color)
    def Animation2(self):
        self.Canvas = tkinter.Canvas(self.Root, highlightthickness=0)
        self.Canvas.pack(fill=tkinter.BOTH, expand=True)
        sw=self.Root.winfo_screenwidth()
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
        self.Root.update()
        time.sleep(3)
        self.Root.attributes('-transparentcolor','#f0f0f0')
        self.Canvas.delete("all")
        self.SetupCanvas()
        self.Root.after(5000, self.Animation3)

    def Animation1(self):
        self.A1Frame = tkinter.Frame(self.Root, bd=0)
        self.A1Frame.pack(fill=tkinter.BOTH, expand=True)
        self.Root.update()
        def Text(text, fg="#FFF", bg="#000"):
            tkinter.Label(self.A1Frame, text=text,fg=fg,bg=bg,font=("ipix_12px",15)).pack(anchor="sw")
        def FText():
            tkinter.Label(self.A1Frame, text="").pack(anchor="sw")
        Text("Please contact the Voodoo Kernel Dev-Team with a photo of the Information printed below,")
        Text("Along With a description of your system configuration and what you were doing at the time that")
        Text("the kernel panic occurred. We appologize for the lnconvenience")
        FText()
        self.Root.update()
        time.sleep(1)
        Text('Panic(CPU 0 Caller 0x001AC05E): "Windows Teacher Error"')
        Text("Debugger Called: <Panic>")
        Text("Backtrace (CPU 0),Frame : Return Address (4 potential ponies on stack)")
        self.Root.update()
        time.sleep(0.2)
        Text("0x14e1ffce68 : 0x12b08c (0xfffffffff 0xfffffffff 0xfffffffff)")
        Text("0x14e1ffce69 : 0x12b07c (0xfffffffff 0xfffffffff 0xfffffffff)")
        Text("0x14e1ffce70 : 0x12b05c (0xfffffffff 0xfffffffff 0xfffffffff)")
        Text("0x14e1ffce23 : 0x12b0cc (0xfffffffff 0xfffffffff 0xfffffffff)")
        Text("0x14e1ffcf35 : 0x12b0fc (0xfffffffff 0xfffffffff 0xfffffffff)")
        Text("0x14e1ffcf90 : 0x12b0ac (0xfffffffff 0xfffffffff 0xfffffffff)")
        self.Root.update()
        time.sleep(0.2)
        Text("Backtrace terminated-invalid frame pointer 0")
        FText()
        Text("BSD process name corresponding to current thread: Unknown")
        FText()
        self.Root.update()
        time.sleep(1)
        Text("Windows version:")
        Text("Win 32/Run")
        FText()
        Text("Kernel version:")
        Text("Win32 Kernel V3.2.5 / EFI Boot System V7")
        FText()
        self.Root.update()
        time.sleep(1)
        Text("Try automatic repair...")
        self.Root.update()
        time.sleep(1)
        Text("0x14e1ffce61 : 0x12b08c (0xfffffffff 0xfffffffff 0xfffffffff)")
        Text("0x14e1ffce62 : 0x12b07c (0xfffffffff 0xfffffffff 0xfffffffff)")
        FText()
        self.Root.update()
        time.sleep(1)
        Text("WARNING", "yellow", "red")
        Text("We now advise you to understand that by stopping the operation of your computer,", "yellow", "red")
        Text("your computer is suspected to be infected with a virus that modifies the BIOS,", "yellow", "red")
        Text("as we have an error while verifying the BIOS file, therefore,", "yellow", "red")
        Text("please shut down this computer immediately, otherwise,", "yellow", "red")
        Text("the manufacturer should not be responsible for any consequences", "yellow", "red")
        self.Root.update()
        time.sleep(3)
        self.A1Frame.destroy()
        self.Root.after(1, self.Animation2)

    def EndProgram(self):
        if self.Callback:
            self.Callback()
        self.Root.withdraw()
        self.Root.destroy()
        show_cursor()
        win32api.ShowCursor(True)

    def Run(self):
        self.Root.update()
        self.Root.after(1, self.Animation1)
        self.Root.mainloop()


if __name__ == "__main__":
    BlueScreenApp("./System.ttf", "./HA.mp3", lambda: os.system("")).Run()