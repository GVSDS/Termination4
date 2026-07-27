import os
import sys

def batch_replace(root_dir, old_str, new_str):
    """
    批量替换指定目录下所有文件的内容和文件名中的指定字符串
    
    参数:
    root_dir: 根目录路径
    old_str: 要替换的旧字符串
    new_str: 替换后的新字符串
    """
    # 获取当前脚本的文件名，用于忽略自身
    script_name = os.path.basename(sys.argv[0])
    
    # 先收集所有文件路径，避免在遍历过程中因文件名变化导致问题
    file_paths = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # 忽略脚本自身
            if filename == script_name:
                continue
            file_paths.append(os.path.join(dirpath, filename))
    
    # 处理文件内容替换
    for file_path in file_paths:
        try:
            # 尝试以文本模式打开文件并读取内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 如果内容中包含要替换的字符串，则进行替换并写入
            if old_str in content:
                new_content = content.replace(old_str, new_str)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"已替换内容: {file_path}")
        except UnicodeDecodeError:
            # 二进制文件可能会解码失败，跳过处理
            print(f"跳过二进制文件: {file_path}")
        except Exception as e:
            print(f"处理文件内容出错 {file_path}: {str(e)}")
    
    # 处理文件名替换
    for old_path in file_paths:
        dirname = os.path.dirname(old_path)
        old_filename = os.path.basename(old_path)
        
        # 如果文件名中包含要替换的字符串，则进行替换
        if old_str in old_filename:
            new_filename = old_filename.replace(old_str, new_str)
            new_path = os.path.join(dirname, new_filename)
            
            # 避免重名
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                print(f"已重命名文件: {old_path} -> {new_path}")
            else:
                print(f"跳过重命名，文件已存在: {new_path}")

if __name__ == "__main__":
    # 设置要处理的根目录，默认为当前目录
    root_directory = os.getcwd()
    
    # 要替换的字符串
    old_string = "winvnc"
    new_string = "T2SRFB"
    
    print(f"开始批量替换: {old_string} -> {new_string}")
    print(f"处理目录: {root_directory}")
    
    batch_replace(root_directory, old_string, new_string)
    
    print("批量替换完成")
