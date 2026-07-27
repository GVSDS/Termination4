import tkinter as tk
import random
import math
import time
import numpy as np
from PIL import Image, ImageTk
import tkinter.ttk

class CompleteGlitchArtPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("50种完整故障特效面板")
        self.root.configure(bg='black')
        self.root.geometry("1400x1000")

        # 主画布
        self.canvas = tk.Canvas(root, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 分页按钮面板
        self.notebook = tk.ttk.Notebook(root)
        self.frames = [tk.Frame(self.notebook) for _ in range(5)]
        for i, frame in enumerate(self.frames):
            self.notebook.add(frame, text=f"特效组{i+1}")
        self.notebook.pack(side=tk.BOTTOM, fill=tk.X)

        # 初始化所有50种特效
        self.effects = {
            # 第一组：基础故障
            "RGB分离": self.rgb_split,
            "像素位移": self.pixel_shift,
            "扫描线抖动": self.scan_line_jitter,
            "数字条纹": self.digital_stripe,
            "模拟噪点": self.analog_noise,
            "屏幕跳跃": self.screen_jump,
            "屏幕抖动": self.screen_shake,
            "波动抖动": self.wave_jitter,
            "错位图块": self.image_block_glitch,
            "错位线条": self.line_block_glitch,

            # 第二组：高级故障
            "图块抖动": self.tile_jitter,
            "过曝光": self.overexposure,
            "量子噪波": self.quantum_noise,
            "数据破损": self.databending,
            "残影拖尾": self.trailing_effect,
            "色彩溢出": self.color_bleed,
            "CRT曲率": self.crt_curvature,
            "电磁脉冲": self.emp_effect,
            "分形噪波": self.fractal_noise,
            "重力扭曲": self.gravity_warp,

            # 第三组：信号干扰
            "低频干扰": self.low_freq_interference,
            "高频闪烁": self.high_freq_flicker,
            "马赛克破损": self.mosaic_corruption,
            "神经噪点": self.neural_noise,
            "等离子体": self.plasma_effect,
            "信号丢失": self.signal_loss,
            "时空撕裂": self.time_rip,
            "VHS噪点": self.vhs_noise,
            "宇宙射线": self.cosmic_ray,
            "维度偏移": self.dimensional_shift,

            # 第四组：数字失真
            "熵增噪点": self.entropy_noise,
            "生物电干扰": self.bio_electric,
            "压缩伪影": self.compression_artifacts,
            "动态模糊": self.motion_blur,
            "通道偏移": self.channel_offset,
            "几何变形": self.geometric_distortion,
            "像素排序": self.pixel_sorting,
            "随机条纹": self.random_stripes,
            "光晕扩散": self.bloom_effect,
            "时间延迟": self.time_delay_effect,

            # 第五组：特殊效果
            "磁场干扰": self.magnetic_distortion,
            "数字衰减": self.digital_decay,
            "模拟失真": self.analog_distortion,
            "频带分离": self.frequency_split,
            "数据包丢失": self.packet_loss,
            "负片效果": self.negative,
            "色彩反相": self.color_inversion,
            "光栅变形": self.raster_distortion,
            "像素化": self.pixelation,
            "动态色块": self.dynamic_color_blocks
        }

        # 创建分页按钮
        self.create_paged_buttons()

    def create_paged_buttons(self):
        """创建分页按钮（每页10个，5列×2行）"""
        effects_list = list(self.effects.items())
        for page in range(5):
            start_idx = page * 10
            end_idx = start_idx + 10
            for i, (name, _) in enumerate(effects_list[start_idx:end_idx]):
                btn = tk.Button(
                    self.frames[page], 
                    text=name,
                    command=lambda n=name: self.run_effect(n),
                    bg='#222', 
                    fg='white', 
                    width=15,
                    font=('Arial', 9),
                    relief=tk.RAISED,
                    borderwidth=2
                )
                # 计算行和列：每行5个按钮
                btn.grid(
                    row=i // 5,  # 行索引（0或1）
                    column=i % 5,  # 列索引（0-4）
                    padx=5, 
                    pady=5,
                    sticky="ew"  # 按钮水平拉伸填充单元格
                )
            
            # 配置网格权重，使按钮均匀分布
            for col in range(5):
                self.frames[page].columnconfigure(col, weight=1)
            for row in range(2):
                self.frames[page].rowconfigure(row, weight=1)

    def run_effect(self, effect_name):
        """执行指定特效"""
        self.canvas.delete("all")
        self.effects[effect_name]()

    # ========== 以下是50种特效的完整实现 ==========

    # 1. RGB三通道分离（抖音风格）
    def rgb_split(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for i, (color, offset) in enumerate(zip(["#FF0000", "#00FF00", "#0000FF"], [5, 10, 15])):
            self.canvas.create_text(
                w//2 + offset * math.sin(time.time()), 
                h//2 + offset * math.cos(time.time()),
                text="GLITCH", fill=color, font=("Arial", 36)
            )

    # 2. 随机像素位移（显存错误模拟）
    def pixel_shift(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(1000):
            x, y = random.randint(0, w), random.randint(0, h)
            self.canvas.create_rectangle(
                x, y, x+random.randint(1, 5), y+random.randint(1, 5),
                fill=f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
            )

    # 3. 扫描线抖动（CRT显示器效果）
    def scan_line_jitter(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for y in range(0, h, 2):
            offset = random.randint(-3, 3) if random.random() > 0.8 else 0
            self.canvas.create_line(0, y+offset, w, y+offset, fill="#111111", width=1)

    # 4. 数字条纹干扰（VHS磁带损坏）
    def digital_stripe(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for x in range(0, w, 10):
            if random.random() > 0.9:
                self.canvas.create_line(
                    x, 0, x, h,
                    fill=f"#{random.randint(100, 255):02x}0000",
                    width=random.randint(1, 3)
                )

    # 5. 模拟噪点（电视雪花）
    def analog_noise(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(2000):
            x, y = random.randint(0, w), random.randint(0, h)
            brightness = random.randint(50, 200)
            self.canvas.create_rectangle(
                x, y, x+1, y+1,
                fill=f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            )

    # 6. 屏幕垂直跳跃（场同步故障）
    def screen_jump(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        jump = int(h * 0.2 * math.sin(time.time() * 2))
        self.canvas.create_rectangle(0, jump, w, h+jump, fill="black")

    # 7. 屏幕随机抖动（地震效果）
    def screen_shake(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        dx, dy = random.randint(-20, 20), random.randint(-20, 20)
        self.canvas.create_rectangle(dx, dy, w+dx, h+dy, fill="black")

    # 8. 正弦波扭曲（信号干扰）
    def wave_jitter(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for y in range(0, h, 5):
            amp = 30 * math.sin(time.time() + y/30)
            self.canvas.create_line(
                amp, y, w-amp, y,
                fill=f"#{random.randint(50, 200):02x}00{random.randint(50, 200):02x}",
                width=2
            )

    # 9. 错位图块（JPEG压缩错误）
    def image_block_glitch(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        block_size = 30
        for x in range(0, w, block_size):
            for y in range(0, h, block_size):
                if random.random() > 0.7:
                    dx, dy = random.randint(-15, 15), random.randint(-15, 15)
                    self.canvas.create_rectangle(
                        x+dx, y+dy, x+block_size+dx, y+block_size+dy,
                        fill=f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
                    )

    # 10. 错位线条（数字信号断裂）
    def line_block_glitch(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for y in range(0, h, 8):
            if random.random() > 0.8:
                break_point = random.randint(50, w-50)
                self.canvas.create_line(0, y, break_point, y, fill="cyan", width=1)
                self.canvas.create_line(break_point+20, y, w, y, fill="cyan", width=1)

    # 11. 图块抖动（动态马赛克）
    def tile_jitter(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        block_size = 10
        for x in range(0, w, block_size):
            for y in range(0, h, block_size):
                if random.random() > 0.9:
                    dx = random.randint(-3, 3) * math.sin(time.time() * 5)
                    dy = random.randint(-3, 3) * math.cos(time.time() * 5)
                    self.canvas.create_rectangle(
                        x+dx, y+dy, x+block_size+dx, y+block_size+dy,
                        fill=f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
                    )

    # 12. 过曝光（高光溢出）
    def overexposure(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.create_rectangle(0, 0, w, h, fill="#FFFFFF", stipple="gray50")
        for _ in range(500):
            x, y = random.randint(0, w), random.randint(0, h)
            self.canvas.create_oval(x, y, x+30, y+30, fill="white", outline="")

    # 13. 量子噪波（柏林噪声）
    def quantum_noise(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        noise = np.random.rand(w//5, h//5)
        for x in range(0, w, 5):
            for y in range(0, h, 5):
                val = int(noise[x//5][y//5] * 255)
                self.canvas.create_rectangle(
                    x, y, x+5, y+5,
                    fill=f"#{val:02x}{val:02x}{val:02x}"
                )

    # 14. 数据破损（文件损坏模拟）
    def databending(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(10):
            x1, y1 = random.randint(0, w//2), random.randint(0, h//2)
            x2, y2 = x1 + random.randint(50, 200), y1 + random.randint(50, 200)
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=f"#{random.randint(0, 100):02x}{random.randint(0, 100):02x}{random.randint(0, 100):02x}"
            )

    # 15. 残影拖尾（运动模糊）
    def trailing_effect(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for i in range(3):
            offset = i * 10
            self.canvas.create_text(
                w//2 + offset, h//2 + offset,
                text="TRAIL", fill=f"#FF00{55+i*50:02x}", font=("Arial", 24)
            )

    # 16. 色彩溢出（通道混合）
    def color_bleed(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(500):
            x, y = random.randint(0, w), random.randint(0, h)
            self.canvas.create_rectangle(
                x, y, x+10, y+10,
                fill=f"#{random.randint(200, 255):02x}00{random.randint(200, 255):02x}",
                stipple="gray25"
            )

    # 17. CRT曲率（老式显示器变形）
    def crt_curvature(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for y in range(0, h, 5):
            curve = int(20 * math.sin(y/40))
            self.canvas.create_line(
                curve, y, w-curve, y,
                fill=f"#{random.randint(50, 150):02x}{random.randint(50, 150):02x}{random.randint(50, 150):02x}"
            )

    # 18. 电磁脉冲（径向干扰）
    def emp_effect(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        center_x, center_y = w//2, h//2
        for r in range(0, max(w, h)//2, 10):
            if random.random() > 0.7:
                self.canvas.create_oval(
                    center_x-r, center_y-r, center_x+r, center_y+r,
                    outline=f"#{random.randint(100, 255):02x}00{random.randint(100, 255):02x}",
                    width=2
                )

    # 19. 分形噪波（自然纹理）
    def fractal_noise(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.delete("all")  # 清空画布
        
        # 分块处理（每50x50像素为一组）
        for x in range(0, w, 50):
            for y in range(0, h, 50):
                # 延迟渲染避免界面冻结
                self.canvas.after(0, lambda x=x, y=y: self._draw_noise_block(x, y, w, h))
        
    def _draw_noise_block(self, start_x, start_y, w, h):
        """绘制单个噪点块"""
        for x in range(start_x, min(start_x+50, w), 3):
            for y in range(start_y, min(start_y+50, h), 3):
                val = int((math.sin(x/10) + math.cos(y/10)) * 128 + 128)
                val = max(0, min(255, val))
                self.canvas.create_rectangle(
                    x, y, x+3, y+3,
                    fill=f"#{val:02x}{val:02x}{val:02x}"
                )
        self.canvas.update_idletasks()  # 局部刷新界面

    # 20. 重力扭曲（像素坍缩）
    def gravity_warp(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        center_x, center_y = w//2, h//2
        for x in range(0, w, 15):
            for y in range(0, h, 15):
                dx = int((center_x - x) * 0.1)
                dy = int((center_y - y) * 0.1)
                self.canvas.create_rectangle(
                    x+dx, y+dy, x+15+dx, y+15+dy,
                    fill=f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
                )

    # 21. 低频干扰（模拟电磁干扰）
    def low_freq_interference(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for y in range(0, h, 3):
            offset = int(10 * math.sin(y/20 + time.time()))
            self.canvas.create_line(
                0, y + offset, w, y + offset,
                fill="#444444",
                width=1
            )

    # 22. 高频闪烁（CRT老化效果）
    def high_freq_flicker(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        flicker = random.randint(0, 255)
        self.canvas.create_rectangle(
            0, 0, w, h,
            fill=f"#{flicker:02x}{flicker:02x}{flicker:02x}",
            outline=""
        )

    # 23. 马赛克破损（JPEG块错误）
    def mosaic_corruption(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        block_size = 15
        for x in range(0, w, block_size):
            for y in range(0, h, block_size):
                if random.random() > 0.8:
                    self.canvas.create_rectangle(
                        x, y, x+block_size, y+block_size,
                        fill=f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
                    )

    # 24. 神经噪点（生物电干扰模拟）
    def neural_noise(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(2000):
            x, y = random.randint(0, w), random.randint(0, h)
            val = int(255 * abs(math.sin(x/50 + y/50 + time.time())))
            self.canvas.create_oval(
                x, y, x+2, y+2,
                fill=f"#{val:02x}{val:02x}{val:02x}"
            )

    # 25. 等离子体（动态光斑）
    def plasma_effect(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(100):
            x, y = random.randint(0, w), random.randint(0, h)
            radius = random.randint(5, 30)
            self.canvas.create_oval(
                x-radius, y-radius, x+radius, y+radius,
                fill=f"#{random.randint(100, 255):02x}00{random.randint(100, 255):02x}",
                outline=""
            )

    # 26. 信号丢失（模拟断线）
    def signal_loss(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(50):
            x1, y1 = random.randint(0, w), random.randint(0, h)
            length = random.randint(20, 100)
            self.canvas.create_line(
                x1, y1, x1+length, y1,
                fill="white" if random.random() > 0.5 else "red",
                width=2
            )

    # 27. 时空撕裂（维度裂缝效果）
    def time_rip(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for i in range(10):
            offset = int(30 * math.sin(time.time() * 2 + i))
            self.canvas.create_line(
                0, h//2 + offset + i*15, 
                w, h//2 - offset + i*15,
                fill=f"#{random.randint(100, 255):02x}00{random.randint(100, 255):02x}",
                width=3
            )

    # 28. VHS噪点（模拟磁带噪波）
    def vhs_noise(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(3000):
            x, y = random.randint(0, w), random.randint(0, h)
            brightness = random.randint(50, 200)
            self.canvas.create_rectangle(
                x, y, x+1, y+1,
                fill=f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            )

    # 29. 宇宙射线（高能粒子轨迹）
    def cosmic_ray(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(5):
            x, y = random.randint(0, w), 0
            length = random.randint(50, h)
            self.canvas.create_line(
                x, y, x + random.randint(-20, 20), y + length,
                fill=f"#{random.randint(200, 255):02x}{random.randint(200, 255):02x}{random.randint(200, 255):02x}",
                width=2
            )

    # 30. 维度偏移（空间扭曲）
    def dimensional_shift(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for x in range(0, w, 20):
            shift = int(15 * math.sin(x/30 + time.time()))
            self.canvas.create_line(
                x, 0 + shift, x, h - shift,
                fill=f"#{random.randint(50, 150):02x}{random.randint(50, 150):02x}{random.randint(50, 150):02x}"
            )

    # 31. 熵增噪点（信息熵混乱）
    def entropy_noise(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(1500):
            x, y = random.randint(0, w), random.randint(0, h)
            val = int(255 * (1 - abs(math.sin(x*y + time.time()))))
            self.canvas.create_rectangle(
                x, y, x+3, y+3,
                fill=f"#{val:02x}{val:02x}{val:02x}"
            )

    # 32. 生物电干扰（神经脉冲模拟）
    def bio_electric(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(30):
            center_x, center_y = random.randint(0, w), random.randint(0, h)
            for r in range(0, 50, 5):
                self.canvas.create_oval(
                    center_x-r, center_y-r, center_x+r, center_y+r,
                    outline=f"#{random.randint(100, 255):02x}00{random.randint(100, 255):02x}",
                    width=1
                )

    # 33. 压缩伪影（JPEG失真）
    def compression_artifacts(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        block_size = 8
        for x in range(0, w, block_size):
            for y in range(0, h, block_size):
                if random.random() > 0.7:
                    color = random.choice(["#FF0000", "#00FF00", "#0000FF"])
                    self.canvas.create_rectangle(
                        x, y, x+block_size, y+block_size,
                        fill=color,
                        outline=""
                    )

    # 34. 动态模糊（运动残影）
    def motion_blur(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for i in range(3):
            offset = i * 5
            self.canvas.create_text(
                w//2 + offset, h//2 + offset,
                text="MOTION BLUR",
                fill=f"#FFFF{85-i*30:02x}",
                font=("Arial", 24)
            )

    # 35. 通道偏移（色彩分离进阶）
    def channel_offset(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        offsets = [(10, 5), (-5, 10), (5, -10)]
        for i, (dx, dy) in enumerate(offsets):
            color = ["#FF0000", "#00FF00", "#0000FF"][i]
            self.canvas.create_text(
                w//2 + dx, h//2 + dy,
                text="CHANNEL OFFSET",
                fill=color,
                font=("Arial", 24)
            )

    # 36. 几何变形（非线性扭曲）
    def geometric_distortion(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for y in range(0, h, 10):
            distortion = int(30 * math.sin(y/30 + time.time()))
            self.canvas.create_line(
                0 + distortion, y, w - distortion, y,
                fill="#FFFFFF",
                width=2
            )

    # 37. 像素排序（算法艺术）
    def pixel_sorting(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        columns = []
        for x in range(0, w, 2):
            col_height = random.randint(10, h//2)
            columns.append((x, h//2 - col_height, x+2, h//2 + col_height))
        
        for x1, y1, x2, y2 in columns:
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
            )

    # 38. 随机条纹（数据流错误）
    def random_stripes(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(20):
            x = random.randint(0, w)
            width = random.randint(1, 10)
            self.canvas.create_rectangle(
                x, 0, x+width, h,
                fill=f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}",
                outline=""
            )

    # 39. 光晕扩散（Bloom效果）
    def bloom_effect(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(15):
            x, y = random.randint(0, w), random.randint(0, h)
            radius = random.randint(20, 100)
            self.canvas.create_oval(
                x-radius, y-radius, x+radius, y+radius,
                fill=f"#FFFF{random.randint(10, 100):02x}",
                outline=""
            )

    # 40. 时间延迟（帧不同步）
    def time_delay_effect(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for i in range(3):
            offset = i * 15
            self.canvas.create_rectangle(
                offset, offset, w-offset, h-offset,
                outline=f"#{random.randint(100, 255):02x}{random.randint(100, 255):02x}{random.randint(100, 255):02x}",
                width=2
            )

    # 41. 磁场干扰（磁力线扭曲）
    def magnetic_distortion(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        center_x, center_y = w//2, h//2
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            radius = random.randint(50, 150)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            self.canvas.create_line(
                center_x, center_y, x, y,
                fill="#00FFFF",
                width=1
            )

    # 42. 数字衰减（数据腐蚀）
    def digital_decay(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(500):
            x, y = random.randint(0, w), random.randint(0, h)
            size = random.randint(1, 5)
            self.canvas.create_rectangle(
                x, y, x+size, y+size,
                fill="#000000" if random.random() > 0.3 else "#FFFFFF",
                outline=""
            )

    # 43. 模拟失真（老式电视）
    def analog_distortion(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for y in range(0, h, 2):
            curve = int(20 * math.sin(y/40 + time.time()))
            noise = random.randint(0, 50)
            self.canvas.create_line(
                curve, y+noise, w-curve, y+noise,
                fill=f"#{50+noise:02x}{50+noise:02x}{50+noise:02x}"
            )

    # 44. 频带分离（频谱分析）
    def frequency_split(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        bands = 10
        band_width = w // bands
        for i in range(bands):
            height = random.randint(10, h//2)
            self.canvas.create_rectangle(
                i*band_width, h//2 - height,
                (i+1)*band_width, h//2 + height,
                fill=f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
            )

    # 45. 数据包丢失（网络错误）
    def packet_loss(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(30):
            x1, y1 = random.randint(0, w//2), random.randint(0, h//2)
            size = random.randint(20, 100)
            self.canvas.create_rectangle(
                x1, y1, x1+size, y1+size,
                fill="#000000",
                outline=""
            )

    # 46. 负片效果（颜色反转）
    def negative(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.create_rectangle(
            0, 0, w, h,
            fill="#FFFFFF",
            outline=""
        )
        self.canvas.create_text(
            w//2, h//2,
            text="NEGATIVE",
            fill="#000000",
            font=("Arial", 36)
        )

    # 47. 色彩反相（RGB反转）
    def color_inversion(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(500):
            x, y = random.randint(0, w), random.randint(0, h)
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            self.canvas.create_rectangle(
                x, y, x+5, y+5,
                fill=f"#{255-r:02x}{255-g:02x}{255-b:02x}"
            )

    # 48. 光栅变形（扫描线进阶）
    def raster_distortion(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for y in range(0, h, 4):
            offset = int(10 * math.sin(y/30 + time.time()))
            width = random.randint(1, 3)
            self.canvas.create_line(
                0, y+offset, w, y+offset,
                fill="#FFFFFF",
                width=width
            )

    # 49. 像素化（马赛克效果）
    def pixelation(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        block_size = 15
        for x in range(0, w, block_size):
            for y in range(0, h, block_size):
                self.canvas.create_rectangle(
                    x, y, x+block_size, y+block_size,
                    fill=f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}",
                    outline=""
                )

    # 50. 动态色块（抽象艺术）
    def dynamic_color_blocks(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for _ in range(50):
            x1, y1 = random.randint(0, w), random.randint(0, h)
            size = random.randint(20, 100)
            self.canvas.create_rectangle(
                x1, y1, x1+size, y1+size,
                fill=f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}",
                outline=""
            )
            # 添加内部细节
            for _ in range(5):
                inner_x = random.randint(x1, x1+size)
                inner_y = random.randint(y1, y1+size)
                self.canvas.create_line(
                    inner_x, inner_y, 
                    inner_x+random.randint(-10, 10), 
                    inner_y+random.randint(-10, 10),
                    fill="white" if random.random() > 0.5 else "black",
                    width=random.randint(1, 3)
                )

if __name__ == "__main__":
    root = tk.Tk()
    app = CompleteGlitchArtPanel(root)
    root.mainloop()