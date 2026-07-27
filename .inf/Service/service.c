#include <windows.h>
#include <stdio.h>
#include <tchar.h>
#include <wtsapi32.h>
#include <userenv.h>
#include <tlhelp32.h>
#include <psapi.h>

#define SERVICE_NAME "TProcess"
#define SLEEP_TIME 5000

SERVICE_STATUS ServiceStatus;
SERVICE_STATUS_HANDLE hStatus;
TCHAR szPath[MAX_PATH];
HANDLE hProcess = NULL;

#pragma comment(lib, "wtsapi32.lib")
#pragma comment(lib, "userenv.lib")
#pragma comment(lib, "psapi.lib")
#pragma comment(lib, "advapi32.lib")

// 日志记录函数
/*
void LogEvent(LPCTSTR pszFormat, ...) {
    TCHAR szMsg[256];
    HANDLE hEventSource;
    LPTSTR lpszStrings[1];
    va_list pArg;

    va_start(pArg, pszFormat);
    _vstprintf_s(szMsg, 256, pszFormat, pArg);
    va_end(pArg);

    lpszStrings[0] = szMsg;

    hEventSource = RegisterEventSource(NULL, SERVICE_NAME);
    if (hEventSource != NULL) {
        ReportEvent(hEventSource, EVENTLOG_INFORMATION_TYPE, 0, 0, NULL, 1, 0, (LPCTSTR*)&lpszStrings[0], NULL);
        DeregisterEventSource(hEventSource);
    }
}
*/

// 获取当前登录用户的管理员令牌
HANDLE GetAdminToken() {
    PWTS_SESSION_INFO pSessionInfo = NULL;
    DWORD dwCount = 0;
    HANDLE hToken = NULL;
    HANDLE hPrimaryToken = NULL;
    HANDLE hUnfilteredToken = NULL;
    DWORD dwSize = 0;

    // 枚举会话
    if (!WTSEnumerateSessions(WTS_CURRENT_SERVER_HANDLE, 0, 1, &pSessionInfo, &dwCount)) {
        //LogEvent(_T("WTSEnumerateSessions failed: %d"), GetLastError());
        return NULL;
    }

    // 查找活动会话
    DWORD dwSessionId = 0;
    for (DWORD i = 0; i < dwCount; i++) {
        if (pSessionInfo[i].State == WTSActive) {
            dwSessionId = pSessionInfo[i].SessionId;
            break;
        }
    }
    WTSFreeMemory(pSessionInfo);

    if (dwSessionId == 0) {
        //LogEvent(_T("No active session found"));
        return NULL;
    }

    // 获取用户令牌
    if (!WTSQueryUserToken(dwSessionId, &hToken)) {
        //LogEvent(_T("WTSQueryUserToken failed: %d"), GetLastError());
        return NULL;
    }

    // 复制令牌
    if (!DuplicateTokenEx(hToken, TOKEN_ALL_ACCESS, NULL, SecurityIdentification, TokenPrimary, &hPrimaryToken)) {
        //LogEvent(_T("DuplicateTokenEx failed: %d"), GetLastError());
        CloseHandle(hToken);
        return NULL;
    }
    CloseHandle(hToken);

    // 获取不受限的管理员令牌
    if (!GetTokenInformation(hPrimaryToken, TokenLinkedToken, (LPVOID)&hUnfilteredToken, sizeof(HANDLE), &dwSize)) {
        // 如果UAC关闭，直接使用主令牌
        if (GetLastError() == ERROR_NO_SUCH_LOGON_SESSION) {
            //LogEvent(_T("UAC is disabled, using primary token"));
            return hPrimaryToken;
        }
        //LogEvent(_T("GetTokenInformation failed: %d"), GetLastError());
        CloseHandle(hPrimaryToken);
        return NULL;
    }

    CloseHandle(hPrimaryToken);
    return hUnfilteredToken;
}

// 以管理员权限启动进程
BOOL RunAsAdmin(LPCTSTR lpApplicationPath) {
    HANDLE hToken = GetAdminToken();
    if (hToken == NULL) {
        //LogEvent(_T("Failed to get admin token"));
        return FALSE;
    }

    LPVOID lpEnvironment = NULL;
    STARTUPINFO si = {0};
    PROCESS_INFORMATION pi = {0};
    BOOL bResult = FALSE;

    // 创建环境块
    if (!CreateEnvironmentBlock(&lpEnvironment, hToken, FALSE)) {
        //LogEvent(_T("CreateEnvironmentBlock failed: %d"), GetLastError());
        goto cleanup;
    }

    // 设置启动信息
    ZeroMemory(&si, sizeof(STARTUPINFO));
    si.cb = sizeof(STARTUPINFO);
    si.lpDesktop = _T("winsta0\\default");  // 允许UI交互
    si.wShowWindow = SW_SHOW;
    si.dwFlags = STARTF_USESHOWWINDOW;

    // 启动进程
    bResult = CreateProcessAsUser(
        hToken,
        NULL,
        (LPTSTR)lpApplicationPath,
        NULL,
        NULL,
        FALSE,
        CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP | NORMAL_PRIORITY_CLASS | CREATE_UNICODE_ENVIRONMENT, // CREATE_NEW_CONSOLE
        lpEnvironment,
        NULL,
        &si,
        &pi
    );

    if (!bResult) {
        //LogEvent(_T("CreateProcessAsUser failed: %d"), GetLastError());
    } else {
        CloseHandle(pi.hThread);
        // 不保存进程句柄，让进程独立运行
        CloseHandle(pi.hProcess);
        //LogEvent(_T("Started target program with admin rights: %s"), lpApplicationPath);
    }

cleanup:
    if (lpEnvironment) DestroyEnvironmentBlock(lpEnvironment);
    if (hToken) CloseHandle(hToken);
    return bResult;
}

// 检查指定路径的进程是否在运行
BOOL IsProcessRunning(LPCTSTR processPath) {
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        //LogEvent(_T("CreateToolhelp32Snapshot failed: %d"), GetLastError());
        return FALSE;
    }

    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32);

    if (!Process32First(hSnapshot, &pe32)) {
        //LogEvent(_T("Process32First failed: %d"), GetLastError());
        CloseHandle(hSnapshot);
        return FALSE;
    }

    BOOL bFound = FALSE;
    do {
        HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pe32.th32ProcessID);
        if (hProcess != NULL) {
            TCHAR szProcessPath[MAX_PATH] = {0};
            if (GetModuleFileNameEx(hProcess, NULL, szProcessPath, MAX_PATH)) {
                if (_tcsicmp(szProcessPath, processPath) == 0) {
                    bFound = TRUE;
                    CloseHandle(hProcess);
                    break;
                }
            }
            CloseHandle(hProcess);
        }
    } while (Process32Next(hSnapshot, &pe32));

    CloseHandle(hSnapshot);
    return bFound;
}

// 服务控制处理函数
void WINAPI ServiceCtrlHandler(DWORD dwControl) {
    switch (dwControl) {
        case SERVICE_CONTROL_STOP:
        case SERVICE_CONTROL_SHUTDOWN:
            ServiceStatus.dwWin32ExitCode = 0;
            ServiceStatus.dwCurrentState = SERVICE_STOPPED;
            ServiceStatus.dwCheckPoint = 0;
            ServiceStatus.dwWaitHint = 0;
            
            // 不终止已启动的进程
            //LogEvent(_T("Service stopped, leaving target process running"));
            break;
        default:
            break;
    }
    
    SetServiceStatus(hStatus, &ServiceStatus);
}

// 服务主函数
void WINAPI ServiceMain(DWORD argc, LPTSTR *argv) {
    // 注册服务控制处理函数
    hStatus = RegisterServiceCtrlHandler(SERVICE_NAME, ServiceCtrlHandler);
    if (hStatus == 0) {
        //LogEvent(_T("RegisterServiceCtrlHandler failed: %d"), GetLastError());
        return;
    }

    // 初始化服务状态
    ServiceStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS;
    ServiceStatus.dwCurrentState = SERVICE_START_PENDING;
    ServiceStatus.dwControlsAccepted = SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_SHUTDOWN;
    ServiceStatus.dwWin32ExitCode = 0;
    ServiceStatus.dwServiceSpecificExitCode = 0;
    ServiceStatus.dwCheckPoint = 0;
    ServiceStatus.dwWaitHint = 0;
    SetServiceStatus(hStatus, &ServiceStatus);

    //LogEvent(_T("Service starting"));

    // 更新服务状态为运行中
    ServiceStatus.dwCurrentState = SERVICE_RUNNING;
    ServiceStatus.dwCheckPoint = 0;
    ServiceStatus.dwWaitHint = 0;
    SetServiceStatus(hStatus, &ServiceStatus);

    // 主服务循环
    while (ServiceStatus.dwCurrentState == SERVICE_RUNNING) {
        if (!IsProcessRunning(szPath)) {
            if (!RunAsAdmin(szPath)) {
                //LogEvent(_T("Failed to start target program: %d"), GetLastError());
            }
        }
        Sleep(SLEEP_TIME);
    }
}

// 安装服务
BOOL InstallService(LPCTSTR path) {
    SC_HANDLE schSCManager = NULL;
    SC_HANDLE schService = NULL;
    TCHAR szFilePath[MAX_PATH];
    BOOL bSuccess = FALSE;
    
    // 获取当前可执行文件路径
    if (GetModuleFileName(NULL, szFilePath, MAX_PATH) == 0) {
        _tprintf(_T("GetModuleFileName failed: %d\n"), GetLastError());
        goto cleanup;
    }
    
    // 打开服务控制管理器
    schSCManager = OpenSCManager(NULL, NULL, SC_MANAGER_ALL_ACCESS);
    if (schSCManager == NULL) {
        _tprintf(_T("OpenSCManager failed: %d\n"), GetLastError());
        goto cleanup;
    }
    
    // 创建服务
    TCHAR szCommand[MAX_PATH + 50];
    _stprintf_s(szCommand, MAX_PATH + 50, _T("\"%s\" /start \"%s\""), szFilePath, path);
    
    schService = CreateService(
        schSCManager,              // SCM数据库
        SERVICE_NAME,              // 服务名
        SERVICE_NAME,              // 显示名
        SERVICE_ALL_ACCESS,        // 访问权限 SERVICE_ALL_ACCESS
        SERVICE_WIN32_OWN_PROCESS, // 服务类型
        SERVICE_AUTO_START,        // 启动类型
        SERVICE_ERROR_NORMAL,      // 错误控制类型
        szCommand,                 // 服务二进制文件路径
        NULL,                      // 不依赖其他服务
        NULL,                      // 不使用标签
        NULL,                      // 不使用密码
        NULL,                      // 本地系统账户
        NULL                       // 无密码
    );
    
    if (schService == NULL) {
        _tprintf(_T("CreateService failed: %d\n"), GetLastError());
        goto cleanup;
    }
    
    // 设置服务描述
    SERVICE_DESCRIPTION sd;
    sd.lpDescription = _T("Maintain the normal operation of some services in Windows");
    ChangeServiceConfig2(schService, SERVICE_CONFIG_DESCRIPTION, &sd);
    
    _tprintf(_T("Service installed successfully\n"));
    bSuccess = TRUE;
    
cleanup:
    if (schService != NULL) CloseServiceHandle(schService);
    if (schSCManager != NULL) CloseServiceHandle(schSCManager);
    return bSuccess;
}

// 卸载服务
BOOL UninstallService() {
    SC_HANDLE schSCManager = NULL;
    SC_HANDLE schService = NULL;
    BOOL bSuccess = FALSE;
    
    // 打开服务控制管理器
    schSCManager = OpenSCManager(NULL, NULL, SC_MANAGER_ALL_ACCESS);
    if (schSCManager == NULL) {
        _tprintf(_T("OpenSCManager failed: %d\n"), GetLastError());
        goto cleanup;
    }
    
    // 打开服务
    schService = OpenService(schSCManager, SERVICE_NAME, DELETE);
    if (schService == NULL) {
        _tprintf(_T("OpenService failed: %d\n"), GetLastError());
        goto cleanup;
    }
    
    // 删除服务
    if (!DeleteService(schService)) {
        _tprintf(_T("DeleteService failed: %d\n"), GetLastError());
        goto cleanup;
    }
    
    _tprintf(_T("Service uninstalled successfully\n"));
    bSuccess = TRUE;
    
cleanup:
    if (schService != NULL) CloseServiceHandle(schService);
    if (schSCManager != NULL) CloseServiceHandle(schSCManager);
    return bSuccess;
}

// 主函数
int _tmain(int argc, TCHAR *argv[]) {
    if (argc > 1) {
        if (_tcsicmp(argv[1], _T("/install")) == 0 && argc > 2) {
            if (!InstallService(argv[2])) {
                return 1;
            }
        } else if (_tcsicmp(argv[1], _T("/uninstall")) == 0) {
            if (!UninstallService()) {
                return 1;
            }
        } else if (_tcsicmp(argv[1], _T("/start")) == 0 && argc > 2) {
            _tcscpy_s(szPath, MAX_PATH, argv[2]);
            
            SERVICE_TABLE_ENTRY ServiceTable[] = {
                { (LPTSTR)SERVICE_NAME, (LPSERVICE_MAIN_FUNCTION)ServiceMain },
                { NULL, NULL }
            };
            
            if (!StartServiceCtrlDispatcher(ServiceTable)) {
                //LogEvent(_T("StartServiceCtrlDispatcher failed: %d"), GetLastError());
                return 1;
            }
        } else {
            _tprintf(_T("Usage:\n"));
            _tprintf(_T("  %s /install \"path\" - Install service to launch \"path\" with admin rights\n"), argv[0]);
            _tprintf(_T("  %s /uninstall - Uninstall service\n"), argv[0]);
            _tprintf(_T("  %s /start \"path\" - Start service (internal use)\n"), argv[0]);
            return 1;
        }
    } else {
        _tprintf(_T("Usage:\n"));
        _tprintf(_T("  %s /install \"path\" - Install service to launch \"path\" with admin rights\n"), argv[0]);
        _tprintf(_T("  %s /uninstall - Uninstall service\n"), argv[0]);
        _tprintf(_T("  %s /start \"path\" - Start service (internal use)\n"), argv[0]);
        return 1;
    }
    
    return 0;
}