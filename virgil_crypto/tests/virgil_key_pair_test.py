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

from virgil_crypto.virgil_crypto_python import VirgilKeyPair


class VirgilKeyPairTest(unittest.TestCase):
    def test_generates_keys(self):
        key_pair = VirgilKeyPair.generate(VirgilKeyPair.Type_FAST_EC_ED25519)
        self.assertTrue(
            key_pair.publicKey()
        )
        self.assertTrue(
            key_pair.privateKey()
        )

    def test_converts_keys_to_der(self):
        key_pair = VirgilKeyPair.generate(VirgilKeyPair.Type_FAST_EC_ED25519)
        self.assertTrue(
            VirgilKeyPair.publicKeyToDER(key_pair.publicKey())
        )
        self.assertTrue(
            VirgilKeyPair.privateKeyToDER(key_pair.privateKey())
        )

    def test_encrypts_and_decrypts_private_key(self):
        password = bytearray("test", "utf-8")
        key_pair = VirgilKeyPair.generate(VirgilKeyPair.Type_FAST_EC_ED25519)
        encrypted_private_key = VirgilKeyPair.encryptPrivateKey(
            key_pair.privateKey(),
            password
        )
        decrypted_private_key = VirgilKeyPair.decryptPrivateKey(
            encrypted_private_key,
            password
        )
        self.assertEqual(
            key_pair.privateKey(),
            decrypted_private_key
        )

    def test_extracts_public_key(self):
        key_pair = VirgilKeyPair.generate(VirgilKeyPair.Type_FAST_EC_ED25519)
        extracted_public_key = VirgilKeyPair.extractPublicKey(
            key_pair.privateKey(),
            []
        )
        self.assertEqual(
            key_pair.publicKey(),
            extracted_public_key
        )
