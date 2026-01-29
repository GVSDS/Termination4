#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <tchar.h>

#pragma comment(linker, "/subsystem:windows /entry:mainCRTStartup")

// 从完整路径中提取目录
BOOL GetDirectoryFromPath(const char* fullPath, char* directory, size_t dirSize) {
    if (!fullPath || !directory || dirSize == 0) return FALSE;
    
    const char* lastSlash = strrchr(fullPath, '\\');
    if (!lastSlash) {
        strncpy(directory, ".", dirSize);
        return TRUE;
    }
    
    size_t dirLength = lastSlash - fullPath;
    if (dirLength >= dirSize) {
        return FALSE;
    }
    
    strncpy(directory, fullPath, dirLength);
    directory[dirLength] = '\0';
    return TRUE;
}

// 安全复制文件
BOOL SecureCopyFile(const char* srcPath, const char* dstPath) {
    if (!srcPath || !dstPath) return FALSE;

    HANDLE hSrc = CreateFileA(
        srcPath,
        GENERIC_READ,
        FILE_SHARE_READ,
        NULL,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL | FILE_FLAG_SEQUENTIAL_SCAN,
        NULL
    );
    
    if (hSrc == INVALID_HANDLE_VALUE) {
        return FALSE;
    }

    HANDLE hDst = CreateFileA(
        dstPath,
        GENERIC_WRITE,
        0,
        NULL,
        CREATE_ALWAYS,
        FILE_ATTRIBUTE_NORMAL | FILE_FLAG_WRITE_THROUGH,
        NULL
    );
    
    if (hDst == INVALID_HANDLE_VALUE) {
        CloseHandle(hSrc);
        return FALSE;
    }

    BYTE buffer[8192];
    DWORD bytesRead, bytesWritten;
    BOOL result = TRUE;

    while (ReadFile(hSrc, buffer, sizeof(buffer), &bytesRead, NULL) && bytesRead > 0) {
        if (!WriteFile(hDst, buffer, bytesRead, &bytesWritten, NULL) || bytesWritten != bytesRead) {
            result = FALSE;
            break;
        }
    }

    FlushFileBuffers(hDst);
    
    CloseHandle(hSrc);
    CloseHandle(hDst);

    if (!result) {
        DeleteFileA(dstPath);
    }
    
    return result;
}

// 高级启动程序
BOOL AdvancedLaunchProgram(const char* exePath) {
    if (!exePath || *exePath == '\0') return FALSE;

    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi = {0};

    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_HIDE;

    char cmdLine[MAX_PATH + 2];
    if (strchr(exePath, ' ') != NULL) {
        snprintf(cmdLine, sizeof(cmdLine), "\"%s\"", exePath);
    } else {
        strncpy(cmdLine, exePath, sizeof(cmdLine) - 1);
    }
    cmdLine[sizeof(cmdLine) - 1] = '\0';

    char workingDir[MAX_PATH];
    if (!GetDirectoryFromPath(exePath, workingDir, MAX_PATH)) {
        strcpy(workingDir, ".");
    }

    DWORD creationFlags = CREATE_NO_WINDOW | DETACHED_PROCESS;

    if (CreateProcessA(
        NULL,
        cmdLine,
        NULL,
        NULL,
        FALSE,
        creationFlags,
        NULL,
        workingDir,
        &si,
        &pi)) {
        CloseHandle(pi.hThread);
        CloseHandle(pi.hProcess);
        return TRUE;
    }
    
    DWORD err = GetLastError();

    if (err == ERROR_ACCESS_DENIED || err == ERROR_ELEVATION_REQUIRED) {
        char rundllCmd[MAX_PATH + 100];
        snprintf(rundllCmd, sizeof(rundllCmd), "rundll32.exe shell32.dll,ShellExec_RunDLL \"%s\"", exePath);
        rundllCmd[sizeof(rundllCmd) - 1] = '\0';
        
        if (CreateProcessA(
            NULL,
            rundllCmd,
            NULL,
            NULL,
            FALSE,
            creationFlags,
            NULL,
            workingDir,
            &si,
            &pi)) {
            CloseHandle(pi.hThread);
            CloseHandle(pi.hProcess);
            return TRUE;
        }
        err = GetLastError();
    }

    if (err == ERROR_FILE_NOT_FOUND || err == ERROR_PATH_NOT_FOUND) {
        char explorerCmd[MAX_PATH + 100];
        snprintf(explorerCmd, sizeof(explorerCmd), "explorer.exe \"%s\"", exePath);
        explorerCmd[sizeof(explorerCmd) - 1] = '\0';
        
        if (CreateProcessA(
            NULL,
            explorerCmd,
            NULL,
            NULL,
            FALSE,
            creationFlags,
            NULL,
            workingDir,
            &si,
            &pi)) {
            CloseHandle(pi.hThread);
            CloseHandle(pi.hProcess);
            return TRUE;
        }
        err = GetLastError();
    }

    if (err == ERROR_MOD_NOT_FOUND || err == ERROR_DLL_NOT_FOUND) {
        char envBlock[MAX_PATH * 2];
        char systemPath[MAX_PATH];
        GetSystemDirectoryA(systemPath, MAX_PATH);
        snprintf(envBlock, sizeof(envBlock), "PATH=%s;%s\0\0", workingDir, systemPath);
        envBlock[sizeof(envBlock) - 1] = '\0';
        
        if (CreateProcessA(
            NULL,
            cmdLine,
            NULL,
            NULL,
            FALSE,
            creationFlags,
            envBlock,
            workingDir,
            &si,
            &pi)) {
            CloseHandle(pi.hThread);
            CloseHandle(pi.hProcess);
            return TRUE;
        }
        err = GetLastError();
    }

    char errorMsg[512];
    const char* errorDesc = "Unknown error";
    
    switch (err) {
        case ERROR_FILE_NOT_FOUND: errorDesc = "File not found"; break;
        case ERROR_PATH_NOT_FOUND: errorDesc = "Path not found"; break;
        case ERROR_ACCESS_DENIED: errorDesc = "Access denied (try running as admin)"; break;
        case ERROR_ELEVATION_REQUIRED: errorDesc = "Administrator privileges required"; break;
        case ERROR_BAD_EXE_FORMAT: errorDesc = "Invalid executable format"; break;
        case ERROR_MOD_NOT_FOUND: 
        case ERROR_DLL_NOT_FOUND: errorDesc = "Required DLL not found"; break;
    }
    
    snprintf(errorMsg, sizeof(errorMsg), 
            "Failed to launch program\nPath: %s\nWorking Dir: %s\nError %d: %s", 
            exePath, workingDir, err, errorDesc);
    
    printf("%s\n", errorMsg);
    return FALSE;
}

int main(int argc, char* argv[]) {
    // 检查参数数量
    if (argc != 4) {
        printf(
            "Usage: Program.exe <delay_seconds> <source_path> <dest_path>\n\n"
            "Example: Program.exe 5 C:\\temp\\app.exe C:\\Windows\\Temp\\app.exe\n"
        );
        return 1;
    }

    // 解析延迟时间参数
    DWORD delaySeconds = atoi(argv[1]);
    if (delaySeconds == 0 && strcmp(argv[1], "0") != 0) {
        printf("Invalid delay value: %s\n", argv[1]);
        return 1;
    }

    // 使用用户指定的延迟时间
    Sleep(delaySeconds * 1000);

    // 检查源文件是否存在（修正参数索引错误）
    DWORD fileAttributes = GetFileAttributesA(argv[2]);
    if (fileAttributes == INVALID_FILE_ATTRIBUTES) {
        printf("Source file not found: %s\n", argv[2]);
        // 尝试直接启动源文件（如果存在）
        if (!AdvancedLaunchProgram(argv[2])) {
            return 3;
        }
        return 0;
    }

    // 复制文件并启动（修正参数索引错误）
    if (SecureCopyFile(argv[2], argv[3])) {
        Sleep(1 * 1000); // 短暂延迟确保文件写入完成
        if (!AdvancedLaunchProgram(argv[3])) {
            return 3;
        }
        return 0;
    } else {
        DWORD copyErr = GetLastError();
        char errorMsg[256];
        const char* errorDesc = "Unknown error";
        
        switch (copyErr) {
            case ERROR_FILE_NOT_FOUND: errorDesc = "Source file not found"; break;
            case ERROR_PATH_NOT_FOUND: errorDesc = "Path not found"; break;
            case ERROR_ACCESS_DENIED: errorDesc = "Access denied"; break;
            case ERROR_SHARING_VIOLATION: errorDesc = "File in use by another process"; break;
            case ERROR_DISK_FULL: errorDesc = "Disk full"; break;
        }
        
        snprintf(errorMsg, sizeof(errorMsg), 
                "Failed to copy file\nFrom: %s\nTo: %s\nError %d: %s", 
                argv[2], argv[3], copyErr, errorDesc);
        
        printf("%s\n", errorMsg);
        return 2;
    }
}
