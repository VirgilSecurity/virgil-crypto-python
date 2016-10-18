import os
import sys
import shutil
import subprocess
from distutils.command.build import build as _build
from distutils.command.build_ext import build_ext as _build_ext

from distutils import log
from setuptools import setup, find_packages, Extension

try:
    THIS_FILE = __file__
except NameError:
    THIS_FILE = sys.argv[0]
THIS_FILE = os.path.abspath(THIS_FILE)

if os.path.dirname(THIS_FILE):
    os.chdir(os.path.dirname(THIS_FILE))
SCRIPT_DIR = os.getcwd()

def run_process(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            log.info(output.strip())
    return process.poll()

class VirgilBuild(_build):
    def __init__(self, *args, **kwargs):
        _build.__init__(self, *args, **kwargs)

    def run(self):
        crypto_dir = os.path.join(SCRIPT_DIR, "src", "virgil-crypto")
        os.chdir(crypto_dir)
        build_prefix = os.path.join(SCRIPT_DIR, "_build")
        install_prefix = SCRIPT_DIR
        install_dir = "virgil_crypto"
        VirgilBuild.cleanup_dir(build_prefix)

        cmake_build_command = [
            "cmake",
            "-H.",
            "-B%s" % build_prefix,
            "-DCMAKE_INSTALL_PREFIX=%s" % install_prefix,
            "-DINSTALL_API_DIR_NAME=%s" % install_dir,
            "-DINSTALL_LIB_DIR_NAME=%s" % install_dir,
            "-DLANG=python"
        ]
        run_process(cmake_build_command)
        cmake_install_command = [
            "cmake",
            "--build",
            build_prefix,
            "--target",
            "install"
        ]
        run_process(cmake_install_command)
        os.chdir(SCRIPT_DIR)
        VirgilBuild.cleanup_dir(build_prefix)

    @staticmethod
    def cleanup_dir(path):
        shutil.rmtree(path, ignore_errors=True)

class VirgilBuildExt(_build_ext):
    def __init__(self, *args, **kwargs):
        _build_ext.__init__(self, *args, **kwargs)

    def run(self):
        pass

setup(
    name="virgil-crypto",
    version="1.0",
    packages=find_packages(),
    long_description="Virgil keys service SDK",
    cmdclass={
        'build': VirgilBuild,
        'build_ext': VirgilBuildExt,
    },
    ext_modules=[Extension('virgil_crypto_python', [])],
    ext_package='virgil.crypto'
)
