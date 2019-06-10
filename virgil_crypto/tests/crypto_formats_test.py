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
import unittest
from base64 import b64decode

from virgil_crypto import VirgilCrypto
from virgil_crypto.hashes import HashAlgorithm


class CryptoFormatsTest(unittest.TestCase):

    def test_signature_hash(self):
        data = bytearray("test".encode())
        crypto = VirgilCrypto()
        key_pair = crypto.generate_key_pair()
        signature = crypto.generate_signature(data, key_pair.private_key)

        self.assertEqual(
            signature[:17],
            bytearray(b64decode("MFEwDQYJYIZIAWUDBAIDBQA="))
        )

    def test_key_identifier_is_correct(self):
        crypto_1 = VirgilCrypto()
        key_pair_1 = crypto_1.generate_key_pair()

        self.assertEqual(key_pair_1.private_key.identifier, key_pair_1.public_key.identifier)
        self.assertEqual(
            crypto_1.compute_hash(crypto_1.export_public_key(key_pair_1.public_key), HashAlgorithm.SHA512)[:8],
            key_pair_1.private_key.identifier
        )

        crypto_2 = VirgilCrypto(use_sha256_fingerprints=True)
        key_pair_2 = crypto_2.generate_key_pair()

        self.assertEqual(
            crypto_2.compute_hash(crypto_1.export_public_key(key_pair_2.public_key), HashAlgorithm.SHA256),
            key_pair_2.private_key.identifier
        )

