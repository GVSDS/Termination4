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

        self.draw()

    @asyncs
    def draw(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()


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

        original_image = Image.open("./glasses1.png")
        self.label_img1 = tk.Label(self, bg="black", bd=0)

        original_image2 = Image.open("./glasses2.png")
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
        
        time.sleep(0.5)

        for step in range(100):
            factor = (1 - math.cos(math.pi * step / 100)) / 2
            offset_y = int(70 * factor)
            self.label_img1.place(x=self.start_x_img1, y=self.start_y_img1 - 79 - offset_y)
            self.label_img2.place(x=self.start_x_img1, y=self.start_y_img1 + offset_y)
            self.update()
            time.sleep(0.003)

        current_color=0
        while current_color <= 255:
            r = g = b = current_color
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.label.config(fg=color)
            current_color += 10
            self.update()
            time.sleep(0.001)

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
            time.sleep(0.002)
        self.label_img1.destroy()
        self.label_img2.destroy()


        self.animation_step = 0
        self.max_animation_steps = 100
        self.move_distance = 70

        for step in range(100):
            factor = (1 - math.cos(math.pi * step / 100)) / 2
            offset_y = int(70 * factor)
            new_y = self.start_y - offset_y
            self.label.place(x=self.start_x, y=new_y)
            self.update()
            time.sleep(0.004)




if __name__ == "__main__":
    app = GradientAndMoveApp()
    app.mainloop()