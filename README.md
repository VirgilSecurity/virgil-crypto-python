# Virgil Security Python Crypto Library 

[![PyPI](https://img.shields.io/pypi/v/virgil-crypto.svg)](https://pypi.python.org/pypi/virgil-crypto) [![PyPI](https://img.shields.io/pypi/wheel/virgil-crypto.svg)](https://pypi.python.org/pypi/virgil-crypto) [![PyPI](https://img.shields.io/pypi/pyversions/virgil-crypto.svg)](https://pypi.python.org/pypi/virgil-crypto)

### [Introduction](#introduction) | [Library purposes](#library-purposes) | [Usage examples](#usage-examples) | [Installation](#installation) | [Docs](#docs) | [License](#license) | [Contacts](#support)

## Introduction
VirgilCrypto is a stack of security libraries (ECIES with Crypto Agility wrapped in Virgil Cryptogram) and an 
open-source high-level [cryptographic library](https://github.com/VirgilSecurity/virgil-crypto) that allows you to 
perform all necessary operations for securely storing and transferring data in your digital solutions. Crypto Library 
is written in C++ and is suitable for mobile and server platforms.

Virgil Security, Inc., guides software developers into the forthcoming security world in which everything will be 
encrypted (and passwords will be eliminated). In this world, the days of developers having to raise millions of 
dollars to build a secure chat, secure email, secure file-sharing, or a secure anything have come to an end. Now 
developers can instead focus on building features that give them a competitive market advantage while end-users can 
enjoy the privacy and security they increasingly demand.

## Library purposes
* Asymmetric Key Generation
* Encryption/Decryption of data
* Generation/Verification of digital signatures

## Usage examples

#### Generate a key pair

Generate a Private Key with the default algorithm (EC_X25519):

```python
from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()
key_pair = crypto.generate_keys()
```

#### Generate and verify a signature

Generate signature and sign data with a private key:

```python
from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()
key_pair = crypto.generate_keys()
sender_private_key = key_pair.private_key

message_to_sign = "Hello, Bob!"
data_to_sign = message_to_sign.encode()

signature = crypto.sign(data_to_sign, sender_private_key)
```

Verify a signature with a public key:

```python
from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()

verified = crypto.verify(data_to_sign, signature, sender_public_key)
```

#### Encrypt and decrypt data

Encrypt data with a Public Key:

```python
from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()

message_to_encrypt = "Hello, Bob!"
data_to_encrypt = message_to_encrypt.encode()

reciver_list = [reciver_public_key]
encrypted_data = crypto.encrypt(data_to_encrypt, *reciver_list)
```

Decrypt the encrypted data with a Private Key:

```python
from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()

decrypted_data = crypto.decrypt(encrypted_data, reciver_private_key)
decrypted_message = bytes(decrypted_data).decode()
```

Need more examples? Visit our [developer documentation](https://developer.virgilsecurity.com/docs/how-to#cryptography).

  
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

## Docs
- [API Reference](http://virgilsecurity.github.io/virgil-crypto-javascript/)
- [Crypto Core Library](https://github.com/VirgilSecurity/virgil-crypto)
- [More usage examples](https://developer.virgilsecurity.com/docs/how-to#cryptography)

## License
This library is released under the [3-clause BSD License](LICENSE).

## Support
Our developer support team is here to help you. Find out more information on our [Help Center](https://help.virgilsecurity.com/).

You can find us on [Twitter](https://twitter.com/VirgilSecurity) or send us email support@VirgilSecurity.com.

Also, get extra help from our support team on [Slack](https://virgilsecurity.slack.com/join/shared_invite/enQtMjg4MDE4ODM3ODA4LTc2OWQwOTQ3YjNhNTQ0ZjJiZDc2NjkzYjYxNTI0YzhmNTY2ZDliMGJjYWQ5YmZiOGU5ZWEzNmJiMWZhYWVmYTM).
