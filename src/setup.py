# Run as:
#    python setup.py build_ext --inplace

from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'decorateur',
  ext_modules = cythonize("decorateur.py"),
)
setup(
  name = 'poly',
  ext_modules = cythonize("poly.py"),
)
setup(
  name = 'galois',
  ext_modules = cythonize("galois.py"),
)
setup(
  name = 'matrice',
  ext_modules = cythonize("matrice.py"),
)
setup(
  name = 'goppa',
  ext_modules = cythonize("goppa.py"),
)
setup(
  name = 'clef',
  ext_modules = cythonize("clef.py"),
)