import os
import sys
import shutil
import subprocess
from distutils.command.build import build as _build
from distutils.command.build_ext import build_ext as _build_ext

from distutils.spawn import spawn
from distutils import log
from setuptools import setup, Extension

try:
    THIS_FILE = __file__
except NameError:
    THIS_FILE = sys.argv[0]
THIS_FILE = os.path.abspath(THIS_FILE)

if os.path.dirname(THIS_FILE):
    os.chdir(os.path.dirname(THIS_FILE))
SCRIPT_DIR = os.getcwd()

setup(
    name="virgil-crypto",
    version="2.0.4",
    author="Virgil Security",
    url="https://virgilsecurity.com/",
    classifiers=[
        "Development Status :: 5 - Production",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: C++",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Security :: Cryptography",
    ],
    license="BSD",
    packages=["virgil_crypto"],
    include_package_data=True,
    zip_safe=False,
    long_description="Virgil Crypto library wrapper",
    ext_modules=[Extension('_virgil_crypto_python', [])],
    ext_package='virgil_crypto'
)
