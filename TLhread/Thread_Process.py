# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLhread/Thread_Process
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Breakthrough: we used a dual-process and thread system,
# which means we can enjoy both the convenience of
# threads and the speed of processes at the same time.
# Praise our leader!


from TLib import *
from TLib.T_imports import *


class Process_Test(T_Process.Mp_TProcess):
    def Run(self):
        self.desc = "CMD: Test"
        self.logger.Info("Test Process")
        while True:
            self.logger.Info("Test Process")
            time.sleep(5)

class Process_ChildProcess(T_Process.Mp_TProcess):
    def Run(self, FilePath: str = None, SleepTime: float = 5, FilePath2: str = None):
        self.desc: str = FilePath
        Path: str = FilePath
        if not os.path.isfile(FilePath) and os.path.isfile(FilePath2):
            Path: str = FilePath2
        else: self.logger.Info(f"FilePath: {FilePath} Is Not Exist, FilePath2: {FilePath2} Is Not Exist Too.")
        self.Handle = T_Tools.ChildProcessManager()
        self.Handle.SetLogger(self.logger)
        if not self.Handle.StartChildProcess(Path):
            self.logger.Error(f"Start Child Process: {Path} Failed.")
            return
        while True:
            time.sleep(SleepTime)
            if not self.Handle.IsProcessAlive():
                break
        self.Handle.Close()
        return 0
