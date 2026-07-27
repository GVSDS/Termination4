import ctypes


_ = ctypes.CDLL(r".\.lib\libTemplateMatcher.dll", winmode=0)
print(dir(_))
print(_.CaptureScreenGray)