from cx_Freeze import setup, Executable


setup( name="TestApp", version="4.1.0.114514", description="This is description", executables=[Executable("test.py")], )