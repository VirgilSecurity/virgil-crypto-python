# Copyright (C) 2016-2018 Virgil Security Inc.
#
# Lead Maintainer: Virgil Security Inc. <support@virgilsecurity.com>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     (1) Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#     (2) Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
#     (3) Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ''AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from virgil_crypto.hashes import HashAlgorithm

from virgil_crypto import VirgilCrypto
from virgil_crypto.keys import PrivateKey, PublicKey


class CardCrypto(object):
    """Cards cryptographic operations.
    Class provides a cryptographic operations for Cards.
    """

    def __init__(self, crypto=VirgilCrypto()):
        self.__crypto = crypto

    def generate_signature(self, data, private_key):
        # type: (Union[bytes, bytearray], PrivateKey) -> bytearray
        """Signs the specified data using Private key.
        Args:
            data: raw data bytes for signing.
            private_key: private key for signing.
        Returns:
            Signature bytes.
        """
        if not private_key:
            raise ValueError("Missing private key")

        if not isinstance(private_key, PrivateKey):
            raise ValueError("private_key must be a VirgilPrivateKey type")

        return self.__crypto.sign(data, private_key)

    def verify_signature(self, signature, data, public_key):
        # type: (Union[bytes, bytearray], Union[bytes, bytearray], PublicKey) -> bool
        """Verifies the specified signature using original data and signer's public key.
        Args:
            data: original data bytes for verification.
            signature: signature bytes for verification.
            public_key: signer public key for verification.
        Returns:
            True if signature is valid, False otherwise.
        """
        if not isinstance(public_key, PublicKey):
            raise ValueError("public_key must be a VirgilPublicKey type")

        return self.__crypto.verify(
            data, signature, public_key
        )

    def export_public_key(self, public_key):
        # type: (PublicKey) -> bytearray
        """Exports the Public key into material representation.
        Args:
            public_key: public key for export.
        Returns:
            Key material representation bytes.
        """
        if not public_key:
            raise ValueError("Missing public key")
        return self.__crypto.export_public_key(public_key)

    def import_public_key(self, data):
        # type: (Union[bytes, bytearray]) -> PublicKey
        """Imports the Public key from material representation.
        Args:
            data: key material representation bytes.
        Returns:
            Imported public key.
        """
        return self.__crypto.import_public_key(data)

    def generate_sha512(self, data):
        # type: (Union[bytes, bytearray]) -> bytearray
        """Computes the sha512 hash of specified data.
        Args:
            data: data bytes for fingerprint calculation.
        Returns:
            Hash bytes.
        """
        return self.__crypto.compute_hash(data, HashAlgorithm.SHA512)

    @property
    def crypto(self):
        """
        Gets Virgil Crypto.
        Returns:
             Card Crypto
        """
        return self.__crypto
