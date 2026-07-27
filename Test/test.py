import code
import inspect
from pprint import pprint

class REBLConsole(code.InteractiveConsole):
    def __init__(self, locals=None):
        super().__init__(locals)
        self._breakpoints = set()
    
    def showsource(self, obj):
        """显示对象源代码"""
        try:
            lines, start = inspect.getsourcelines(obj)
            print(f"Source code of {obj.__name__}:")
            for i, line in enumerate(lines, start):
                print(f"{i:4d}: {line.rstrip()}")
        except (TypeError, OSError):
            print("No source code available")
    
    def inspect(self, obj):
        """检查对象详细信息"""
        print(f"Inspecting {type(obj).__name__}:")
        pprint(dir(obj))
        if callable(obj):
            print("\nSignature:")
            print(inspect.signature(obj))
    
    def add_breakpoint(self, line_no):
        """添加断点"""
        self._breakpoints.add(line_no)
        print(f"Breakpoint set at line {line_no}")
    
    def runcode(self, code_obj):
        """执行代码并处理断点"""
        try:
            exec(code_obj, self.locals)
        except SystemExit:
            raise
        except:
            self.showtraceback()

def start_rebl():
    """启动REBL环境"""
    print("Python REBL - Read Eval Break Loop")
    print("Type 'help' for available commands")
    
    console = REBLConsole(locals())
    
    while True:
        try:
            code_input = input("rebl> ")
            
            if code_input.strip() == "help":
                print("REBL commands:")
                print("  help - 显示帮助")
                print("  inspect(obj) - 检查对象")
                print("  source(obj) - 显示源代码")
                print("  break(line) - 设置断点")
                print("  exit - 退出REBL")
                continue
            elif code_input.strip() == "exit":
                break
            
            console.push(code_input)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
        except EOFError:
            break

if __name__ == "__main__":
    start_rebl()