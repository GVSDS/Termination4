import pygame
import data
from PIL import Image
from os import makedirs, remove
from shutil import rmtree
from os.path import isdir
from playsound import playsound
from random import randint
from _thread import start_new_thread as startThread
from win32api import GetSystemMetrics
from win32gui import SetForegroundWindow, ShowWindow, FindWindow, GetWindowText, EnumWindows, PostMessage
from win32con import SM_CXSCREEN, SM_CYSCREEN, SW_SHOW, WM_CLOSE


# 写出数据到文件
if not isdir(r"C:\cat"):  # Load cat frame
    makedirs(r"C:\cat")
f = None
for i in range(6):
    f = open(fr"C:\cat\cat{i}.png", "wb+")
    f.write(data.cat_frame_data[i])
    f.close()

if not isdir(r"C:\star"):  # Load star frame
    makedirs(r"C:\star")
for i in range(6):
    f = open(fr"C:\star\star{i}.png", "wb+")
    f.write(data.star_frame_data[i])
    f.close()
with open(r"C:\music.wma", "wb+") as f:
    f.write(data.music_data)


# 更改图片大小
image = None
image_resize = 5
for i in range(6):
    image = Image.open(fr"C:\cat\cat{i}.png")
    image = image.resize((image.size[0]*image_resize,
                          image.size[1]*image_resize),
                         Image.NEAREST)
    image.save(fr"C:\cat\cat{i}.png")

# 获取屏幕分辨率
dis_width = GetSystemMetrics(SM_CXSCREEN)
dis_height = GetSystemMetrics(SM_CYSCREEN)

# 初始化窗口
pygame.init()
screen = pygame.display.set_mode((dis_width, dis_height), pygame.FULLSCREEN)
pygame.display.set_caption("Nyan Cat")
pygame.mouse.set_visible(False)
hwnd = FindWindow(None, "Nyan Cat")
SetForegroundWindow(hwnd)
ShowWindow(hwnd, SW_SHOW)

# 获取猫猫大小
image = Image.open(r"C:\cat\cat0.png")
cat_size = image.size
image.close()

# 初始化变量
star_list = []  # 星星列表
cat_frame_list = []  # 猫猫帧列表
star_frame_list = []  # 星星帧列表
frame_count = 0  # 帧计数
star_change_count = 6  # 星星变化帧
cat_change_count = 3  # 猫猫变化帧
cat = [(dis_width-cat_size[0])//2, (dis_height-cat_size[1])//2, 0]  # 猫猫位置
x_speed = 4  # x速度
y_speed = 4  # y速度
move_viscous = 6  # 移动润滑指数
friction_viscous = 15  # 停止润滑指数
move_speed = 3
key_down = {"up": False,
            "down": False,
            "left": False,
            "right": False}

# 加载彩虹猫,星星的帧
for i in range(6):
    cat_frame_list.append(pygame.image.load(fr"C:\cat\cat{i}.png"))
    star_frame_list.append(pygame.image.load(fr"C:\star\star{i}.png"))

# 生成星星
for _ in range(20):
    # 1.x坐标,2.y坐标,3.造型序号
    temp = [randint(0, dis_width), randint(10, dis_height-50), randint(0, 5)]
    star_list.append(temp)


# 播放音乐
def play_music():
    while run:
        playsound(r"C:\music.wma")


# 显示星星
def draw_star():
    global star_list
    del_list = []
    star = None
    for i in range(len(star_list)):
        star = star_list[i]
        screen.blit(star_frame_list[star[2]], (star[0], star[1]))
        star[0] -= 12  # 向左移动
        if frame_count % star_change_count == 0:
            star[2] += 1  # 下一个造型
            star[2] = star[2] % 6  # 求余运算
        if star[0] < -200:  # 超出屏幕删除
            del_list.append(i)
    del_list.reverse()
    for i in del_list:
        star_list.pop(i)


# 显示猫
def draw_cat():
    global cat
    screen.blit(cat_frame_list[cat[2]], (cat[0], cat[1]))
    if frame_count % cat_change_count == 0:
        cat[2] += 1
        cat[2] %= 6


# 显示彩虹
def draw_tail(m):
    x = cat[0]
    y = cat[1] + 10

    color_list = [(255, 0, 0),
                  (255, 154, 0),
                  (255, 240, 0),
                  (38, 221, 0),
                  (0, 144, 255),
                  (104, 68, 255)]
    while True:
        for i in range(6):
            pygame.draw.rect(screen, color_list[i], [x, y, 40, 15])
            y += 15
        x -= 40
        y = cat[1] + 10
        if m:
            y += 5
            m = 0
        else:
            m = 1
        if x < -200:
            break


# 响应事件
def check_event():
    global run
    global key_down
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                key_down["up"] = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                key_down["down"] = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                key_down["left"] = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                key_down["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                key_down["up"] = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                key_down["down"] = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                key_down["left"] = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                key_down["right"] = False


# 移动猫猫
def move_cat():
    global key_down
    global y_speed
    global x_speed

    if True in key_down.values():
        if key_down["up"]:
            y_speed -= (y_speed)/move_viscous
        if key_down["down"]:
            y_speed += (8-y_speed)/move_viscous
        if key_down["left"]:
            x_speed -= x_speed/move_viscous
        if key_down["right"]:
            x_speed += (8-x_speed)/move_viscous
    else:
        x_speed -= (x_speed-4)/friction_viscous
        y_speed -= (y_speed-4)/friction_viscous

    cat[0] += (x_speed-4)*move_speed
    cat[1] += (y_speed-4)*move_speed


def del_wins():
    hwnds = []
    EnumWindows(lambda hWnd, param: param.append(hWnd), hwnds)  # 获取窗口句柄列表
    for hwnd in hwnds:
        if GetWindowText(hwnd) == "MEMZ":
            PostMessage(hwnd, WM_CLOSE)


# 进入主循环
startThread(del_wins, ())
startThread(play_music, ())  # 播放音乐
run = True
while run:
    check_event()
    move_cat()

    # 绘制
    pygame.draw.rect(screen, (0, 49, 105), [0, 0, dis_width, dis_height])
    if frame_count % 7 == 0:
        # 1:x坐标,2:y坐标,3:造型序号
        temp = [dis_width+200, randint(45, dis_height-50), randint(0, 5)]
        star_list.append(temp)
    draw_star()
    draw_tail(frame_count % 10 < 5)
    draw_cat()
    # 绘制

    frame_count += 1
    pygame.display.update()
    pygame.time.Clock().tick(60)
pygame.quit()

# 移除文件
try:
    rmtree(r"C:\cat")
except:
    pass
try:
    rmtree(r"C:\star")
except:
    pass
try:
    remove(r"C:\music.wma")
except:
    pass
