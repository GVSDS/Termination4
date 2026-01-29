#include <windows.h>
#include <shellapi.h>
#include <stdio.h>

int main() {
    char rootPath[MAX_PATH];
    GetModuleFileNameA(NULL, rootPath, MAX_PATH);
    rootPath[3] = '\0';

    char exePath[MAX_PATH];
    snprintf(exePath, MAX_PATH, "%s.Termination\\Termination.exe", rootPath);

    SHELLEXECUTEINFO sei = {0};
    sei.cbSize = sizeof(SHELLEXECUTEINFO);
    sei.fMask = SEE_MASK_NOCLOSEPROCESS;
    sei.lpVerb = "runas";
    sei.lpFile = exePath;
    sei.lpDirectory = rootPath;
    sei.nShow = SW_HIDE;

    if (!ShellExecuteEx(&sei)) {
        DWORD err = GetLastError();
        printf("Failed to execute program. Error code: %lu\n", err);
        return 1;
    }

    WaitForSingleObject(sei.hProcess, INFINITE);
    CloseHandle(sei.hProcess);

    return 0;
}