from PIL import Image, ImageTk, ImageEnhance
import tkinter as tk
import threading
import tkinter.font as font
import math
import time
import os

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

class GradientAndMoveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.configure(bg="black")
        self.bind("<Button-1>", lambda X: os._exit(0))
        self.labels=[]


        self.draw()

    @asyncs
    def nlabel(self, text):
        new_label = tk.Label(self, text=text, bg="black", fg="white", font=("System", 10))
        new_label.pack(anchor="nw")
        new_label.update()
        self.labels.append(new_label)
        window_height = self.winfo_height()
        last_label_y = new_label.winfo_y()
        last_label_height = new_label.winfo_height()
        if last_label_y + last_label_height >= window_height:
            for label in self.labels:
                label.destroy()
            self.labels = []

    @asyncs
    def l(self):
        with open("./nt.log", "r", encoding="UTF-8") as f:
            for i in f.read().split("\n"):
                self.nlabel(i)
                time.sleep(0.003)
        for label in self.labels:
            label.destroy()
        self.labels = []

    @asyncs
    def draw(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.l()

        time.sleep(2)

        #Lucida Calligraphy

        self.label2 = tk.Label(self, text="Version : 4.1.0", bg="black", fg="#FFF", font=("Lucida Calligraphy", 20))
        self.label = tk.Label(self, text="Termination", bg="black", fg="#000", font=("Lucida Calligraphy", 48))

        label_width = self.label.winfo_reqwidth()
        label_height = self.label.winfo_reqheight()
        self.start_x = (screen_width - label_width) // 2
        self.start_y = (screen_height - label_height) // 2 - 40

        label_width2 = self.label2.winfo_reqwidth()
        label_height2 = self.label2.winfo_reqheight()
        self.start_x2 = (screen_width - label_width2) // 2
        self.start_y2 = (screen_height - label_height2) // 2 - 40

        self.label2.place(x=self.start_x2, y=self.start_y2)
        self.label.place(x=self.start_x, y=self.start_y)

        #time.sleep(1)

        original_image = Image.open("./.theme/GLASSES/glasses1.png")
        self.label_img1 = tk.Label(self, bg="black", bd=0)

        original_image2 = Image.open("./.theme/GLASSES/glasses2.png")
        self.label_img2 = tk.Label(self, bg="black", bd=0)

        self.start_x_img1 = (screen_width - original_image.width) // 2
        self.start_y_img1 = (screen_height - original_image.height) // 2

        self.label_img1.place(x=self.start_x_img1, y=self.start_y_img1-79)
        self.label_img2.place(x=self.start_x_img1, y=self.start_y_img1)

        for brightness_level in range(0, 120, 1):
            brightness_factor = brightness_level / 100
            enhancer = ImageEnhance.Brightness(original_image)
            brightened_image = enhancer.enhance(brightness_factor)
            tk_image = ImageTk.PhotoImage(brightened_image)
            self.label_img1.config(image=tk_image)
            self.label_img1.image = tk_image

            enhancer2 = ImageEnhance.Brightness(original_image2)
            brightened_image2 = enhancer2.enhance(brightness_factor)
            tk_image2 = ImageTk.PhotoImage(brightened_image2)
            self.label_img2.config(image=tk_image2)
            self.label_img2.image = tk_image2
            self.update()
            time.sleep(0.002)

        b=0
        for _ in range(2*2):
            enhancer = ImageEnhance.Brightness(original_image)
            brightened_image = enhancer.enhance(b)
            tk_image = ImageTk.PhotoImage(brightened_image)
            self.label_img1.config(image=tk_image)
            self.label_img1.image = tk_image

            enhancer2 = ImageEnhance.Brightness(original_image2)
            brightened_image2 = enhancer2.enhance(b)
            tk_image2 = ImageTk.PhotoImage(brightened_image2)
            self.label_img2.config(image=tk_image2)
            self.label_img2.image = tk_image2
            self.update()
            b=1 if not b else 0
            time.sleep(0.05)

        for step in range(100):
            factor = (1 - math.cos(math.pi * step / 70)) / 2
            offset_y_img = int(70 * factor)
            self.label_img1.place(x=self.start_x_img1, y=self.start_y_img1 - 79 - offset_y_img)
            self.label_img2.place(x=self.start_x_img1, y=self.start_y_img1 + offset_y_img)
            self.update()
            time.sleep(0.003)

        for i in range(0, 255+1):
            r = g = b = i
            self.label.config(fg=f"#{r:02x}{g:02x}{b:02x}")
            self.update()
            time.sleep(0.005)

        for brightness_level in range(120, -1, -1):
            brightness_factor = brightness_level / 100
            enhancer = ImageEnhance.Brightness(original_image)
            brightened_image = enhancer.enhance(brightness_factor)
            tk_image = ImageTk.PhotoImage(brightened_image)
            self.label_img1.config(image=tk_image)
            self.label_img1.image = tk_image

            enhancer2 = ImageEnhance.Brightness(original_image2)
            brightened_image2 = enhancer2.enhance(brightness_factor)
            tk_image = ImageTk.PhotoImage(brightened_image2)
            self.label_img2.config(image=tk_image)
            self.label_img2.image = tk_image
            self.update()
            time.sleep(0.001)

        self.label_img1.place_forget()
        self.label_img2.place_forget()

        time.sleep(0.5)

        for step in range(100):
            factor = (1 - math.cos(math.pi * step / 80)) / 2
            offset_y = int(70 * factor)
            new_y = self.start_y - offset_y
            self.label.place(x=self.start_x, y=new_y)
            self.update()
            if step > 70:
                time.sleep(0.005)
            time.sleep(0.002)
        
        time.sleep(3)

        for step2 in range(100):
            factor2 = (1 - math.cos(math.pi * step2 / 80)) / 2
            offset_y2 = int(70 * factor2)
            new_y2 = self.start_y - offset_y + offset_y2
            self.label.place(x=self.start_x, y=new_y2)
            self.update()
            if step2 > 70:
                time.sleep(0.005)
            time.sleep(0.002)
        self.label2.place_forget()

        time.sleep(1)

        self.label_img1.place(x=self.start_x_img1, y=self.start_y_img1-79-offset_y_img)
        self.label_img2.place(x=self.start_x_img1, y=self.start_y_img1+offset_y_img)

        for brightness_level in range(0, 120+1):
            brightness_factor = brightness_level / 100
            enhancer = ImageEnhance.Brightness(original_image)
            brightened_image = enhancer.enhance(brightness_factor)
            tk_image = ImageTk.PhotoImage(brightened_image)
            self.label_img1.config(image=tk_image)
            self.label_img1.image = tk_image

            enhancer2 = ImageEnhance.Brightness(original_image2)
            brightened_image2 = enhancer2.enhance(brightness_factor)
            tk_image = ImageTk.PhotoImage(brightened_image2)
            self.label_img2.config(image=tk_image)
            self.label_img2.image = tk_image
            self.update()
            time.sleep(0.001)


        for i in range(255, 0-1, -1):
            r = g = b = i
            self.label.config(fg=f"#{r:02x}{g:02x}{b:02x}")
            self.update()
            time.sleep(0.002)

        """for step in range(100):
            factor = (1 - math.cos(math.pi * step / 70)) / 2
            offset_y_img2 = int(70 * factor)
            self.label_img1.place(x=self.start_x_img1, y=self.start_y_img1 - 79 - offset_y_img + offset_y_img2)
            self.label_img2.place(x=self.start_x_img1, y=self.start_y_img1 + offset_y_img - offset_y_img2)
            self.update()
            time.sleep(0.003)"""

        for step in range(100):
            factor = (1 - math.cos(math.pi * step / 70)) / 2
            offset_y_img2 = int(70 * factor)
            self.label_img1.place(x=self.start_x_img1, y=self.start_y_img1 - 79 - offset_y_img + offset_y_img2)
            self.label_img2.place(x=self.start_x_img1, y=self.start_y_img1 + offset_y_img - offset_y_img2)
            if offset_y_img2 >= 44:
                break
            self.update()
            time.sleep(0.003)

        time.sleep(2)

        for brightness_level in range(120, -1, -1):
            brightness_factor = brightness_level / 100
            enhancer = ImageEnhance.Brightness(original_image)
            brightened_image = enhancer.enhance(brightness_factor)
            tk_image = ImageTk.PhotoImage(brightened_image)
            self.label_img1.config(image=tk_image)
            self.label_img1.image = tk_image

            enhancer2 = ImageEnhance.Brightness(original_image2)
            brightened_image2 = enhancer2.enhance(brightness_factor)
            tk_image = ImageTk.PhotoImage(brightened_image2)
            self.label_img2.config(image=tk_image)
            self.label_img2.image = tk_image
            self.update()
            time.sleep(0.001)


        #self.label.destroy()
        #self.label2.destroy()






if __name__ == "__main__":
    app = GradientAndMoveApp()
    app.mainloop()