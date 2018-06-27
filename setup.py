import os
from setuptools import setup, find_packages
from setuptools.dist import Distribution

crypto_version = os.getenv("CRYPTO_VERSION").split(".")
crypto_version[0] = crypto_version[0].replace("2", "3")


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    def has_ext_modules(self):
        return True

    def is_pure(self):
        return False


setup(
    name="virgil-crypto",
    version=".".join(crypto_version),
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
        "Programming Language :: Python :: 3.6",
        "Topic :: Security :: Cryptography",
    ],
    license="BSD",
    include_package_data=True,
    zip_safe=False,
    long_description="""
    Virgil Security provides a set of APIs for adding security to any application. In a few simple steps you can encrypt communication, securely store data, provide passwordless login, and ensure data integrity.
    Virgil SDK allows developers to get up and running with Virgil API quickly and add full end-to-end (E2EE) security to their existing digital solutions to become HIPAA and GDPR compliant and more.(изменено)
    Virgil Python Crypto Library is a high-level cryptographic library that allows you to perform all necessary operations for secure storing and transferring data and everything required to become HIPAA and GDPR compliant.
    """,
    distclass=BinaryDistribution,
    packages=find_packages(),
    package_data={"virgil_crypto": [
        "_virgil_crypto_python.so",
        "virgil_crypto_python.py",
        "_virgil_crypto_python.pyd",
        "tests/*"
    ]}
)

