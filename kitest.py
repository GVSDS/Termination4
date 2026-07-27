import os


KIT = r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64"
KITUM = r"C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\um"
KITLIB = r"C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\um"
VC = r"D:\Microsoft Visual Studio\18\Insiders\VC\Tools\MSVC\14.50.35503\bin\Hostx64\x64"

os.system(f"\"{os.path.join(KIT, 'rc.exe')}\" /i \"{KITLIB}\" /fo .\\.tmp\\App.res .\\.tmp\\App.rc")
# os.system(f"\"{os.path.join(KIT, 'mt.exe')}\" -manifest .\\.tmp\\App.manifest -outputresource:Termination4.exe")
# os.system(f"\"{os.path.join(VC,  'link.exe')}\" /nologo /out:Termination4.exe Termination4.exe .\\.tmp\\App.res")

"""
rc.exe /fo .\.tmp\App.res .\.tmp\App.rc
mt.exe -manifest .\.tmp\App.manifest -outputresource:Termination4.exe
link.exe /nologo /out:Termination4.exe Termination4.exe .\.tmp\App.res


"""