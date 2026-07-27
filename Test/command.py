import subprocess


class Command:
    def __init__(self, cmd):
        self.cmd = cmd
        #startupinfo = None
        #if sys.platform.startswith('win'):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        creationflags = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
        #else:
        #    creationflags = 0
        self.result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=False,
            startupinfo=startupinfo,
            creationflags=creationflags
        )
        self.stdout = self.result.stdout
        self.stderr = self.result.stderr
        self.returncode = self.result.returncode
    def __str__(self):
        return self.stdout
    def count(self, substring):
        return self.stdout.count(substring) + self.stderr.count(substring)
    def ishad(self, items):
        if not isinstance(items, (list, tuple, set)): items = [items]
        return any(self.count(item) > 0 for item in items)
    def successtatus(self):
        return self.ishad(["success", "successfully", "成功"])

a=Command("net start 'TProcess'")
print(a.successtatus())

b=Command("net stop 'TProcess'")
print(b.successtatus())
