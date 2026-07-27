import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("Draw Circles on Canvas")

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算画布的大小
canvas_width = 800
canvas_height = 600

# 计算画布在屏幕上的位置，使其居中显示
x_position = (screen_width - canvas_width) // 2
y_position = (screen_height - canvas_height) // 2

# 设置主窗口的大小和位置
root.geometry(f"{canvas_width}x{canvas_height}+{x_position}+{y_position}")

# 创建一个 Canvas 组件，背景颜色为黑色
canvas = tk.Canvas(root, bg="black", width=canvas_width, height=canvas_height)
canvas.pack()

# 计算画布的中心坐标
center_x = canvas_width // 2
center_y = canvas_height // 2

# 定义浅绿色的颜色代码
light_green = "#90EE90"

# 定义中心圆的半径
center_radius = 50

# 在中心绘制一个浅绿色的实心圆
canvas.create_oval(center_x - center_radius, center_y - center_radius,
                   center_x + center_radius, center_y + center_radius,
                   fill=light_green, outline="")

# 定义空心圆的起始半径和半径增量
start_radius = center_radius + 20
radius_increment = 20

# 绘制 5 个空心圆
for i in range(5):
    current_radius = start_radius + i * radius_increment
    canvas.create_oval(center_x - current_radius, center_y - current_radius,
                       center_x + current_radius, center_y + current_radius,
                       outline="white")

# 运行主循环
root.mainloop()