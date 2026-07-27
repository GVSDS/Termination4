import sys
f=open(sys.argv[0], "rb")
s=f.read()
f.close()

print(s)

f=open("1.dmp", "wb")
f.write(s)
f.close()