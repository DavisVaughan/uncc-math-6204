# Convert to C and compile with:
# python setup.py build_ext --inplace
# Docs: http://cython.readthedocs.io/en/latest/src/reference/compilation.html

from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize("SOR2.pyx"),
    include_dirs=[numpy.get_include()]
)