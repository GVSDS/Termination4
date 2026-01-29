import tkinter as tk
import ctypes

# 定义Windows API常量
GWL_STYLE = -16
GWL_EXSTYLE = -20
WS_SYSMENU = 0x00080000
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000
SWP_FLAGS = 0x0020 | 0x0002 | 0x0001  # SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE

# 创建窗口
root = tk.Tk()
root.title("QNMD WindowTools")
root.update_idletasks()  # 确保窗口已绘制

try:
    # 获取窗口句柄
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    
    # 1. 移除系统菜单（包含最小化、最大化和关闭按钮）
    style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWL_STYLE)
    ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWL_STYLE, style & ~WS_SYSMENU)
    
    # 2. 移除任务栏显示
    ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ex_style = (ex_style & ~WS_EX_APPWINDOW) | WS_EX_TOOLWINDOW
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)
    
    # 3. 设置窗口无法获得焦点
    ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_NOACTIVATE)
    
    # 刷新窗口样式
    ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, SWP_FLAGS)

except Exception as e:
    print(f"发生错误: {e}")

root.mainloop()

"""
import tkinter as tk
import ctypes

# 定义一些 Windows API 相关的常量和函数
SW_HIDE = 0
SW_SHOW = 5
FINDWINDOW = ctypes.windll.user32.FindWindowW
SHOWWINDOW = ctypes.windll.user32.ShowWindow

# 创建主窗口
root = tk.Tk()
root.title("隐藏任务栏示例")

# 隐藏任务栏的函数
def hide_taskbar():
    hWnd = FINDWINDOW("Shell_TrayWnd", None)
    SHOWWINDOW(hWnd, SW_HIDE)

# 显示任务栏的函数
def show_taskbar():
    hWnd = FINDWINDOW("Shell_TrayWnd", None)
    SHOWWINDOW(hWnd, SW_SHOW)

# 创建隐藏和显示任务栏的按钮
hide_button = tk.Button(root, text="隐藏任务栏", command=hide_taskbar)
hide_button.pack(pady=10)

show_button = tk.Button(root, text="显示任务栏", command=show_taskbar)
show_button.pack(pady=10)

# 运行主循环
root.mainloop()"""
