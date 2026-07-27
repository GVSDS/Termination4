import tkinter as tk
from tkinter import ttk
import platform

class RoundedLabel(tk.Label):
    def __init__(self, master=None, text="", bg="white", fg="black", 
                 corner_radius=10, border_width=0, border_color=None,** kwargs):
        # 初始化父类
        super().__init__(master, text=text, bg=bg, fg=fg, bd=0, 
                         highlightthickness=0, **kwargs)
        
        # 圆角相关参数
        self.corner_radius = corner_radius
        self.border_width = border_width
        self.border_color = border_color if border_color else fg
        
        # 绑定事件以触发重绘
        self.bind("<Configure>", self._on_configure)
        
        # 初始绘制
        self._draw_rounded_bg()
    
    def _on_configure(self, event=None):
        # 当控件大小改变时重绘
        self._draw_rounded_bg()
    
    def _draw_rounded_bg(self):
        # 获取控件大小
        width = self.winfo_width()
        height = self.winfo_height()
        
        # 确保控件已渲染
        if width <= 1 or height <= 1:
            self.after(10, self._draw_rounded_bg)
            return
        
        # 创建用于绘制的图像
        self._image = tk.PhotoImage(width=width, height=height)
        self.configure(image=self._image)
        
        # 获取绘制上下文
        draw = self._image.tk.call(self._image, "cget", "-draw")
        
        # 绘制圆角背景
        bg = self["bg"]
        radius = self.corner_radius
        
        # 确保圆角半径不会超过控件尺寸的一半
        max_radius = min(width, height) // 2
        radius = min(radius, max_radius)
        
        # 绘制背景圆角矩形
        self._image.tk.call(
            "image", "draw", self._image,
            "-fill", bg,
            "-roundedrect", 0, 0, width-1, height-1, radius
        )
        
        # 绘制边框（如果需要）
        if self.border_width > 0:
            self._image.tk.call(
                "image", "draw", self._image,
                "-stroke", self.border_color,
                "-width", self.border_width,
                "-roundedrect", 
                self.border_width//2, 
                self.border_width//2, 
                width-1 - self.border_width//2, 
                height-1 - self.border_width//2, 
                radius - self.border_width//2
            )
    
    def configure(self, cnf=None,** kwargs):
        # 重写配置方法以更新外观
        update = False
        if "bg" in kwargs or "background" in kwargs:
            update = True
        if "corner_radius" in kwargs:
            self.corner_radius = kwargs.pop("corner_radius")
            update = True
        if "border_width" in kwargs:
            self.border_width = kwargs.pop("border_width")
            update = True
        if "border_color" in kwargs:
            self.border_color = kwargs.pop("border_color")
            update = True
            
        # 调用父类配置方法
        super().configure(cnf, **kwargs)
        
        # 如果有外观相关参数变更，重绘
        if update:
            self._draw_rounded_bg()

# 测试代码
if __name__ == "__main__":
    root = tk.Tk()
    root.title("真正的圆角 Label 示例")
    root.geometry("500x400")
    root.configure(bg="#f0f0f0")
    
    # 创建普通 Label 作为对比
    tk.Label(root, text="普通 Label", bg="white", padx=10, pady=5).pack(pady=10)
    
    # 创建不同样式的圆角 Label
    RoundedLabel(
        root, 
        text="基础圆角 Label", 
        bg="#4a90e2", 
        fg="white", 
        corner_radius=15,
        padx=20, 
        pady=10,
        font=("微软雅黑", 12)
    ).pack(pady=10)
    
    RoundedLabel(
        root, 
        text="带边框的圆角 Label", 
        bg="#ffffff", 
        fg="#333333", 
        corner_radius=10,
        border_width=2,
        border_color="#5cb85c",
        padx=20, 
        pady=10,
        font=("宋体", 10)
    ).pack(pady=10)
    
    RoundedLabel(
        root, 
        text="大圆角样式", 
        bg="#f0ad4e", 
        fg="white", 
        corner_radius=25,
        padx=30, 
        pady=15,
        font=("黑体", 14, "bold")
    ).pack(pady=10)
    
    root.mainloop()
