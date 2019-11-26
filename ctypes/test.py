from ctypes import *
from time import time

so_path = "/Users/guolei08/work/CrossLanguage/ctypes/libadd.so"
#mylib = CDLL(so_path)
mylib = cdll.LoadLibrary(so_path)
#add = mylib.add

#print add(1,2)

# c ext
# from demo import add

# Cython
# from add_wrapper import add

# ctypes
# mylib = CDLL('/home/yanxurui/test/keepcoding/python/extension/ctypes/libadd.so')
# add = mylib.add
# add.argtypes = [c_int, c_int]

# python
def add(a,b):
    return a+b

s=time()
for i in range(10000000):
    r = add(i, i)
print(time()-s)
