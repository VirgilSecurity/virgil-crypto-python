# Virgil Crypto Library Python

[![Travis (.com)](https://img.shields.io/travis/com/VirgilSecurity/virgil-crypto-python/master.svg)](https://travis-ci.com/VirgilSecurity/virgil-crypto-python) [![PyPI](https://img.shields.io/pypi/v/virgil-crypto.svg)](https://pypi.python.org/pypi/virgil-crypto) [![PyPI](https://img.shields.io/pypi/wheel/virgil-crypto.svg)](https://pypi.python.org/pypi/virgil-crypto) [![PyPI](https://img.shields.io/pypi/pyversions/virgil-crypto.svg)](https://pypi.python.org/pypi/virgil-crypto)

[Introduction](#introduction) | [Library purposes](#library-purposes) | [Installation](#installation) | [Usage examples](#usage-examples) | [Docs](#docs) | [License](#license) | [Contacts](#support)

## Introduction

Virgil Crypto Library Python is a stack of security libraries (ECIES with Crypto Agility wrapped in Virgil Cryptogram) and an open-source high-level [cryptographic library](https://github.com/VirgilSecurity/virgil-crypto) that allows you to perform all necessary operations for securely storing and transferring data in your digital solutions. Crypto Library is written in C++ and is suitable for mobile and server platforms.

## Library purposes
* Asymmetric Key Generation
* Encryption/Decryption of data and streams
* Generation/Verification of digital signatures
* Double Ratchet algorithm support
* **Post quantum algorithms support**: [Round5](https://round5.org/) (ecnryption) and [Falcon](https://falcon-sign.info/) (signature) 
* Crypto for using [Virgil Core SDK](https://github.com/VirgilSecurity/virgil-sdk-python)

## Installation

### Installing prerequisites

Install latest pip distribution: download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
and run it using the python interpreter.

### Installing from wheel binary packages

We provide binary packages for all the supported platforms.
Use pip to install the wheel binary packages:

```bash
pip install virgil-crypto
```

## Usage examples

### Generate a key pair

Generate a private key using the default algorithm (EC_X25519):

```python
from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()
key_pair = crypto.generate_key_pair()
```

### Generate and verify a signature

Generate signature and sign data with a private key:

```python
from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()
key_pair = crypto.generate_key_pair()
sender_private_key = key_pair.private_key

message_to_sign = "Hello, Bob!"
data_to_sign = message_to_sign.encode()

signature = crypto.generate_signature(data_to_sign, sender_private_key)
```

Verify a signature with a public key:

```python
from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()

verified = crypto.verify_signature(data_to_sign, signature, sender_public_key)
```

### Encrypt and decrypt data

Encrypt data with a public key:

```python
from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()

message_to_encrypt = "Hello, Bob!"
data_to_encrypt = message_to_encrypt.encode()

reciver_list = [reciver_public_key]
encrypted_data = crypto.encrypt(data_to_encrypt, *reciver_list)
```

Decrypt the encrypted data with a private key:

```python
from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()

decrypted_data = crypto.decrypt(encrypted_data, reciver_private_key)
decrypted_message = bytes(decrypted_data).decode()
```

### Import and export keys

Export keys:

```
crypto = VirgilCrypto()

# generate a Key Pair
key_pair = crypto.generate_keys()

# export a Private key
private_key_data = crypto.export_private_key(key_pair.private_key, "[YOUR_PASSWORD]")
base64.b64encode(private_key_data)

# export a Public key
public_key_data = crypto.export_public_key(key_pair.public_key, "[YOUR_PASSWORD]")
base64.b64encode(public_key_data)
```

Import keys:

```
crypto = VirgilCrypto()
private_key_str = "MIGhMF0GCSqGSIb3DQEFDTBQMC8GCSqGSIb3DQEFDDAiBBBtfBoM7VfmWPlvyHuGWvMSAgIZ6zAKBggqhkiG9w0CCjAdBglghkgBZQMEASoEECwaKJKWFNn3OMVoUXEcmqcEQMZ+WWkmPqzwzJXGFrgS/+bEbr2DvreVgEUiLKrggmXL9ZKugPKG0VhNY0omnCNXDzkXi5dCFp25RLqbbSYsCyw="
private_key_data = base64.b64decode(private_key_str)

# import a Private key
crypto.import_private_key(private_key_data, "[YOUR_PASSWORD]")

//-----------------------------------------------------

crypto = VirgilCrypto()
public_key_str = "MCowBQYDK2VwAyEA9IVUzsQENtRVzhzraTiEZZy7YLq5LDQOXGQG/q0t0kE="
public_key_data = base64.b64decode(public_key_str)

# import a Public key
crypto.import_public_key(public_key_data)
```

## Docs
- [API Reference](http://virgilsecurity.github.io/virgil-crypto-python/)
- [Crypto Core Library](https://github.com/VirgilSecurity/virgil-crypto)
- [Developer Documentation](https://developer.virgilsecurity.com/docs/)

## License
This library is released under the [3-clause BSD License](LICENSE).

## Support
Our developer support team is here to help you. Find out more information on our [Help Center](https://help.virgilsecurity.com/).

You can find us on [Twitter](https://twitter.com/VirgilSecurity) or send us email support@VirgilSecurity.com.

Also, get extra help from our support team on [Slack](https://virgilsecurity.com/join-community).
