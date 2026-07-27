# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_std
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# Export sys.stdout to the log system or socket system.


from .T_imports import *


class StdoutRevertedWriter:
    def __init__(self) -> None:
        self.Show: bool | None = None
        self.logger: None = None
        self.__pid__: int = os.getpid()
    def SetConfig(self, Show: bool | None = None, logger: None = None) -> None:
        if Show: self.Show: bool | None = Show
        if logger: self.logger: None = logger
    def write(self, s: str) -> None:
        # self.logger.emit("T4Message", TWNT.GodKeys.encrypt({"PCMachineGUID": self.PCMachineGUID, "Message": s if s.replace("\n", "").replace("\t", "").replace(" ", "") in ('^', '') else f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] [{self.__pid__}] {s}"}), namespace="/Termination4SocketIOSpace")
        output: str = "" if s.replace("\n", "").replace("\t", "").replace(" ", "") in ('^', '') else s
        if not output.replace("\n", "").replace("\t", "").replace(" ", ""): return
        if self.logger: self.logger.Info(output)
        else: 
            if self.Show: print(output)
    def flush(self) -> None:
        pass

class ErrorToJsonError(Exception):
    def __init__(self, Message: str, OriginalException: typing.Optional[Exception] = None) -> None:
        super().__init__(Message)
        self.OriginalException: typing.Optional[Exception] = OriginalException
@dataclasses.dataclass
class TracebackFrame:
    FilePath: str
    LineNumber: int
    FunctionName: str
    CodeLine: typing.Optional[str]
    BytecodeInfo: typing.Optional[str]
@dataclasses.dataclass
class ErrorDetails:
    ErrorType: str
    ErrorMessage: str
    TracebackFrames: typing.List[TracebackFrame]
    IsConversionError: bool = False
    ConversionErrorMessage: typing.Optional[str] = None
class ErrorJsonConverter:
    @staticmethod
    def GetBytecodeInfo(Frame: typing.Callable) -> typing.Optional[str]:
        try:
            code_obj: types.CodeType = Frame.f_code
            info = {
                "CoName": code_obj.co_name,
                "CoArgcount": code_obj.co_argcount,
                "CoLenCode": len(code_obj.co_code),
                "CoCode30": code_obj.co_code.hex()
            }
            return info
        except Exception as e:
            return f"Failed To Get The Bytecode: {str(e)}"
    @staticmethod
    def GetCodeLineFromFrame(Frame: typing.Callable) -> typing.Optional[str]:
        try:
            Lines: typing.List[str]
            Lineno: int
            Lines, Lineno = inspect.getsourcelines(Frame)
            RelLineno: int
            RelLineno = Frame.f_lineno - Lineno
            if 0 <= RelLineno < len(Lines): return Lines[RelLineno].strip()
            return "Unable To Get The Source Code Line"
        except (IOError, OSError, TypeError, Exception) as e: return f"Failed To Get A Line Of Code: {str(e)}"
    @classmethod
    def GetErrorDetails(cls, exc: Exception) -> ErrorDetails:
        try:
            ErrorType = exc.__class__.__name__
            ErrorMessage = str(exc)
            TracebackFrames = []
            tb = exc.__traceback__
            while tb:
                frame = tb.tb_frame
                traceback_frame = TracebackFrame(
                    FilePath = frame.f_code.co_filename,
                    LineNumber = tb.tb_lineno,
                    FunctionName = frame.f_code.co_name,
                    CodeLine = cls.GetCodeLineFromFrame(frame),
                    BytecodeInfo = cls.GetBytecodeInfo(frame)
                )
                TracebackFrames.append(traceback_frame)
                tb = tb.tb_next
            return ErrorDetails(
                ErrorType = ErrorType,
                ErrorMessage = ErrorMessage,
                TracebackFrames = TracebackFrames
            )
        except Exception as e:
            return ErrorDetails(
                ErrorType = "ErrorProcessingFailure",
                ErrorMessage = "Unable To Handle The Original Error Message",
                TracebackFrames = [],
                IsConversionError = True,
                ConversionErrorMessage = str(e)
            )
    @classmethod
    def ConvertToJson(cls, exc: Exception) -> str:
        try: return dataclasses.asdict(cls.GetErrorDetails(exc))
        except Exception as e: raise ErrorToJsonError(message="Failed To Convert The Error To JSON", original_exception=e) from e
class FormatErrorJSON:
    def __init__(self, j: dict, b: str = None) -> None:
        self.j: dict = j
        self.b: str = b
    def __str__(self) -> str:
        if type(self.j) == ErrorToJsonError: return "Error To JSON Format Self Error Traceback:\n" + traceback.format_exc()
        return f"""Termination Traceback (Most Recent Call Last):
{"\n".join([f"\tFile \"{i["FilePath"]}\", Line {i["LineNumber"]}, In {i["FunctionName"]}:\n\t\t{i["CodeLine"]}" for i in self.j["TracebackFrames"]])}
{self.b + "\n" if self.b else ""}{self.j["ErrorType"]}: {self.j["ErrorMessage"]}"""
def ErrorFormat(e: Exception, b: str = None) -> FormatErrorJSON:
    return FormatErrorJSON(ErrorJsonConverter.ConvertToJson(e), b)
