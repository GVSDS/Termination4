import sys
import os

MARKER = b"MAKEND"
FILE_START = b"FILESTART"

def main():
    if len(sys.argv) != 4:
        print("Usage: python combine.py <input_exe> <resource_file> <output_exe>")
        return
    
    input_exe = sys.argv[1]
    resource_file = sys.argv[2]
    output_exe = sys.argv[3]
    
    # 获取资源文件名
    filename = os.path.basename(resource_file)
    filename_bytes = filename.encode('utf-8')
    
    # 读取原始exe
    with open(input_exe, 'rb') as f:
        exe_data = f.read()
    
    # 读取资源文件
    with open(resource_file, 'rb') as f:
        resource_data = f.read()
    
    # 构建附加数据
    combined_data = (
        exe_data +
        MARKER +
        filename_bytes +
        FILE_START +
        resource_data
    )
    
    # 写入输出文件
    with open(output_exe, 'wb') as f:
        f.write(combined_data)
    
    print(f"Successfully combined {input_exe} and {resource_file} into {output_exe}")

if __name__ == "__main__":
    main()