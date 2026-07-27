import tkinter as tk
import math
import time
import random
from tkinter import Canvas

class SwingingClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Swinging Clock")
        # Set to fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="black")
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Main canvas
        self.canvas = Canvas(root, width=self.screen_width, height=self.screen_height, 
                            bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Clock parameters
        self.clock_radius = min(self.screen_width, self.screen_height) * 0.3
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        self.clock_color = "white"
        self.bg_color = "black"
        
        # Swing parameters
        self.swing_angle = 0
        self.swing_direction = 1
        self.swing_speed = 2
        self.max_swing = 30  # Max swing angle
        
        # Wave parameters
        self.wave_radius = self.clock_radius + 20
        self.wave_width = 100  # Increased wave width
        self.wave_spacing = 30  # Wave spacing
        self.wave_alpha = 0
        self.wave_growing = True
        self.waves = []  # To track multiple waves
        
        # Time and animation parameters
        self.start_time = time.time()
        self.current_speed = -30 * 60  # Start at 30 minutes per second counter-clockwise
        self.last_update_time = time.time()
        self.total_elapsed = 0  # Track total elapsed time in clock's perspective
        
        # Hand angles for smooth animation
        self.smooth_hour_angle = 0
        self.smooth_minute_angle = 0
        
        # Draw initial clock
        self.draw_clock()
        
        # Start animation loop
        self.animate()
        
        # Bind escape key to exit fullscreen
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        self.root.bind('<F11>', lambda e: self.root.attributes('-fullscreen', True))

    def draw_clock(self):
        """Draw the clock"""
        self.canvas.delete("all")
        
        # Draw wave effects
        for wave in self.waves:
            radius, alpha = wave
            if alpha > 0:
                wave_color = self.get_wave_color(alpha)
                self.canvas.create_oval(
                    self.center_x - radius,
                    self.center_y - radius,
                    self.center_x + radius,
                    self.center_y + radius,
                    outline=wave_color,
                    width=self.wave_width
                )
        
        # Draw clock outer circle
        self.canvas.create_oval(
            self.center_x - self.clock_radius,
            self.center_y - self.clock_radius,
            self.center_x + self.clock_radius,
            self.center_y + self.clock_radius,
            outline=self.clock_color,
            width=3
        )
        
        # Draw clock center point
        self.canvas.create_oval(
            self.center_x - 5,
            self.center_y - 5,
            self.center_x + 5,
            self.center_y + 5,
            fill=self.clock_color,
            outline=self.clock_color
        )
        
        # Draw clock numbers (counter-clockwise)
        for i in range(1, 13):
            angle = math.radians(-(i * 30 - 90))  # Negative for counter-clockwise
            x = self.center_x + (self.clock_radius - 30) * math.cos(angle)
            y = self.center_y + (self.clock_radius - 30) * math.sin(angle)
            self.canvas.create_text(x, y, text=str(i), fill=self.clock_color, 
                                  font=("Arial", 12, "bold"))
        
        # Draw clock hands
        self.draw_clock_hands()
    
    def draw_clock_hands(self):
        """Draw clock hands with smooth animation (always counter-clockwise)"""
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Update total elapsed time (always negative)
        self.total_elapsed += elapsed * self.current_speed
        
        # Calculate accelerated time components (always negative)
        accelerated_hours = self.total_elapsed / 3600
        accelerated_minutes = self.total_elapsed / 60
        
        # Calculate angles (negative for counter-clockwise)
        hour_angle = -((accelerated_hours % 12) * 30)  # 30 degrees per hour
        minute_angle = -((accelerated_minutes % 60) * 6)  # 6 degrees per minute
        
        # Smooth transitions for hands
        self.smooth_hour_angle = self.smooth_hour_angle * 0.8 + hour_angle * 0.2
        self.smooth_minute_angle = self.smooth_minute_angle * 0.7 + minute_angle * 0.3
        
        # Add swing effect
        hour_angle_swing = math.radians(self.smooth_hour_angle - 90 + self.swing_angle)
        minute_angle_swing = math.radians(self.smooth_minute_angle - 90 + self.swing_angle)
        
        # Hour hand
        hour_x = self.center_x + (self.clock_radius * 0.5) * math.cos(hour_angle_swing)
        hour_y = self.center_y + (self.clock_radius * 0.5) * math.sin(hour_angle_swing)
        self.canvas.create_line(
            self.center_x, self.center_y, hour_x, hour_y,
            fill=self.clock_color, width=4
        )
        
        # Minute hand
        minute_x = self.center_x + (self.clock_radius * 0.7) * math.cos(minute_angle_swing)
        minute_y = self.center_y + (self.clock_radius * 0.7) * math.sin(minute_angle_swing)
        self.canvas.create_line(
            self.center_x, self.center_y, minute_x, minute_y,
            fill=self.clock_color, width=2
        )
    
    def get_wave_color(self, alpha):
        """Get wave color based on alpha"""
        alpha_hex = hex(int(alpha * 255))[2:].zfill(2)
        return f"#{alpha_hex}{alpha_hex}{alpha_hex}"
    
    def animate(self):
        """Animation loop"""
        # Update swing angle
        self.swing_angle += self.swing_speed * self.swing_direction
        
        # Check if direction needs to reverse
        if abs(self.swing_angle) >= self.max_swing:
            self.swing_direction *= -1
            self.shake_screen()
            self.invert_colors()
            self.start_wave()
        
        # Update wave effects
        new_waves = []
        for wave in self.waves:
            radius, alpha = wave
            if alpha > 0:
                radius += 15  # Wave expansion speed
                alpha -= 0.02  # Fade speed
                if alpha > 0:
                    new_waves.append((radius, alpha))
        
        # Add new wave if needed (based on spacing)
        if not self.waves or (self.waves[-1][0] >= self.wave_radius + self.wave_spacing):
            self.waves.append((self.wave_radius, 1.0))
        
        self.waves = new_waves
        
        # Redraw clock
        self.draw_clock()
        
        # Continue animation
        self.root.after(16, self.animate)  # ~60fps
    
    def shake_screen(self):
        """Screen shake effect"""
        original_x = self.root.winfo_x()
        original_y = self.root.winfo_y()
        
        for i in range(5):
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-5, 5)
            self.root.geometry(f"+{original_x + offset_x}+{original_y + offset_y}")
            self.root.update()
            time.sleep(0.02)
        
        self.root.geometry(f"+{original_x}+{original_y}")
    
    def invert_colors(self):
        """Invert colors without affecting clock direction"""
        self.clock_color, self.bg_color = self.bg_color, self.clock_color
        self.canvas.config(bg=self.bg_color)
    
    def start_wave(self):
        """Start a new wave effect"""
        self.waves.append((self.wave_radius, 1.0))

if __name__ == "__main__":
    root = tk.Tk()
    app = SwingingClock(root)
    root.mainloop()