from setuptools import setup, Extension

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
    ext_modules=[Extension('_virgil_crypto_python', [])],
    ext_package='virgil_crypto'
)
