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

from virgil_crypto_lib.foundation import RecipientCipher, Aes256Gcm, CtrDrbg

from virgil_crypto import VirgilCrypto
from virgil_crypto.keys import KeyPairType


class VirgilCipherTest(unittest.TestCase):
    def test_encrypts_and_decrypts_data(self):
        raw_data = bytearray("test", "utf-8")

        rng = CtrDrbg()
        rng.setup_defaults()

        key_pair1 = VirgilCrypto().generate_key_pair(KeyPairType.ED25519)
        key_pair2 = VirgilCrypto().generate_key_pair(KeyPairType.ED25519)

        cipher = RecipientCipher()
        aes_gcm = Aes256Gcm()

        cipher.set_encryption_cipher(aes_gcm)
        cipher.set_random(rng)

        cipher.add_key_recipient(bytearray("1", "utf-8"), key_pair1.public_key.public_key)
        cipher.add_key_recipient(bytearray("2", "utf-8"), key_pair2.public_key.public_key)

        cipher.start_encryption()
        encrypted_data = cipher.pack_message_info()
        encrypted_data += cipher.process_encryption(raw_data)
        encrypted_data += cipher.finish_encryption()

        cipher.start_decryption_with_key(
            bytearray("1", "utf-8"),
            key_pair1.private_key.private_key,
            bytearray()
        )
        decrypted_data1 = bytearray()
        decrypted_data1 += cipher.process_decryption(encrypted_data)
        decrypted_data1 += cipher.finish_decryption()

        self.assertEqual(
            raw_data,
            bytearray(decrypted_data1)
        )

        cipher.start_decryption_with_key(
            bytearray("2", "utf-8"),
            key_pair2.private_key.private_key,
            bytearray()
        )
        decrypted_data2 = bytearray()
        decrypted_data2 += cipher.process_decryption(encrypted_data)
        decrypted_data2 += cipher.finish_decryption()

        self.assertEqual(
            raw_data,
            bytearray(decrypted_data2)
        )
