# Tsugi
# JSON TO PYTHON
# *.tdoc

import traceback
import threading
import msgpack
import json
import ast
import re


class EnvThread(threading.Thread):
    def __init__(self, name, env, target, args=(), kwargs=None, 
                 start_callback=None, end_callback=None):
        super().__init__(target=target, args=args, kwargs=kwargs or {})
        self.name = name
        self.env = env
        self.local = threading.local()
        self.start_callback = start_callback
        self.end_callback = end_callback
    def run(self):
        try:
            if self.start_callback:
                self.start_callback(self)
            for key, value in self.env.items():
                setattr(self.local, key, value)
            original_target = self._target
            def wrapped_target():
                globals().update(vars(self.local))
                return original_target(*self._args, **self._kwargs)
            wrapped_target()
        except Exception as e:
            print(f"Thread Error: {e} {self.name}")
            traceback.print_exc()
        if self.end_callback:
            self.end_callback(self)


def XOR_encrypt_decrypt(data, key):
    if isinstance(data, str):
        data = data.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
def JSON2TDOC(j, xor_key="TSUGI_XOR_KEY"):
    packed = msgpack.packb(j, use_bin_type=True)
    if xor_key is not None:
        packed = XOR_encrypt_decrypt(packed, xor_key)
    return packed
def TDOC2JSON(tdoc, xor_key="TSUGI_XOR_KEY"):
    if xor_key is not None:
        tdoc = XOR_encrypt_decrypt(tdoc, xor_key)
    return msgpack.unpackb(tdoc, raw=False)

def GetAllEnvOutput(env):
    pattern = re.compile(r'^output_\d+$')
    return [key for key in env.keys() if pattern.match(key)]

def WashBlocks(tdoc):
    func={}
    for i in tdoc:
        _=tdoc[i]
        func[i]={
            "ID": str(_["id"]),
            "Name": _["name"],
            "Data": _["data"],
            "Type": _["class"],
            "Inputs": _["inputs"],
            "Outputs": _["outputs"]
        }
    return func

class Tsugi:
    def __init__(self, func, debug: bool = False):
        self.func = func
        self.res: dict = {}
        self.debug: bool = debug
        # res -> {ID: {"output_1":XXX, "output_2":XXX}}
        self.thread: dict = {}
        self.LogicalNode = ["for", "while", "if"]
        self.MappingTable: dict = {
            "start": self.Handle_Start,
            "data": self.Handle_Data,
            "retype": self.Handle_Retype,
            "tryretype": self.Handle_Tryretype,
            "operation": self.Handle_Operation,
            "print": self.Handle_Print,
            "code": self.Handle_Code,
            "if": self.Handle_If,
            "input": self.Handle_Input,
            "and": self.Handle_and,
            "or": self.Handle_or,
            "not": self.Handle_not,
            "comparison": self.Handle_Comparison,
            "comparison_not": self.Handle_Comparison_Not,
            "lt": self.Handle_lt,
            "gt": self.Handle_gt,
            "com_lt": self.Handle_com_lt,
            "com_gt": self.Handle_com_gt,
            "left_shift": self.Handle_left_shift,
            "right_shift": self.Handle_right_shift,
        }
        self.dl("===== ===== Tsugi ===== =====")
    def dl(self, *log):
        if self.debug:
            print(*log)
    def run(self):
        for i in self.func:
            if not self.func[i]["Inputs"]:
                self.thread[i] = EnvThread(i, {}, self.MappingTable[self.func[i]["Type"]], args=((), self.func[i]), end_callback=self.EndCallBack)
                self.thread[i].run()
    def EndCallBack(self, thread: EnvThread):
        _env=vars(thread)
        _k = GetAllEnvOutput(_env)
        self.res[thread.name]={k: _env[k] for k in _k}
        for i in self.func:
            connection_stop=False
            if i in self.res: continue
            if i in self.thread: continue
            if not self.func[i]["Inputs"]: continue
            for _input in self.func[i]["Inputs"]:
                for connection in self.func[i]["Inputs"][_input]["connections"]:
                    if connection["node"] not in self.res:
                        connection_stop=True
                        break
            if connection_stop: continue
            # Prepare To Run
            _inputs={}
            connection_stop=False
            for _input in self.func[i]["Inputs"]:
                connections=self.func[i]["Inputs"][_input]["connections"]
                _i=[]
                for _ in connections:
                    if _["input"] not in self.res[_["node"]]:
                        self.dl("NOT IN", i, _["node"], _["input"])
                        connection_stop=True
                        continue
                    if self.func[_["node"]]["Type"] not in self.LogicalNode:
                        _i.append(self.res[_["node"]][_["input"]])
                _inputs[_input]=tuple(_i) if len(_i) > 1 else (_i[0] if _i else _i)
                if connection_stop: break
            if connection_stop: continue
            self.dl("RUN", i, _inputs, self.func[i])
            self.thread[i] = EnvThread(i, _inputs, self.MappingTable[self.func[i]["Type"]], args=(_inputs, self.func[i]), end_callback=self.EndCallBack)
            self.thread[i].run()
    def _ChangeType(self, _value, _type):
        _=None
        if _type == "str": _=str(_value)
        elif _type == "int": _=int(_value)
        elif _type == "float": _=float(_value)
        elif _type == "tuple": _=tuple(ast.literal_eval(_value))
        elif _type == "bool":
            _=bool(_value)
            if _value.lower() in ["0", "false"]: _=False
        elif _type == "bytes": _=bytes(_value)
        elif _type == "frozenset": _=frozenset(_value)
        elif _type == "list": _=list(ast.literal_eval(_value))
        elif _type == "dict": _=dict(ast.literal_eval(_value))
        elif _type == "set": _=set(ast.literal_eval(_value))
        elif _type == "NoneType": _=None
        elif _type == "complex": _=complex(_value)
        return _
    def SetOutput(self, thread: EnvThread, output: str, value):
        setattr(thread, output, value)
    def Handle_Start(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", "0")
    def Handle_Data(self, _input, func):
        _=self._ChangeType(func["Data"]["value"], func["Data"]["type"])
        self.SetOutput(self.thread[func["ID"]], "output_1", _)
    def Handle_Retype(self, _input, func):
        _=self._ChangeType(_input["input_1"], func["Data"]["type"])
        self.SetOutput(self.thread[func["ID"]], "output_1", _)
    def Handle_Tryretype(self, _input, func):
        try: self._ChangeType(_input["input_1"], func["Data"]["type"])
        except: self.SetOutput(self.thread[func["ID"]], "output_1", False)
        else: self.SetOutput(self.thread[func["ID"]], "output_1", True)
    def Handle_Operation(self, _input, func):
        self.dl("D", func["Data"]["operation"], _input)
        _=eval(func["Data"]["operation"], dict(_input))
        self.SetOutput(self.thread[func["ID"]], "output_1", _)
    def Handle_and(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", _input["input_1"] and _input["input_2"])
    def Handle_or(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", _input["input_1"] or _input["input_2"])
    def Handle_not(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", not _input["input_1"])
    def Handle_Comparison(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", _input["input_1"] == _input["input_2"])
    def Handle_Comparison_Not(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", _input["input_1"] != _input["input_2"])
    def Handle_Code(self, _input, func):
        self.dl("C", func["Data"]["code"], _input)
        def SetOutput(name, value):
            name=str(name)
            if not re.compile(r'^output_\d+$').match(name):
                name=f"output_{name}"
            self.SetOutput(self.thread[func["ID"]], name, value)
        if not _input: _input={}
        _env={**_input, "SetOutput": SetOutput, "Output": SetOutput, "output": SetOutput, "out": SetOutput}
        exec(func["Data"]["code"], _env)
    def Handle_Print(self, _input, func):
        print(" ".join([str(_input[v]) for v in _input]))
    def Handle_If(self, _input, func):
        if _input["input_1"]: self.SetOutput(self.thread[func["ID"]], "output_1", True)
        else: self.SetOutput(self.thread[func["ID"]], "output_2", True)
    def Handle_Input(self, _input, func):
        prompt=""
        if func["Data"]["prompt"]: prompt=func["Data"]["prompt"]
        if "input_1" in _input: prompt=_input["input_1"]
        self.SetOutput(self.thread[func["ID"]], "output_1", input(prompt))
    def Handle_lt(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", _input["input_1"] < _input["input_2"])
    def Handle_gt(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", _input["input_1"] > _input["input_2"])
    def Handle_com_lt(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", _input["input_1"] <= _input["input_2"])
    def Handle_com_gt(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", _input["input_1"] >= _input["input_2"])
    def Handle_left_shift(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", _input["input_1"] << _input["input_2"])
    def Handle_right_shift(self, _input, func):
        self.SetOutput(self.thread[func["ID"]], "output_1", _input["input_1"] >> _input["input_2"])
