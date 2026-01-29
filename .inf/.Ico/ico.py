import pefile
import struct

def replace_exe_icon(input_exe_path, input_ico_path, output_exe_path):
    """
    替换EXE文件的图标
    :param input_exe_path: 输入EXE文件路径
    :param input_ico_path: 输入ICO文件路径
    :param output_exe_path: 输出EXE文件路径
    """
    try:
        # 1. 读取ICO文件
        with open(input_ico_path, 'rb') as f:
            ico_data = f.read()
        
        # 2. 解析PE文件
        pe = pefile.PE(input_exe_path)
        
        # 3. 定位资源段
        resource_section = None
        for section in pe.sections:
            if b'.rsrc' in section.Name:
                resource_section = section
                break
        
        if not resource_section:
            raise ValueError("未找到资源段(.rsrc)")
        
        # 4. 查找图标资源目录
        resource_dir = pe.DIRECTORY_ENTRY_RESOURCE
        icon_group = None
        for entry in resource_dir.entries:
            if entry.id == 3:  # RT_ICON
                icon_group = entry
                break
        
        if not icon_group:
            raise ValueError("未找到图标资源目录")
        
        # 5. 计算资源段内偏移量
        icon_offset = icon_group.directory.entries[0].data.struct.OffsetToData
        icon_rva = resource_section.VirtualAddress + icon_offset - resource_section.PointerToRawData
        
        # 6. 替换图标数据
        pe.set_bytes_at_rva(icon_rva, ico_data)
        
        # 7. 保存修改后的文件
        pe.write(output_exe_path)
        pe.close()
        
        print(f"图标替换成功，输出文件: {output_exe_path}")
    
    except Exception as e:
        print(f"错误: {str(e)}")

replace_exe_icon("./main.exe", r"C:\Users\Lenovo\Desktop\Termination4\icon.ico", "./o.exe")