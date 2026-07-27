import sys
import os

MARKER = b"MAKEND"
FILE_START = b"FILESTART"

def hexReverseEncrypt(data):
    """Reverse the order of bytes (simple hex reversal)"""
    return data[::-1]

def main():
    if len(sys.argv) != 4:
        print("Usage: python combine.py <input_exe> <resource_file> <output_exe>")
        return
    
    input_exe = sys.argv[1]
    resource_file = sys.argv[2]
    output_exe = sys.argv[3]
    
    # Get resource filename
    filename = os.path.basename(resource_file)
    filename_bytes = filename.encode('utf-8')
    
    # Read original exe
    with open(input_exe, 'rb') as f:
        exe_data = f.read()
    
    # Read resource file and encrypt it
    with open(resource_file, 'rb') as f:
        resource_data = f.read()
    encrypted_data = hexReverseEncrypt(resource_data)
    
    # Build combined data
    combined_data = (
        exe_data +
        MARKER +
        filename_bytes +
        FILE_START +
        encrypted_data
    )
    
    # Write output file
    with open(output_exe, 'wb') as f:
        f.write(combined_data)
    
    print(f"Successfully combined {input_exe} and {resource_file} into {output_exe}")

if __name__ == "__main__":
    main()