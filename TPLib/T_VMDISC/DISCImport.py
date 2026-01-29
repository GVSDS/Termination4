class importlib:
    class abc: from importlib.abc import Loader, MetaPathFinder
    class util: from importlib.util import spec_from_loader
from . import DISCAPI
import typing
import types
import json
import sys
import ast


class MemoryModuleLoader(importlib.abc.Loader):
    def __init__(self, module_name, module_code):
        self.module_name = module_name
        self.module_code = module_code
    def create_module(self, spec):
        return types.ModuleType(spec.name)
    def exec_module(self, module):
        exec(self.module_code, module.__dict__)
class MemoryModuleFinder(importlib.abc.MetaPathFinder):
    def __init__(self, ModulesDict: dict[str, str]):
        self.modules = ModulesDict
    def find_spec(self, fullname, path, target=None):
        return importlib.util.spec_from_loader(fullname,MemoryModuleLoader(fullname, self.modules[fullname]), origin = 'memory') if fullname in self.modules else None
def AddModule(ModulesDict: dict[str, str]):
    sys.meta_path.insert(0, MemoryModuleFinder(ModulesDict))

class DISCModule:
    def __init__(self, DISCPath: str, DISCPwd: str | None = None):
        self.Info_DISCNeeds: list[str] = ["disconfiguration.json"]
        self.Info_DISCModules: list[str] = ["Modules", "Functions", "Texture", "Sounds", "DataSets"]
        self.Info_DISConfigKeys: dict[str, typing.Any] = {"Name": [str, type(None)], "Version": [str, type(None)], "ICON": [str, type(None)], "EnabledModule": [list]}
        self.DISCPath: str = DISCPath
        self.DISCPwd: str | None = DISCPwd
        self._DISCHandle: DISCAPI.DISCFile | None = None
        self.Data_Modules: list = {}
        self.Data_Functions: list = {}
        self.Data_Textures: list = {}
        self.Data_Sounds: list = {}
        self.Data_DataSet: list = {}
        self.List_Modules: list = []
        self.List_Functions: list = []
        self.List_Textures: list = []
        self.List_Sounds: list = []
        self.List_DataSet: list = []
        if DISCAPI.is_DISCfile(self.DISCPath):
            self._DISCHandle: DISCAPI.DISCFile | None = DISCAPI.DISCFile(self.DISCPath)
            self.DISCFileList: list[str] = self._DISCHandle.namelist()
            self.DISCFileListLower: list[str] = [i.lower() for i in self.DISCFileList]
            for i in self.Info_DISCNeeds:
                if i.lower() not in self.DISCFileListLower:
                    self.close()
            self.__init_config__()
    def Is_Useful(self):
        return self._DISCHandle is not None
    def Is_InConfig(self, Key, Type):
        return Key in self.Config and (type(self.Config[Key]) in ([Type] if not isinstance(Type, list) else Type) if None not in ([Type] if not isinstance(Type, list) else Type) else (self.Config[Key] is None or type(self.Config[Key]) in [t for t in ([Type] if not isinstance(Type, list) else Type) if t is not None]))        
    def __init_config__(self):
        if not self.Is_Useful(): return False
        self.Config = self.GetFile("DISConfiguration.Json")
        try: self.Config = json.loads(self.Config)
        except: return self.close()
        for i in self.Info_DISConfigKeys:
            if not self.Is_InConfig(i, self.Info_DISConfigKeys[i]):
                return self.close()
        for i in self.Config["EnabledModule"]:
            if i not in self.Info_DISCModules or i.lower() + "/" not in self.DISCFileListLower:
                return self.close()
        for i in self.Config["EnabledModule"]:
            if i == "Modules": self.__init_modules__()
            if i == "Functions": self.__init_functions__()
            if i == "Textures": self.__init_texture_pack__()
            if i == "Sounds": self.__init_sound_pack__()
            if i == "DataSets": self.__init_dataset__()
    def __init_modules__(self):
        if self.Is_InConfig("Modules", list): self.List_Modules = [f"Modules/{i}" for i in self.Config["Modules"]]
        else: self.List_Modules = self.GetFileInZipDir("Modules")
        for i in self.List_Modules:
            try: self.Data_Modules[i] = AddModule({i.replace("Modules/", "").split(".")[0]: self.GetFile(i)})
            except: self.List_Modules.remove(i)
    def __init_functions__(self):
        if self.Is_InConfig("Functions", list): self.List_Functions = [f"Functions/{i}" for i in self.Config["Functions"]]
        else: self.List_Functions = self.GetFileInZipDir("Functions")
        for i in self.List_Functions:
            try: self.Data_Functions[i] = AddModule({i.replace("Functions/", "").split(".")[0]: self.GetFile(i)})
            except: self.List_Functions.remove(i)
    def __init_texture_pack__(self):
        pass
    def __init_sound_pack__(self):
        pass
    def __init_dataset__(self):
        pass
    def GetFile(self, Path):
        with self._DISCHandle.open(Path, "r", pwd = self.DISCPwd) as f: return f.read()
    def GetFileInZipDir(self, Path: str):
        return [name for name in self._DISCHandle.namelist() if name.startswith(Path.rstrip('/') + '/') and name != Path.rstrip('/') + '/']
    def close(self):
        self._DISCHandle.close()
        self._DISCHandle: DISCAPI.DISCFile | None = None
        return False

if __name__ == "__main__":
    print("Loading...")
    disc = DISCModule("./COREMOD.disc")
    print(disc.Is_Useful())
    print(disc.Data_Modules)
    import TestModule
    print(TestModule.a())
