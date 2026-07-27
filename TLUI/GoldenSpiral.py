import tkinter as tk
import math

class GoldenSpiralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("黄金回旋线")
        self.root.attributes('-fullscreen', True)  # 全屏显示
        
        # 获取屏幕尺寸
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # 创建画布
        self.canvas = tk.Canvas(root, bg='white', width=self.screen_width, height=self.screen_height)
        self.canvas.pack()
        
        # 绘制黄金回旋线
        self.draw_golden_spiral()
        
        # 绑定退出快捷键
        self.root.bind('<Escape>', lambda e: root.destroy())
    
    def draw_golden_spiral(self):
        # 斐波那契数列 (调整过的版本: 1, 2, 3, 5, 8, 11...)
        # 注意: 这不是标准斐波那契，但按题目要求实现
        def modified_fibonacci(n):
            if n == 0:
                return 1
            elif n == 1:
                return 2
            elif n == 2:
                return 3
            else:
                return modified_fibonacci(n-1) + modified_fibonacci(n-2)
        
        # 计算缩放因子，使图形适应屏幕
        max_fib = modified_fibonacci(10)  # 计算足够大的斐波那契数来确定比例
        scale = min(self.screen_width, self.screen_height) / (max_fib * 2)
        
        # 中心点
        center_x, center_y = self.screen_width // 2, self.screen_height // 2
        
        # 初始参数
        fibs = [1, 2, 3, 5, 8, 11, 19, 30, 49, 79, 128]  # 预计算好的修改版斐波那契数列
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # 右、上、左、下
        dir_index = 0
        
        # 初始位置 (从中心点开始向右)
        x, y = center_x, center_y
        prev_fib = 0
        
        # 绘制螺旋
        for i in range(len(fibs)):
            current_fib = fibs[i]
            dx, dy = directions[dir_index % 4]
            
            # 计算圆弧的起始和结束角度
            start_angle = (dir_index - 1) * 90
            end_angle = dir_index * 90
            
            # 计算圆弧的边界框
            if dir_index % 4 == 0:  # 向右
                arc_x = x - prev_fib * scale
                arc_y = y - prev_fib * scale
                arc_width = current_fib * 2 * scale
                arc_height = current_fib * 2 * scale
            elif dir_index % 4 == 1:  # 向上
                arc_x = x - current_fib * scale
                arc_y = y - current_fib * scale
                arc_width = current_fib * 2 * scale
                arc_height = current_fib * 2 * scale
            elif dir_index % 4 == 2:  # 向左
                arc_x = x - current_fib * scale
                arc_y = y - (current_fib - prev_fib) * scale
                arc_width = current_fib * 2 * scale
                arc_height = (current_fib + prev_fib) * 2 * scale
            else:  # 向下
                arc_x = x - (current_fib - prev_fib) * scale
                arc_y = y - current_fib * scale
                arc_width = (current_fib + prev_fib) * 2 * scale
                arc_height = current_fib * 2 * scale
            
            # 绘制四分之一圆
            self.canvas.create_arc(
                arc_x, arc_y, 
                arc_x + arc_width, arc_y + arc_height,
                start=start_angle, extent=90, 
                outline="black", style=tk.ARC, width=2
            )
            
            # 更新位置
            x += dx * (current_fib - prev_fib) * scale
            y += dy * (current_fib - prev_fib) * scale
            
            prev_fib = current_fib
            dir_index += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = GoldenSpiralApp(root)
    root.mainloop()
