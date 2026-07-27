# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_Version
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Automatically record and read the number of runs and modifications of this project,
# And use it as a minor version number.


from .T_imports import *


class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, option: str) -> str:
        return option
class IniConfigHandler:
    @staticmethod
    def ReadIniToDict(FilePath: str) -> typing.Dict[str, typing.Dict[str, str]]:
        if not os.path.exists(FilePath): raise FileNotFoundError(f"{FilePath} Not Found.")
        Config: CaseSensitiveConfigParser = CaseSensitiveConfigParser()
        LoadedFiles: typing.List[str] = Config.read(FilePath, encoding = "utf-8")
        if not LoadedFiles: raise ValueError(f"Failed to load file: {FilePath}")
        if not Config.sections(): raise ValueError("No valid sections found in the INI file.")
        return {section: dict(Config.items(section)) for section in Config.sections()}
    @staticmethod
    def WriteDictToIni(Data: typing.Dict[str, typing.Dict[str, typing.Any]], FilePath: str) -> None:
        if not os.path.exists(FilePath): raise FileNotFoundError(f"{FilePath} not found.")
        Config: CaseSensitiveConfigParser = CaseSensitiveConfigParser()
        for Section, Items in Data.items():
            Config.add_section(Section)
            for Key, Value in Items.items():
                Config.set(Section, Key, str(Value))
        with open(FilePath, 'w', encoding = "utf-8") as f:
            Config.write(f)

class Version:
    def __init__(self, master: 'Termination4.Termination', vfile: str):
        self.master: 'Termination4.Termination' = master
        self.vfile: str = vfile
        self._v: typing.Dict[str, typing.Dict[str, str]] = IniConfigHandler.ReadIniToDict(vfile)
        self.version: typing.Dict[str, typing.Dict[str, str]] = self._v
        if self.master.WorkMod == "py":
            self._v["Compilation"]["Runs"] = str(int(self._v["Compilation"]["Runs"])+1)
            IniConfigHandler.WriteDictToIni(self._v, vfile)