from TLib.T_imports import *
from . import Tool

class ScreenErrorSimulator:
    def __init__(self):
        self.root = tkinter.Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # 设置全屏无边框窗口
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        # 创建画布
        self.canvas = tkinter.Canvas(self.root, width=self.screen_width, height=self.screen_height, 
                               bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # 特效列表
        self.effects = [
            self.glitch_lines,
            self.color_shift,
            self.static_noise,
            self.vertical_roll,
            self.horizontal_roll,
            self.pixel_distortion,
            self.wave_distortion,
            self.color_inversion,
            self.burn_in,
            self.random_blocks,
            self.rgb_split,
            self.pixel_shift,
            self.scan_line_jitter,
            self.digital_stripe,
            self.analog_noise,
            self.screen_jump,
            self.screen_shake,
            self.wave_jitter,
            self.image_block_glitch,
            self.line_block_glitch,
            self.tile_jitter,
            self.overexposure,
            self.quantum_noise,
            self.databending,
            self.trailing_effect,
            self.color_bleed,
            self.crt_curvature,
            self.emp_effect,
            self.fractal_noise,
            self.gravity_warp,
            self.low_freq_interference,
            self.high_freq_flicker,
            self.mosaic_corruption,
            self.neural_noise,
            self.plasma_effect,
            self.signal_loss,
            self.time_rip,
            self.vhs_noise,
            self.cosmic_ray,
            self.dimensional_shift,
            self.entropy_noise,
            self.bio_electric,
            self.compression_artifacts,
            self.motion_blur,
            self.channel_offset,
            self.geometric_distortion,
            self.pixel_sorting,
            self.random_stripes,
            self.bloom_effect,
            self.time_delay_effect,
            self.magnetic_distortion,
            self.digital_decay,
            self.analog_distortion,
            self.frequency_split,
            self.packet_loss,
            self.negative,
            self.color_inversion,
            self.raster_distortion,
            self.pixelation,
            self.dynamic_color_blocks
        ]
        
        self.current_effect = 0
        self.effect_start_time = time.time()
        self.effect_duration = 0.3  # 每个特效持续时间(秒)
        
        # 使用Pillow创建抗锯齿图像
        self.pil_image = Image.new('RGB', (self.screen_width, self.screen_height), 'black')
        self.draw = ImageDraw.Draw(self.pil_image)
        self.tk_image = None
        
        self.end=0
        self.animate()
        self.root.mainloop()
    
    def animate(self):
        now = time.time()
        elapsed = now - self.effect_start_time
        
        # 如果当前特效持续时间结束，切换到下一个
        if elapsed > self.effect_duration:
            self.current_effect = (self.current_effect + 1) % len(self.effects)
            if self.current_effect == 0 and self.end:
                self.root.destroy()
                return
        #    self.current_effect = self.effects.index(random.choice(self.effects))
            self.effect_start_time = now
            self.end=1
        
        # 清除Pillow图像
        self.draw.rectangle([0, 0, self.screen_width, self.screen_height], fill='black')
        
        # 应用当前特效
        self.effects[self.current_effect]()
        
        # 将Pillow图像转换为Tkinter PhotoImage并显示
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor='nw')
        
        # 保持高帧率
        self.root.after(16, self.animate)
    
    def glitch_lines(self):
        """水平线干扰效果"""
        for y in range(0, self.screen_height, 5):
            offset = random.randint(-10, 10)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.draw.line([(0, y), (self.screen_width, y + offset)], fill=color, width=1)
    
    def color_shift(self):
        """颜色偏移效果"""
        for x in range(0, self.screen_width, 3):
            r = int(255 * abs(math.sin(x * 0.01 + time.time())))
            g = int(255 * abs(math.sin(x * 0.02 + time.time() * 0.8)))
            b = int(255 * abs(math.sin(x * 0.03 + time.time() * 0.6)))
            self.draw.line([(x, 0), (x, self.screen_height)], fill=(r, g, b), width=3)
    
    def static_noise(self):
        """静态噪声效果"""
        for _ in range(1000):
            x = random.randint(0, self.screen_width - 1)
            y = random.randint(0, self.screen_height - 1)
            intensity = random.randint(0, 255)
            self.draw.point((x, y), fill=(intensity, intensity, intensity))
    
    def vertical_roll(self):
        """垂直滚动效果"""
        offset = int(time.time() * 50) % self.screen_height
        for y in range(0, self.screen_height, 10):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            y_pos = (y + offset) % self.screen_height
            self.draw.line([(0, y_pos), (self.screen_width, y_pos)], fill=color, width=10)
    
    def horizontal_roll(self):
        """水平滚动效果"""
        offset = int(time.time() * 40) % self.screen_width
        for x in range(0, self.screen_width, 10):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            x_pos = (x + offset) % self.screen_width
            self.draw.line([(x_pos, 0), (x_pos, self.screen_height)], fill=color, width=10)
    
    def pixel_distortion(self):
        """像素扭曲效果"""
        for y in range(0, self.screen_height, 5):
            for x in range(0, self.screen_width, 5):
                offset_x = int(10 * math.sin(y * 0.05 + time.time()))
                offset_y = int(10 * math.cos(x * 0.05 + time.time()))
                color = (
                    (x + y + int(time.time() * 100)) % 256,
                    (x - y + int(time.time() * 80)) % 256,
                    (y - x + int(time.time() * 60)) % 256
                )
                self.draw.rectangle(
                    [x + offset_x, y + offset_y, x + offset_x + 5, y + offset_y + 5],
                    fill=color
                )
    
    def wave_distortion(self):
        """波浪扭曲效果"""
        for y in range(0, self.screen_height, 2):
            wave = int(50 * math.sin(y * 0.02 + time.time() * 2))
            color = (
                int(128 + 127 * math.sin(y * 0.01 + time.time())),
                int(128 + 127 * math.sin(y * 0.015 + time.time() * 1.5)),
                int(128 + 127 * math.sin(y * 0.02 + time.time() * 0.8))
            )
            self.draw.line([(0, y), (self.screen_width, y + wave)], fill=color, width=2)
    
    def color_inversion(self):
        """颜色反转效果"""
        for y in range(0, self.screen_height, 10):
            for x in range(0, self.screen_width, 10):
                r = 255 - (x % 256)
                g = 255 - (y % 256)
                b = 255 - ((x + y) % 256)
                self.draw.rectangle([x, y, x + 10, y + 10], fill=(r, g, b))
    
    def burn_in(self):
        """烧屏效果"""
        for _ in range(500):
            x = random.randint(0, self.screen_width - 1)
            y = random.randint(0, self.screen_height - 1)
            r = random.randint(200, 255)
            g = random.randint(0, 100)
            b = random.randint(0, 50)
            self.draw.rectangle([x, y, x + 3, y + 3], fill=(r, g, b))
    
    def random_blocks(self):
        """随机色块效果"""
        for _ in range(50):
            x = random.randint(0, self.screen_width - 50)
            y = random.randint(0, self.screen_height - 50)
            width = random.randint(10, 100)
            height = random.randint(10, 100)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.draw.rectangle([x, y, x + width, y + height], fill=(r, g, b))

    def rgb_split(self):
        """1. RGB三通道分离（抖音风格）"""
        text = "GLITCH"
        font = ImageFont.load_default(size=36)  # 需要先定义字体
        for i, (color, offset) in enumerate(zip(["red", "green", "blue"], [5, 10, 15])):
            x = self.screen_width//2 + offset * math.sin(time.time())
            y = self.screen_height//2 + offset * math.cos(time.time())
            self.draw.text((x, y), text, fill=color, font=font)

    def pixel_shift(self):
        """2. 随机像素位移（显存错误模拟）"""
        for _ in range(1000):
            x, y = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            self.draw.rectangle(
                [x, y, x+random.randint(1, 5), y+random.randint(1, 5)],
                fill=color
            )

    def scan_line_jitter(self):
        """3. 扫描线抖动（CRT显示器效果）"""
        for y in range(0, self.screen_height, 2):
            offset = random.randint(-3, 3) if random.random() > 0.8 else 0
            self.draw.line(
                [0, y+offset, self.screen_width, y+offset],
                fill=(17, 17, 17),
                width=1
            )

    def digital_stripe(self):
        """4. 数字条纹干扰（VHS磁带损坏）"""
        for x in range(0, self.screen_width, 10):
            if random.random() > 0.9:
                r = random.randint(100, 255)
                width = random.randint(1, 3)
                self.draw.line(
                    [x, 0, x, self.screen_height],
                    fill=(r, 0, 0),
                    width=width
                )

    def analog_noise(self):
        """5. 模拟噪点（电视雪花）"""
        for _ in range(2000):
            x, y = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
            brightness = random.randint(50, 200)
            self.draw.rectangle(
                [x, y, x+1, y+1],
                fill=(brightness, brightness, brightness)
            )

    def screen_jump(self):
        """6. 屏幕垂直跳跃（场同步故障）"""
        jump = int(self.screen_height * 0.2 * math.sin(time.time() * 2))
        self.draw.rectangle(
            [0, jump, self.screen_width, self.screen_height+jump],
            fill="black"
        )

    def screen_shake(self):
        """7. 屏幕随机抖动（地震效果）"""
        dx, dy = random.randint(-20, 20), random.randint(-20, 20)
        self.draw.rectangle(
            [dx, dy, self.screen_width+dx, self.screen_height+dy],
            fill="black"
        )

    def wave_jitter(self):
        """8. 正弦波扭曲（信号干扰）"""
        for y in range(0, self.screen_height, 5):
            amp = 30 * math.sin(time.time() + y/30)
            r = random.randint(50, 200)
            b = random.randint(50, 200)
            self.draw.line(
                [amp, y, self.screen_width-amp, y],
                fill=(r, 0, b),
                width=2
            )

    def image_block_glitch(self):
        """9. 错位图块（JPEG压缩错误）"""
        block_size = 30
        for x in range(0, self.screen_width, block_size):
            for y in range(0, self.screen_height, block_size):
                if random.random() > 0.7:
                    dx, dy = random.randint(-15, 15), random.randint(-15, 15)
                    color = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255)
                    )
                    self.draw.rectangle(
                        [x+dx, y+dy, x+block_size+dx, y+block_size+dy],
                        fill=color
                    )

    def line_block_glitch(self):
        """10. 错位线条（数字信号断裂）"""
        for y in range(0, self.screen_height, 8):
            if random.random() > 0.8:
                break_point = random.randint(50, self.screen_width-50)
                self.draw.line(
                    [0, y, break_point, y],
                    fill="cyan",
                    width=1
                )
                self.draw.line(
                    [break_point+20, y, self.screen_width, y],
                    fill="cyan",
                    width=1
                )

    def tile_jitter(self):
        """11. 图块抖动（动态马赛克）"""
        block_size = 10
        for x in range(0, self.screen_width, block_size):
            for y in range(0, self.screen_height, block_size):
                if random.random() > 0.9:
                    dx = int(random.randint(-3, 3) * math.sin(time.time() * 5))
                    dy = int(random.randint(-3, 3) * math.cos(time.time() * 5))
                    color = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255)
                    )
                    self.draw.rectangle(
                        [x+dx, y+dy, x+block_size+dx, y+block_size+dy],
                        fill=color
                    )

    def overexposure(self):
        """12. 过曝光（高光溢出）"""
        # 创建半透明白色层
        overlay = Image.new('RGBA', (self.screen_width, self.screen_height), (255, 255, 255, 100))
        self.pil_image.paste(overlay, (0, 0), overlay)
        # 添加随机光斑
        for _ in range(500):
            x, y = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
            radius = random.randint(5, 20)
            self.draw.ellipse(
                [x-radius, y-radius, x+radius, y+radius],
                fill=(255, 255, 255, random.randint(100, 200))
            )

    def quantum_noise(self):
        """13. 量子噪波（柏林噪声）"""
        # 使用简化版的噪声生成（实际应用可使用更复杂的噪声算法）
        for x in range(0, self.screen_width, 5):
            for y in range(0, self.screen_height, 5):
                val = int(255 * abs(math.sin(x/50 + y/50 + time.time())))
                self.draw.rectangle(
                    [x, y, x+5, y+5],
                    fill=(val, val, val)
                )

    def databending(self):
        """14. 数据破损（文件损坏模拟）"""
        for _ in range(10):
            x1 = random.randint(0, self.screen_width//2)
            y1 = random.randint(0, self.screen_height//2)
            x2 = x1 + random.randint(50, 200)
            y2 = y1 + random.randint(50, 200)
            self.draw.rectangle(
                [x1, y1, x2, y2],
                fill=(
                    random.randint(0, 100),
                    random.randint(0, 100),
                    random.randint(0, 100)
                )
            )

    def trailing_effect(self):
        """15. 残影拖尾（运动模糊）"""
        text = "TRAIL"
        font = ImageFont.load_default(size=24)
        for i in range(3):
            offset = i * 10
            self.draw.text(
                (self.screen_width//2 + offset, self.screen_height//2 + offset),
                text,
                fill=(255, 0, 55+i*50),
                font=font
            )

    def color_bleed(self):
        """16. 色彩溢出（通道混合）"""
        for _ in range(500):
            x, y = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
            self.draw.rectangle(
                [x, y, x+10, y+10],
                fill=(
                    random.randint(200, 255),
                    0,
                    random.randint(200, 255)
                )
            )

    def crt_curvature(self):
        """17. CRT曲率（老式显示器变形）"""
        for y in range(0, self.screen_height, 5):
            curve = int(20 * math.sin(y/40))
            color = (
                random.randint(50, 150),
                random.randint(50, 150),
                random.randint(50, 150)
            )
            self.draw.line(
                [curve, y, self.screen_width-curve, y],
                fill=color,
                width=1
            )

    def emp_effect(self):
        """18. 电磁脉冲（径向干扰）"""
        center_x, center_y = self.screen_width//2, self.screen_height//2
        for r in range(0, max(self.screen_width, self.screen_height)//2, 10):
            if random.random() > 0.7:
                self.draw.ellipse(
                    [center_x-r, center_y-r, center_x+r, center_y+r],
                    outline=(
                        random.randint(100, 255),
                        0,
                        random.randint(100, 255)
                    ),
                    width=2
                )

    def fractal_noise(self):
        """19. 分形噪波（自然纹理）"""
        for x in range(0, self.screen_width, 50):
            for y in range(0, self.screen_height, 50):
                val = int((math.sin(x/10) + math.cos(y/10)) * 128 + 128)
                val = max(0, min(255, val))
                self.draw.rectangle(
                    [x, y, x+3, y+3],
                    fill=(val, val, val)
                )

    def gravity_warp(self):
        """20. 重力扭曲（像素坍缩）"""
        center_x, center_y = self.screen_width//2, self.screen_height//2
        for x in range(0, self.screen_width, 15):
            for y in range(0, self.screen_height, 15):
                dx = int((center_x - x) * 0.1)
                dy = int((center_y - y) * 0.1)
                self.draw.rectangle(
                    [x+dx, y+dy, x+15+dx, y+15+dy],
                    fill=(
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255)
                    )
                )

    def low_freq_interference(self):
        """21. 低频干扰（模拟电磁干扰）"""
        for y in range(0, self.screen_height, 3):
            offset = int(10 * math.sin(y/20 + time.time()))
            self.draw.line(
                [0, y+offset, self.screen_width, y+offset],
                fill=(68, 68, 68),  # #444444的RGB值
                width=1
            )

    def high_freq_flicker(self):
        """22. 高频闪烁（CRT老化效果）"""
        flicker = random.randint(0, 255)
        self.draw.rectangle(
            [0, 0, self.screen_width, self.screen_height],
            fill=(flicker, flicker, flicker)
        )

    def mosaic_corruption(self):
        """23. 马赛克破损（JPEG块错误）"""
        block_size = 15
        for x in range(0, self.screen_width, block_size):
            for y in range(0, self.screen_height, block_size):
                if random.random() > 0.8:
                    self.draw.rectangle(
                        [x, y, x+block_size, y+block_size],
                        fill=(
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255)
                        )
                    )

    def neural_noise(self):
        """24. 神经噪点（生物电干扰模拟）"""
        for _ in range(2000):
            x, y = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
            val = int(255 * abs(math.sin(x/50 + y/50 + time.time())))
            self.draw.ellipse(
                [x, y, x+2, y+2],
                fill=(val, val, val)
            )

    def plasma_effect(self):
        """25. 等离子体（动态光斑）"""
        for _ in range(100):
            x, y = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
            radius = random.randint(5, 30)
            self.draw.ellipse(
                [x-radius, y-radius, x+radius, y+radius],
                fill=(
                    random.randint(100, 255),
                    0,
                    random.randint(100, 255)
                )
            )

    def signal_loss(self):
        """26. 信号丢失（电视雪花）"""
        for _ in range(3000):
            x, y = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
            self.draw.point(
                (x, y),
                fill=(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            )

    def time_rip(self):
        """27. 时空撕裂（垂直撕裂效果）"""
        tear_pos = random.randint(0, self.screen_width)
        tear_offset = random.randint(-50, 50)
        self.draw.rectangle(
            [0, 0, tear_pos, self.screen_height],
            fill="black"
        )
        self.draw.rectangle(
            [tear_pos, tear_offset, self.screen_width, self.screen_height+tear_offset],
            fill="black"
        )

    def vhs_noise(self):
        """28. VHS噪点（磁带噪声）"""
        for y in range(0, self.screen_height, 2):
            noise = random.randint(-20, 20)
            color = (
                random.randint(50, 100),
                random.randint(50, 100),
                random.randint(50, 100)
            )
            self.draw.line(
                [0, y+noise, self.screen_width, y+noise],
                fill=color,
                width=1
            )

    def cosmic_ray(self):
        """29. 宇宙射线（高能粒子轨迹）"""
        start_x = random.randint(0, self.screen_width)
        start_y = random.randint(0, self.screen_height)
        length = random.randint(50, 300)
        angle = random.uniform(0, 2*math.pi)
        end_x = start_x + length * math.cos(angle)
        end_y = start_y + length * math.sin(angle)
        
        for i in range(10):
            offset = i * 3
            self.draw.line(
                [start_x+offset, start_y+offset, end_x+offset, end_y+offset],
                fill=(255, 255, 255),
                width=2
            )

    def dimensional_shift(self):
        """30. 维度偏移（错位空间）"""
        for x in range(0, self.screen_width, 20):
            for y in range(0, self.screen_height, 20):
                dx = int(15 * math.sin(y/30 + time.time()))
                dy = int(15 * math.cos(x/30 + time.time()))
                self.draw.rectangle(
                    [x+dx, y+dy, x+20+dx, y+20+dy],
                    fill=(
                        (x + int(time.time()*100)) % 256,
                        (y + int(time.time()*80)) % 256,
                        (x + y + int(time.time()*60)) % 256
                    )
                )

    def entropy_noise(self):
        """31. 熵增噪点（信息熵增加效果）"""
        for _ in range(3000):
            x, y = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
            # 修复：确保chaos值在0-255范围内
            chaos = int(255 * abs(math.sin(time.time() % 5)))
            # 二次保险：限制取值范围
            chaos = max(1, min(255, chaos))  # 最小值设为1避免randint(0,0)错误
            
            self.draw.point(
                (x, y),
                fill=(
                    chaos,
                    random.randint(0, chaos),
                    random.randint(0, chaos)
                )
            )

    def bio_electric(self):
        """32. 生物电干扰（神经元放电模拟）"""
        for _ in range(150):
            start_x = random.randint(0, self.screen_width)
            start_y = random.randint(0, self.screen_height)
            length = random.randint(50, 200)
            angle = random.uniform(0, 2*math.pi)
            end_x = start_x + length * math.cos(angle)
            end_y = start_y + length * math.sin(angle)
            
            for i in range(3):  # 三层叠加
                offset = i * 2
                self.draw.line(
                    [start_x+offset, start_y+offset, end_x+offset, end_y+offset],
                    fill=(0, random.randint(200, 255), 0),
                    width=1
                )

    def compression_artifacts(self):
        """33. 压缩伪影（JPEG压缩失真）"""
        block_size = 16
        for x in range(0, self.screen_width, block_size):
            for y in range(0, self.screen_height, block_size):
                if random.random() > 0.7:
                    # 创建8x8的DCT块伪影
                    for i in range(8):
                        val = int(128 + 127 * math.sin(x/50 + y/50 + i/2))
                        self.draw.rectangle(
                            [x+i, y+i, x+block_size-i, y+block_size-i],
                            outline=(val, val, val),
                            width=1
                        )

    def motion_blur(self):
        """34. 动态模糊（运动残影）"""
        text = "MOTION"
        font = ImageFont.load_default(size=48)
        for i in range(5):
            alpha = 50 + i*40
            offset = i * 15
            self.draw.text(
                (self.screen_width//2 + offset, self.screen_height//2 + offset),
                text,
                fill=(255, 255, 255, alpha),
                font=font
            )

    def channel_offset(self):
        """35. 通道偏移（RGB分离）"""
        text = "CHANNEL"
        font = ImageFont.load_default(size=36)
        offsets = [(5, 0), (0, 5), (-5, 0)]
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for (dx, dy), color in zip(offsets, colors):
            x = self.screen_width//2 + dx + 3*math.sin(time.time())
            y = self.screen_height//2 + dy + 3*math.cos(time.time())
            self.draw.text((x, y), text, fill=color, font=font)

    def geometric_distortion(self):
        """36. 几何变形（非线性扭曲）"""
        for y in range(0, self.screen_height, 20):
            distortion = int(30 * math.sin(y/30 + time.time()))
            color = (
                int(128 + 127 * math.sin(y/50)),
                int(128 + 127 * math.sin(y/60 + 2)),
                int(128 + 127 * math.sin(y/70 + 4))
            )
            self.draw.line(
                [distortion, y, self.screen_width-distortion, y],
                fill=color,
                width=3
            )

    def pixel_sorting(self):
        """37. 像素排序（数据重组效果）"""
        for x in range(0, self.screen_width, 10):
            # 修复：确保高度值在合理范围内 (1到屏幕高度)
            column_height = int(self.screen_height * (0.2 + 0.6 * math.sin(x/100)))
            column_height = max(1, min(self.screen_height, column_height))  # 限制在1到屏幕高度之间
            
            # 修复：确保y1 > y0
            y0 = 0
            y1 = y0 + column_height
            
            self.draw.rectangle(
                [x, y0, x+8, y1],  # 明确使用y0和y1
                fill=(
                    x % 256,
                    (x*2) % 256,
                    (x*3) % 256
                )
            )

    def random_stripes(self):
        """38. 随机条纹（磁带损坏效果）"""
        for _ in range(50):
            x = random.randint(0, self.screen_width)
            width = random.randint(1, 20)
            color = (
                random.randint(100, 255),
                random.randint(0, 100),
                random.randint(100, 255)
            )
            self.draw.rectangle(
                [x, 0, x+width, self.screen_height],
                fill=color
            )

    def bloom_effect(self):
        """39. 光晕扩散（高光溢出）"""
        center_x, center_y = self.screen_width//2, self.screen_height//2
        for radius in range(50, 300, 50):
            alpha = min(60, 255 - radius)
            self.draw.ellipse(
                [center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                outline=(255, 255, 255, alpha),
                width=5
            )

    def time_delay_effect(self):
        """40. 时间延迟（信号延迟效果）"""
        for i in range(3):
            delay = i * 20
            alpha = 100 - i*30
            self.draw.rectangle(
                [delay, delay, self.screen_width-delay, self.screen_height-delay],
                outline=(0, 255, 255, alpha),
                width=3
            )

    def magnetic_distortion(self):
        """41. 磁场干扰（模拟磁化效果）"""
        center_x, center_y = self.screen_width//2, self.screen_height//2
        for angle in range(0, 360, 10):
            radius = min(self.screen_width, self.screen_height) // 3
            x = center_x + int(radius * math.cos(math.radians(angle + time.time()*50)))
            y = center_y + int(radius * math.sin(math.radians(angle + time.time()*50)))
            
            # 绘制动态磁力线
            self.draw.line(
                [center_x, center_y, x, y],
                fill=(0, random.randint(150, 255), 0),
                width=2
            )
            # 添加磁极光晕
            self.draw.ellipse(
                [x-15, y-15, x+15, y+15],
                fill=(0, 255, 0, 50),
                outline=(0, 200, 0)
            )

    def digital_decay(self):
        """42. 数字衰减（像素溶解）"""
        # 修复：限制衰减率在0.1-0.9之间
        decay_rate = 0.5 + 0.4 * math.sin(time.time())  # 原0.3 + 0.2*sin可能产生负值
        for x in range(0, self.screen_width, 5):
            for y in range(0, self.screen_height, 5):
                if random.random() < abs(decay_rate):  # 取绝对值保险
                    # 修复：颜色值限制在0-255
                    decay_color = min(255, max(0, int(255 * (1 - abs(decay_rate)))))
                    self.draw.rectangle(
                        [x, y, x+5, y+5],
                        fill=(decay_color, decay_color, decay_color)
                    )

    def analog_distortion(self):
        """43. 模拟失真（老式电视信号干扰）"""
        for y in range(0, self.screen_height, 3):
            # 修复：所有计算值限制在合理范围
            distortion = int(20 * math.sin(y/30 + time.time()*3)) % self.screen_width
            phase_shift = int(15 * math.cos(y/20 + time.time()*4)) % self.screen_height
            # 修复：颜色通道值限制在0-255
            r = int(128 + 127 * math.sin(y/50 + time.time())) % 256
            g = int(128 + 127 * math.sin(y/60 + time.time() + 2)) % 256
            b = int(128 + 127 * math.sin(y/70 + time.time() + 4)) % 256
            self.draw.line(
                [distortion, (y+phase_shift)%self.screen_height, 
                (self.screen_width-distortion)%self.screen_width, (y-phase_shift)%self.screen_height],
                fill=(r, g, b),
                width=2
            )

    def frequency_split(self):
        """44. 频带分离（RGB通道分离）"""
        text = "FREQUENCY"
        font = ImageFont.load_default(size=36)
        offsets = [
            (int(5*math.sin(time.time())), 0),
            (0, int(5*math.cos(time.time()))),
            (int(5*math.cos(time.time())), int(5*math.sin(time.time())))
        ]
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for (dx, dy), color in zip(offsets, colors):
            x = self.screen_width//2 + dx
            y = self.screen_height//2 + dy
            self.draw.text((x, y), text, fill=color, font=font)

    def packet_loss(self):
        """45. 数据包丢失（网络传输模拟）"""
        block_size = 20
        for x in range(0, self.screen_width, block_size):
            for y in range(0, self.screen_height, block_size):
                if random.random() > 0.7:
                    self.draw.rectangle(
                        [x, y, x+block_size, y+block_size],
                        fill=(
                            random.randint(0, 100),
                            random.randint(0, 100),
                            random.randint(0, 100)
                        )
                    )

    def negative(self):
        """46. 负片效果（颜色反转）"""
        # 创建临时图像缓冲区
        buffer = Image.new('RGB', (self.screen_width, self.screen_height))
        draw_buffer = ImageDraw.Draw(buffer)
        
        # 修复：确保effects是字典结构
        if isinstance(self.effects, list):
            effect_names = range(len(self.effects))  # 如果是列表，使用索引
        else:
            effect_names = list(self.effects.keys())  # 如果是字典，使用键
        
        # 随机选择一个特效执行（兼容列表和字典结构）
        random_effect = random.choice(effect_names)
        self.effects[random_effect]()
        
        # 应用负片效果
        for x in range(0, self.screen_width, 5):
            for y in range(0, self.screen_height, 5):
                r, g, b = self.pil_image.getpixel((x, y))
                draw_buffer.rectangle(
                    [x, y, x+5, y+5],
                    fill=(255-r, 255-g, 255-b)
                )
        self.pil_image.paste(buffer, (0, 0))

    def color_inversion(self):
        """47. 色彩反相（色轮反转）"""
        for x in range(0, self.screen_width, 10):
            for y in range(0, self.screen_height, 10):
                r, g, b = self.pil_image.getpixel((x, y))
                # 使用色轮反转公式
                max_val = max(r, g, b)
                min_val = min(r, g, b)
                new_r = max_val + min_val - r
                new_g = max_val + min_val - g
                new_b = max_val + min_val - b
                self.draw.rectangle(
                    [x, y, x+10, y+10],
                    fill=(new_r, new_g, new_b)
                )

    def raster_distortion(self):
        """48. 光栅变形（扫描线扭曲）"""
        for y in range(0, self.screen_height, 2):
            wave = int(30 * math.sin(y/50 + time.time()*2))
            self.draw.line(
                [wave, y, self.screen_width-wave, y],
                fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                width=1
            )

    def pixelation(self):
        """49. 像素化（马赛克增强）"""
        block_size = 15
        for x in range(0, self.screen_width, block_size):
            for y in range(0, self.screen_height, block_size):
                # 获取区块平均颜色
                r_total = g_total = b_total = 0
                count = 0
                for i in range(block_size):
                    for j in range(block_size):
                        if x+i < self.screen_width and y+j < self.screen_height:
                            r, g, b = self.pil_image.getpixel((x+i, y+j))
                            r_total += r
                            g_total += g
                            b_total += b
                            count += 1
                avg_color = (r_total//count, g_total//count, b_total//count)
                # 绘制统一色块
                self.draw.rectangle(
                    [x, y, x+block_size, y+block_size],
                    fill=avg_color
                )

    def dynamic_color_blocks(self):
        """50. 动态色块（抽象艺术效果）"""
        for _ in range(20):
            x = random.randint(0, self.screen_width - 100)
            y = random.randint(0, self.screen_height - 100)
            width = random.randint(50, 200)
            height = random.randint(50, 200)
            # 生成动态渐变颜色
            color1 = (
                int(255 * abs(math.sin(time.time()))),
                int(255 * abs(math.cos(time.time()*0.7))),
                int(255 * abs(math.sin(time.time()*1.3)))
            )
            color2 = (
                int(255 * abs(math.cos(time.time()*0.5))),
                int(255 * abs(math.sin(time.time()*1.1))),
                int(255 * abs(math.cos(time.time()*0.9)))
            )
            # 绘制渐变矩形
            for i in range(height):
                ratio = i / height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                self.draw.line(
                    [x, y+i, x+width, y+i],
                    fill=(r, g, b),
                    width=1
                )

if __name__ == "__main__":
    ScreenErrorSimulator()