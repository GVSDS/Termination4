import time
import os


a=time.time()
os.system(r"D:\mingw64\bin\clang test.c")
b=time.time()

print("0", b-a)

def cov(i):
    a=time.time()
    os.system(fr"D:\mingw64\bin\clang -mllvm -threads={i} test.c")
    print(i, time.time()-a)

for i in range(1, 16+1):
    cov(i)