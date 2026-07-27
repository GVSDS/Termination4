import tkinter as tk
from tkinter import Canvas
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageDraw
import math

class DVDAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("DVD插入动画")
        
        # 设置窗口大小和居中
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 创建画布
        self.canvas = Canvas(root, width=window_width, height=window_height, bg='black')
        self.canvas.pack()
        
        # 图片尺寸
        self.dvd_player_width = 400
        self.dvd_player_height = 300
        self.dvd_width = 200
        self.dvd_height = 200
        self.icon_width = 100
        self.icon_height = 100
        
        # 位置参数
        self.dvd_player_x = (window_width - self.dvd_player_width) // 2
        self.dvd_player_y = (window_height - self.dvd_player_height) // 2
        
        # 创建占位符图片（实际使用时替换为您的图片）
        self.create_placeholder_images()
        
        # 加载图片
        self.load_images()
        
        # 动画参数
        self.animation_steps = 50
        self.current_step = 0
        self.dvd_start_x = window_width
        self.dvd_end_x = self.dvd_player_x + self.dvd_player_width // 2 - self.dvd_width // 2
        
        # 开始动画
        self.animate()
    
    def create_placeholder_images(self):
        """创建占位符图片（实际使用时删除此函数，直接加载您的图片）"""
        # 创建DVD机图片
        img1 = Image.new('RGBA', (self.dvd_player_width, self.dvd_player_height), (50, 50, 50, 255))
        draw1 = ImageDraw.Draw(img1)
        # 绘制DVD机外形
        draw1.rectangle([10, 10, self.dvd_player_width-10, self.dvd_player_height-10], 
                       outline=(100, 100, 100), width=3)
        # 绘制托盘
        draw1.ellipse([self.dvd_player_width//2-80, self.dvd_player_height//2-80,
                      self.dvd_player_width//2+80, self.dvd_player_height//2+80],
                     fill=(30, 30, 30), outline=(80, 80, 80))
        img1.save('1.png')
        
        # 创建DVD图片（带透明圆孔）
        img2 = Image.new('RGBA', (self.dvd_width, self.dvd_height), (0, 0, 0, 0))
        draw2 = ImageDraw.Draw(img2)
        # 绘制DVD外圈
        draw2.ellipse([10, 10, self.dvd_width-10, self.dvd_height-10], 
                     fill=(200, 200, 200), outline=(150, 150, 150))
        # 绘制DVD内圈（透明区域）
        draw2.ellipse([self.dvd_width//2-20, self.dvd_height//2-20,
                      self.dvd_width//2+20, self.dvd_height//2+20],
                     fill=(0, 0, 0, 0))
        img2.save('2.png')
        
        # 创建ICON图片
        img3 = Image.new('RGBA', (self.icon_width, self.icon_height), (0, 0, 0, 0))
        draw3 = ImageDraw.Draw(img3)
        # 绘制一个简单的图标
        draw3.ellipse([20, 20, self.icon_width-20, self.icon_height-20], 
                     fill=(255, 100, 100, 200))
        draw3.text((self.icon_width//2-15, self.icon_height//2-10), "DVD", 
                  fill=(255, 255, 255))
        img3.save('3.png')
    
    def load_images(self):
        """加载图片"""
        try:
            # 加载您的图片
            self.dvd_player_img = Image.open('1.png').resize((self.dvd_player_width, self.dvd_player_height), Image.Resampling.LANCZOS)
            self.dvd_img = Image.open('2.png').resize((self.dvd_width, self.dvd_height), Image.Resampling.LANCZOS)
            self.icon_img = Image.open('3.png').resize((self.icon_width, self.icon_height), Image.Resampling.LANCZOS)
        except FileNotFoundError:
            print("请将您的图片命名为1.png、2.png、3.png并放在同一目录下")
            self.root.destroy()
            return
        
        # 转换为Tkinter可用的格式
        self.dvd_player_photo = ImageTk.PhotoImage(self.dvd_player_img)
        self.dvd_photo = ImageTk.PhotoImage(self.dvd_img)
        self.icon_photo = ImageTk.PhotoImage(self.icon_img)
        
        # 创建叠加后的DVD图片
        self.create_combined_dvd_image()
    
    def create_combined_dvd_image(self):
        """创建DVD和ICON叠加的图片，保持透明度"""
        # 创建一个临时画布来叠加图片
        combined = Image.new('RGBA', (self.dvd_width, self.dvd_height), (0, 0, 0, 0))
        
        # 先放置DVD
        combined.paste(self.dvd_img, (0, 0), self.dvd_img)
        
        # 计算ICON的位置（居中）
        icon_x = (self.dvd_width - self.icon_width) // 2
        icon_y = (self.dvd_height - self.icon_height) // 2
        
        # 处理ICON的透明度，使其与DVD的透明区域匹配
        for x in range(self.icon_width):
            for y in range(self.icon_height):
                dvd_x = icon_x + x
                dvd_y = icon_y + y
                
                if 0 <= dvd_x < self.dvd_width and 0 <= dvd_y < self.dvd_height:
                    # 获取DVD对应位置的alpha值
                    dvd_alpha = self.dvd_img.getpixel((dvd_x, dvd_y))[3]
                    
                    if dvd_alpha > 0:  # 只在DVD不透明的区域绘制ICON
                        icon_pixel = self.icon_img.getpixel((x, y))
                        if icon_pixel[3] > 0:  # ICON也不透明
                            # 混合颜色
                            alpha_ratio = icon_pixel[3] / 255.0
                            new_r = int(icon_pixel[0] * alpha_ratio)
                            new_g = int(icon_pixel[1] * alpha_ratio)
                            new_b = int(icon_pixel[2] * alpha_ratio)
                            new_a = min(dvd_alpha, icon_pixel[3])
                            combined.putpixel((dvd_x, dvd_y), (new_r, new_g, new_b, new_a))
        
        self.combined_dvd_photo = ImageTk.PhotoImage(combined)
    
    def animate(self):
        """执行动画"""
        if self.current_step <= self.animation_steps:
            # 清除画布
            self.canvas.delete("all")
            
            # 计算当前DVD位置
            progress = self.current_step / self.animation_steps
            # 使用缓动函数使动画更平滑
            eased_progress = 1 - (1 - progress) ** 3
            current_x = self.dvd_start_x - (self.dvd_start_x - self.dvd_end_x) * eased_progress
            
            # DVD的Y位置（插入一半的效果）
            dvd_y = self.dvd_player_y + self.dvd_player_height // 2 - self.dvd_height // 2
            
            # 绘制DVD机（最高图层）
            self.canvas.create_image(self.dvd_player_x, self.dvd_player_y, 
                                   anchor=tk.NW, image=self.dvd_player_photo)
            
            # 绘制组合的DVD图片
            self.canvas.create_image(current_x, dvd_y, 
                                   anchor=tk.NW, image=self.combined_dvd_photo)
            
            # 更新动画步骤
            self.current_step += 1
            
            # 继续动画
            self.root.after(30, self.animate)
        else:
            # 动画完成，可以添加其他操作或重新开始
            self.canvas.after(2000, self.reset_animation)
    
    def reset_animation(self):
        """重置动画"""
        self.current_step = 0
        self.animate()

def main():
    root = ttk.Window(themename="darkly")
    app = DVDAnimation(root)
    root.mainloop()

if __name__ == "__main__":
    main()