from setuptools import setup
from setuptools.dist import Distribution


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    def has_ext_modules(self):
        return True

    def is_pure(self):
        return False

setup(
    name="virgil-crypto",
    version="2.0.4",
    author="Virgil Security",
    url="https://virgilsecurity.com/",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: C++",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Security :: Cryptography",
    ],
    license="BSD",
    packages=["virgil_crypto"],
    include_package_data=True,
    zip_safe=False,
    long_description="Virgil Crypto library wrapper",
    distclass=BinaryDistribution,
    ext_package='virgil_crypto',
    package_data={"virgil_crypto": ["_virgil_crypto_python.so", "virgil_crypto_python.py", "_virgil_crypto_python.pyd",
                  "tests/*"]}
)
