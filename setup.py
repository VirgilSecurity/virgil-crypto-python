from virgil_crypto import __version__
from setuptools import setup, find_packages


setup(
    name="virgil-crypto",
    version=__version__,
    author="Virgil Security",
    url="https://virgilsecurity.com/",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: C++",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Security :: Cryptography",
    ],
    install_requires=["virgil-crypto-lib"],
    license="BSD",
    include_package_data=True,
    zip_safe=False,
    description="""
    Virgil Security provides a set of APIs for adding security to any application. In a few simple steps you can encrypt communication, securely store data, provide passwordless login, and ensure data integrity.
    Virgil Python Crypto Library is a high-level cryptographic library that allows you to perform all necessary operations for secure storing and transferring data and everything required to become HIPAA and GDPR compliant.
    """,
    long_description="""
    Virgil Security provides a set of APIs for adding security to any application. In a few simple steps you can encrypt communication, securely store data, provide passwordless login, and ensure data integrity.
    Virgil Python Crypto Library is a high-level cryptographic library that allows you to perform all necessary operations for secure storing and transferring data and everything required to become HIPAA and GDPR compliant.
    """,
    packages=find_packages(),
    package_data={"virgil_crypto": [
        "tests/*",
        "tests/data/*.json"
    ]}
)

