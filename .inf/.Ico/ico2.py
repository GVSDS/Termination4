import win32api
import win32con
import struct

def parse_ico(ico_data):
    reserved, type_ico, count = struct.unpack('<HHH', ico_data[:6])
    if type_ico != 1:
        raise ValueError("文件不是有效的ICO格式")
    entries = []
    images = []
    offset = 6  # ICONDIR头占6字节
    
    for i in range(count):
        # 解析每个图标的ICONDIRENTRY（16字节）
        entry = struct.unpack('<BBBBHHLL', ico_data[offset:offset+16])
        width = entry[0] if entry[0] != 0 else 256
        height = entry[1] if entry[1] != 0 else 256
        color_count = entry[2]
        reserved_entry = entry[3]
        planes = entry[4]
        bit_count = entry[5]
        size = entry[6]
        image_offset = entry[7]
        
        # 提取图像数据
        image_data = ico_data[image_offset:image_offset + size]
        images.append(image_data)
        
        # 构建GRPICONDIRENTRY结构（资源ID从1开始）
        grp_entry = struct.pack('<BBBBHHLL',
                                width if width != 256 else 0,
                                height if height != 256 else 0,
                                color_count,
                                reserved_entry,
                                planes,
                                bit_count,
                                size,
                                i + 1)  # 资源ID
        entries.append(grp_entry)
        offset += 16
    
    # 构建GRPICONDIR头
    grp_dir = struct.pack('<HHH', reserved, type_ico, count)
    grp_data = grp_dir + b''.join(entries)
    
    return grp_data, images

def replace_exe_icon(exe_path, icon_path):
    """替换exe文件的图标"""
    with open(icon_path, 'rb') as f:
        ico_data = f.read()
    
    # 解析ICO文件
    grp_data, icon_images = parse_ico(ico_data)
    
    # 开始更新资源
    h_update = win32api.BeginUpdateResource(exe_path, False)
    try:
        # 更新RT_GROUP_ICON资源（假设资源ID为1）
        win32api.UpdateResource(
            h_update, win32con.RT_GROUP_ICON, 1, grp_data, win32con.LANG_NEUTRAL
        )
        # 更新每个RT_ICON资源
        for idx, img_data in enumerate(icon_images):
            res_id = idx + 1
            win32api.UpdateResource(
                h_update, win32con.RT_ICON, res_id, img_data, win32con.LANG_NEUTRAL
            )
    finally:
        # 提交更改
        win32api.EndUpdateResource(h_update, False)

replace_exe_icon("./main.exe", r"C:\Users\Lenovo\Desktop\Termination4\icon.ico")