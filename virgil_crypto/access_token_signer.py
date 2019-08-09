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
from virgil_crypto.keys import VirgilPrivateKey, VirgilPublicKey

from virgil_crypto import VirgilCrypto


class AccessTokenSigner(object):
    """Access Token cryptographic signature operations
    Class provides a cryptographic signature operations for Access Token.
    """

    def __init__(self, crypto=VirgilCrypto()):
        self.__algorithm = "VEDS512"
        self.__crypto = crypto

    def generate_token_signature(self, token, private_key):
        # type: (Union[bytes, bytearray], VirgilPrivateKey) -> bytearray
        """Generate signature for Access token

        Args:
            token: Access Token bytes.
            private_key: Signer Private Key.

        Returns:
            Signature bytes.

        Raises:
            ValueError: if token or private key missing or malformed
        """
        if not private_key:
            raise ValueError("Missing private key")

        if not token:
            raise ValueError("Missing token for sign")

        if not isinstance(private_key, VirgilPrivateKey):
            raise ValueError("private_key must be a VirgilPrivateKey type")

        return self.__crypto.generate_signature(token, private_key)

    def verify_token_signature(self, signature,  token, public_key):
        # type: (Union[bytes, bytearray], Union[bytes, bytearray], VirgilPublicKey) -> bool
        """Verify Access Token signature

        Args:
            signature: Token signature bytes
            token: Access Token
            public_key: Signer Public Key

        Returns:
            True if signature is valid, False otherwise.

        Raises:
            ValueError: if public key or token missed or malformed.
        """
        if not isinstance(public_key, VirgilPublicKey):
            raise ValueError("public_key must be a VirgilPublicKey type")

        if not token:
            raise ValueError("Missing token to verify")

        return self.__crypto.verify_signature(
            token, signature, public_key
        )

    @property
    def algorithm(self):
        """Get Algorithm"""
        return self.__algorithm

    @property
    def crypto(self):
        """Get Crypto"""
        return self.__crypto
