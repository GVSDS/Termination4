# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_FIO
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# To save lines of code, omit the complex text write stack,
# Wrap the open and os.open functions as File I/O and IFile I/O (FIO/IFIO).
# This is indeed much more convenient to a certain extent,
# And it also causes certain difficulties such as not being able to customize the writing process,
# Reading seek, etc., but the original open function is not particularly difficult to call,
# If you can't use FIO/IFIO, you can use the original open or os.open.


from .T_imports import *


class _FIO:
    def openw(self, file: str, write: str | bytes, mode: str | int = 1, encoding: str = "UTF-8"):
        flags: int = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        fd: int = os.open(file, flags)
        try:
            if mode == 1: write: str | bytes = write.encode(encoding)
            os.write(fd, write)
        finally:
            os.close(fd)
    def opena(self, file: str, write: str | bytes, mode: str | int = 1, encoding: str = "UTF-8"):
        flags: int = os.O_WRONLY | os.O_CREAT | os.O_APPEND
        fd: int = os.open(file, flags)
        try:
            if mode == 1:
                write: bytes = write.encode(encoding)
            os.write(fd, write)
        finally:
            os.close(fd)
    def openr(self, file: str, mode: int = 1, encoding: str = "UTF-8"):
        flags: int = os.O_RDONLY
        fd: int = os.open(file, flags)
        try:
            read: bytes | str = os.read(fd, os.path.getsize(file))
            if mode == 1:
                read: str | bytes = read.decode(encoding)
        finally:
            os.close(fd)
        return read
IFIO = _FIO()

class _FIO():
    def openw(self, file: str, write: str | bytes, mode: str | int = "1", encoding: str = "UTF-8") -> None:
        if mode == "1" or mode == 1:
            with open(file, "w", encoding = encoding) as f:
                f.write(write)
        elif mode == "2" or mode == 2:
            with open(file, "wb") as f:
                f.write(write)
    def opena(self, file: str, write: str, mode: str | int = "1" , encoding: str = "UTF-8") -> None:
        if mode == "1" or mode == 1:
            with open(file, "a", encoding = encoding) as f:
                f.write(write)
        elif mode == "2" or mode == 2:
            with open(file, "ab") as f:
                f.write(write)
    def openr(self, file: str, mode: str | int = "1", encoding: str = "UTF-8") -> str | bytes:
        if mode == "1" or mode == 1:
            with open(file, "r", encoding = encoding) as f:
                read = f.read()
        elif mode == "2" or mode == 2:
            with open(file, "rb") as f:
                read = f.read()
        return read
    def HideFile(self, path) -> None:
        ctypes.windll.kernel32.SetFileAttributesW(path, 0x02 | 0x04)
FIO = _FIO()
