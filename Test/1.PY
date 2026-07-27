import win32process
import win32job
import win32api
import win32con
import subprocess
import win32event

import time

class ChildProcessManager:
    def __init__(self):
        self.HJob = None
        self.ProcessId = None
        self.ProcessHandle = None

    def StartChildProcess(self, exe_path):
        self._Cleanup()
        try:
            self.HJob = win32job.CreateJobObject(None, "")
            if not self.HJob: raise Exception("Failed To Create Job Object")
        except Exception as e:
            print(f"Failed To Create Job Object: {e}")
            self._Cleanup()
            return False

        try:
            info = win32job.QueryInformationJobObject(self.HJob, win32job.JobObjectExtendedLimitInformation)
            info['BasicLimitInformation']['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            win32job.SetInformationJobObject(self.HJob, win32job.JobObjectExtendedLimitInformation, info)
        except Exception as e:
            print(f"Failed To Set Job Object Information: {e}")
            self._Cleanup()
            return False

        startUpInfo = win32process.STARTUPINFO()
        try:
            hProcess, hThread, dwProcessId, dwThreadId = win32process.CreateProcess(
                None, exe_path, None, None, False,
                win32process.CREATE_NEW_PROCESS_GROUP | win32process.CREATE_SUSPENDED,
                None, None, startUpInfo
            )
            self.ProcessId = dwProcessId
            self.ProcessHandle = hProcess
            win32job.AssignProcessToJobObject(self.HJob, hProcess)
            win32process.ResumeThread(hThread)
            win32api.CloseHandle(hThread)
            print(f"Successfully Started Child Process, PID: {dwProcessId}")
            return True
        except Exception as e:
            print(f"Failed To Start Child Process: {e}")
            self._Cleanup()
            return False

    def IsProcessAlive(self):
        if not self.ProcessId or not self.ProcessHandle: return False
        try:
            result = win32event.WaitForSingleObject(self.ProcessHandle, 0)
            return result == win32con.WAIT_TIMEOUT
        except Exception as e:
            print(f"Failed To Check Process Status: {e}")
            return False
    def _Cleanup(self):
        if self.ProcessHandle:
            try: win32api.CloseHandle(self.ProcessHandle)
            except: pass
            self.ProcessHandle = None
        if self.HJob:
            try: win32api.CloseHandle(self.HJob)
            except: pass
            self.HJob = None
        self.ProcessId = None
    def Close(self):
        self._Cleanup()

if __name__ == "__main__":
    manager = ChildProcessManager()
    if manager.StartChildProcess("notepad.exe"):
        try:
            while True:
                status = "存活" if manager.IsProcessAlive() else "死亡"
                print(f"子进程状态: {status}，PID: {manager.ProcessId}")
                time.sleep(1)
        finally:
            manager.Close()
