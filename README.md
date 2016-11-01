# Virgil Crypto Library wrapper

## Installation

### Installing prerequisites

Install latest pip distribution: download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
and run it using the python interpreter.

### Installing from wheel binary packages

We provide binary packages for all supported platforms.
Use pip to install the wheel binary packages:

```sh
pip install -U virgil-crypto
```

### Building Virgil Crypto from source

If there is no binary package for your platform you can build Crypto
library from source.

#### Installing prerequisites

1. Install build dependencies.

   https://github.com/VirgilSecurity/virgil-crypto/#build-prerequisites

2. Install latest `wheel` distribution.

   ```sh
   pip install wheel
   ```

#### Building Virgil Crypto distribution

1. Download Virgil Crypto source distribution:

2. Extract source distribution:


   ```
   tar -xvzf virgil-crypto-2.0.0a.tar.gz

   ```

3. Switch to the distribution directory:


   ```
   cd virgil-crypto-2.0.0a

   ```

4. Build the wheel binary distribution:


   ```
   python setup.py bdist_wheel
   ```

5. Install the distribution with `pip`. The file name may vary depending
   on your platform so look into the dist directory for the correct name

   ```
   pip install dist/virgil_crypto-2.0.0a0-cp27-cp27mu-linux_x86_64.whl
   ```
