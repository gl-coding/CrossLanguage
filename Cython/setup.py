from distutils.core import setup, Extension
from Cython.Build import Cythonize

ext_modules=[
    Extension("add_wrapper",
              sources=["add_wrapper.pyx"],
              extra_objects=['libadd.a']
    )
]

setup(
  name = 'wrapper for libadd',
  ext_modules = Cythonize(ext_modules),
)
