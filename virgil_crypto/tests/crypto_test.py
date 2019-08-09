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
import hashlib
import io
import unittest
from base64 import b64decode

from virgil_crypto_lib.foundation._c_bridge import VirgilCryptoFoundationError

from virgil_crypto import VirgilCrypto
from virgil_crypto.errors import VirgilCryptoError
from virgil_crypto.hashes import HashAlgorithm
from virgil_crypto.keys import KeyPairType


class CryptoTest(unittest.TestCase):

    def _crypto(self):
        return VirgilCrypto()

    def test_strtobytes(self):
        self.assertEqual(self._crypto().strtobytes('test'), (116, 101, 115, 116))

    def __check_key_generation(self, key_pair_type):
        key_pair = self._crypto().generate_key_pair(key_pair_type)
        self.assertEqual(key_pair.private_key.identifier, key_pair.public_key.identifier)
        self.assertEqual(key_pair.private_key.key_type, key_pair_type)

    def __check_key_import(self, key_pair_type):
        key_pair = self._crypto().generate_key_pair(key_pair_type)
        self.assertEqual(key_pair.private_key.key_type, key_pair_type)

        data_1 = self._crypto().export_private_key(key_pair.private_key)
        imported_private_key = self._crypto().import_private_key(data_1).private_key
        self.assertEqual(key_pair.private_key, imported_private_key)
        data_2 = self._crypto().export_public_key(key_pair.public_key)
        imported_public_key = self._crypto().import_public_key(data_2)
        self.assertEqual(key_pair.public_key, imported_public_key)

    def __check_encryption(self, key_pair_type):
        key_pair_1 = self._crypto().generate_key_pair(key_pair_type)
        key_pair_2 = self._crypto().generate_key_pair(key_pair_type)
        self.assertEqual(key_pair_1.private_key.key_type, key_pair_type)
        self.assertEqual(key_pair_2.private_key.key_type, key_pair_type)

        data = bytearray("test data".encode())

        encrypted_data = self._crypto().encrypt(data, key_pair_1.public_key)
        decrypted_data = self._crypto().decrypt(encrypted_data, key_pair_1.private_key)

        self.assertEqual(data, decrypted_data)
        self.assertRaises(VirgilCryptoFoundationError, self._crypto().decrypt, encrypted_data, key_pair_2.private_key)

    def __check_signature(self, key_pair_type):
        key_pair_1 = self._crypto().generate_key_pair(key_pair_type)
        key_pair_2 = self._crypto().generate_key_pair(key_pair_type)
        self.assertEqual(key_pair_1.private_key.key_type, key_pair_type)
        self.assertEqual(key_pair_2.private_key.key_type, key_pair_type)

        data = bytearray("test data".encode())

        signature = self._crypto().generate_signature(data, key_pair_1.private_key)

        self.assertTrue(self._crypto().verify_signature(data, signature, key_pair_1.public_key))
        self.assertFalse(self._crypto().verify_signature(data, signature, key_pair_2.public_key))

    def __check_sign_then_encrypt(self, key_pair_type):
        key_pair_1 = self._crypto().generate_key_pair(key_pair_type)
        key_pair_2 = self._crypto().generate_key_pair(key_pair_type)
        key_pair_3 = self._crypto().generate_key_pair(key_pair_type)
        self.assertEqual(key_pair_1.private_key.key_type, key_pair_type)
        self.assertEqual(key_pair_2.private_key.key_type, key_pair_type)
        self.assertEqual(key_pair_3.private_key.key_type, key_pair_type)

        data = bytearray("test data".encode())

        encrypted = self._crypto().sign_and_encrypt(data, key_pair_1.private_key, key_pair_1.public_key, key_pair_2.public_key)
        decrypted = self._crypto().decrypt_and_verify(encrypted, key_pair_2.private_key, [key_pair_1.public_key, key_pair_2.public_key])

        self.assertEqual(data, decrypted)

        self.assertRaises(VirgilCryptoFoundationError, self._crypto().decrypt_and_verify, encrypted, key_pair_3.private_key, [key_pair_1.public_key, key_pair_2.public_key])
        self.assertRaises(VirgilCryptoError, self._crypto().decrypt_and_verify, encrypted, key_pair_2.private_key, key_pair_3.public_key)

    def __check_stream_sign(self, key_pair_type):
        key_pair_1 = self._crypto().generate_key_pair(key_pair_type)
        key_pair_2 = self._crypto().generate_key_pair(key_pair_type)
        self.assertEqual(key_pair_1.private_key.key_type, key_pair_type)
        self.assertEqual(key_pair_2.private_key.key_type, key_pair_type)

        input_stream = io.BytesIO(bytearray("test data".encode()))

        signature = self._crypto().generate_stream_signature(input_stream, key_pair_1.private_key)

        input_stream_1 = io.BytesIO(bytearray("test data".encode()))
        input_stream_2 = io.BytesIO(bytearray("test data".encode()))

        self.assertTrue(self._crypto().verify_stream_signature(input_stream_1, signature, key_pair_1.public_key))
        self.assertFalse(self._crypto().verify_stream_signature(input_stream_2, signature, key_pair_2.public_key))

    def __check_stream_encryption(self, key_pair_type):
        key_pair_1 = self._crypto().generate_key_pair(key_pair_type)
        key_pair_2 = self._crypto().generate_key_pair(key_pair_type)
        self.assertEqual(key_pair_1.private_key.key_type, key_pair_type)
        self.assertEqual(key_pair_2.private_key.key_type, key_pair_type)

        data = bytearray("test data".encode())

        encrypt_input_stream = io.BytesIO(data)
        encrypt_output_stream = io.BytesIO()
        self._crypto().encrypt_stream(
            encrypt_input_stream,
            encrypt_output_stream,
            key_pair_1.public_key
        )
        encrypt_stream_data = encrypt_output_stream.getvalue()

        decrypt_input_stream = io.BytesIO(encrypt_stream_data)
        decrypt_output_stream = io.BytesIO()
        self._crypto().decrypt_stream(
            decrypt_input_stream,
            decrypt_output_stream,
            key_pair_1.private_key
        )
        decrypt_stream_data = decrypt_output_stream.getvalue()
        self.assertEqual(
            data,
            decrypt_stream_data
        )

        decrypt_input_stream_2 = io.BytesIO(encrypt_stream_data)
        decrypt_output_stream_2 = io.BytesIO()
        self.assertRaises(
            VirgilCryptoFoundationError,
            self._crypto().decrypt_stream,
            decrypt_input_stream_2,
            decrypt_output_stream_2,
            key_pair_2.private_key
        )

    def __check_generate_key_using_seed(self, key_pair_type):
        crypto = VirgilCrypto()
        seed = crypto.generate_random_data(32)

        key_id = crypto.generate_key_pair(key_pair_type, seed=seed).private_key.identifier

        retries = 5
        while retries > 0:
            key_pair = crypto.generate_key_pair(key_pair_type, seed=seed)
            self.assertTrue(key_id, key_pair.private_key.identifier)
            self.assertTrue(key_pair.private_key.identifier, key_pair.public_key.identifier)
            self.assertEqual(key_pair.private_key.key_type, key_pair_type)
            retries -= 1

    def test_key_generation_all_key_types(self):
        for key_type in [KeyPairType.CURVE25519, KeyPairType.ED25519, KeyPairType.SECP256R1, KeyPairType.RSA_2048]:
            self.__check_key_generation(key_type)

    def test_key_import_all_key_types(self):
        for key_type in [KeyPairType.CURVE25519, KeyPairType.ED25519, KeyPairType.SECP256R1, KeyPairType.RSA_2048]:
            self.__check_key_import(key_type)

    def test_encrypt_some_data_all_key_types(self):
        for key_type in [KeyPairType.CURVE25519, KeyPairType.ED25519, KeyPairType.SECP256R1, KeyPairType.RSA_2048]:
            self.__check_encryption(key_type)

    def test_signature_some_data_all_key_types(self):
        for key_type in [
            KeyPairType.ED25519,
            KeyPairType.SECP256R1,
            KeyPairType.RSA_2048
        ]:
            self.__check_signature(key_type)

    def test_sign_then_encrypt_all_key_types(self):
        for key_type in [
            KeyPairType.ED25519,
            KeyPairType.SECP256R1,
            KeyPairType.RSA_2048
        ]:
            self.__check_sign_then_encrypt(key_type)

    def test_sign_stream_all_key_types(self):
        for key_type in [
            KeyPairType.ED25519,
            KeyPairType.SECP256R1,
            KeyPairType.RSA_2048
        ]:
            self.__check_stream_sign(key_type)

    def test_encrypt_stream_all_key_types(self):
        for key_type in [KeyPairType.CURVE25519, KeyPairType.ED25519, KeyPairType.SECP256R1, KeyPairType.RSA_2048]:
            self.__check_stream_encryption(key_type)

    def test_generate_key_using_seed_all_key_types(self):
        for key_type in [KeyPairType.CURVE25519, KeyPairType.ED25519, KeyPairType.SECP256R1, KeyPairType.RSA_2048]:
            self.__check_generate_key_using_seed(key_type)


    def test_import_private_key(self):
        key_pair = self._crypto().generate_key_pair()
        private_key_data = self._crypto().export_private_key(key_pair.private_key)
        imported_key_pair = self._crypto().import_private_key(private_key_data)
        self.assertEqual(
            key_pair.private_key.identifier,
            imported_key_pair.private_key.identifier,
        )

    def test_import_export_public_key(self):
        key_pair = self._crypto().generate_key_pair()
        exported_public_key = self._crypto().export_public_key(
            key_pair.public_key
        )
        imported_public_key = self._crypto().import_public_key(
            exported_public_key
        )
        self.assertEqual(
            key_pair.public_key.identifier,
            imported_public_key.identifier
        )

    def test_extract_public_key(self):
        key_pair = self._crypto().generate_key_pair()
        extracted_public_key = self._crypto().extract_public_key(
            key_pair.private_key,
        )
        self.assertEqual(
            key_pair.public_key.identifier,
            extracted_public_key.identifier
        )

    def test_encrypt_and_decrypt_values(self):
        data = [1, 2, 3]
        key_pair = self._crypto().generate_key_pair()
        encrypt_result = self._crypto().encrypt(
            data,
            key_pair.public_key
        )
        decrypt_result = self._crypto().decrypt(
            encrypt_result,
            key_pair.private_key
        )
        self.assertEqual(
            data,
            list(decrypt_result)
        )

    def test_encrypt_and_decrypt_stream(self):
        data = bytearray([2, 3, 4])
        key_pair_1 = self._crypto().generate_key_pair()
        key_pair_2 = self._crypto().generate_key_pair()

        encrypt_input_stream = io.BytesIO(data)
        encrypt_output_stream = io.BytesIO()
        self._crypto().encrypt_stream(
            encrypt_input_stream,
            encrypt_output_stream,
            key_pair_1.public_key
        )
        encrypt_stream_data = encrypt_output_stream.getvalue()

        decrypt_input_stream = io.BytesIO(encrypt_stream_data)
        decrypt_output_stream = io.BytesIO()
        self._crypto().decrypt_stream(
            decrypt_input_stream,
            decrypt_output_stream,
            key_pair_1.private_key
        )
        decrypt_stream_data = decrypt_output_stream.getvalue()
        self.assertEqual(
            data,
            decrypt_stream_data
        )

        decrypt_input_stream_2 = io.BytesIO(encrypt_stream_data)
        decrypt_output_stream_2 = io.BytesIO()
        self.assertRaises(
            VirgilCryptoFoundationError,
            self._crypto().decrypt_stream,
            decrypt_input_stream_2,
            decrypt_output_stream_2,
            key_pair_2.private_key
        )

    def test_sign_and_verify_values(self):
        data = [1, 2, 3]
        key_pair_1 = self._crypto().generate_key_pair()
        key_pair_2 = self._crypto().generate_key_pair()
        signature = self._crypto().generate_signature(
            data,
            key_pair_1.private_key
        )
        verified = self._crypto().verify_signature(
            data,
            signature,
            key_pair_1.public_key
        )
        not_verified = self._crypto().verify_signature(
            data,
            signature,
            key_pair_2.public_key
        )
        self.assertTrue(verified)
        self.assertFalse(not_verified)

    def test_sign_and_verify_values_sha265(self):
        data = [1, 2, 3]
        cr = self._crypto()
        cr.signature_hash_algorithm = HashAlgorithm.SHA256
        key_pair = cr.generate_key_pair()
        signature = cr.generate_signature(
            data,
            key_pair.private_key
        )
        verified = cr.verify_signature(
            data,
            signature,
            key_pair.public_key
        )
        self.assertTrue(verified)

    def test_sign_and_verify_stream(self):
        data = bytearray([1, 2, 3])
        key_pair = self._crypto().generate_key_pair()
        sign_input_stream = io.BytesIO(data)
        signature = self._crypto().generate_stream_signature(
            sign_input_stream,
            key_pair.private_key
        )
        verify_input_stream = io.BytesIO(data)
        verified = self._crypto().verify_stream_signature(
            verify_input_stream,
            signature,
            key_pair.public_key
        )
        self.assertTrue(verified)

    def test_sign_and_verify_stream_sha256(self):
        data = bytearray([1, 2, 3])
        cr = self._crypto()
        cr.signature_hash_algorithm = HashAlgorithm.SHA256
        key_pair = cr.generate_key_pair()
        sign_input_stream = io.BytesIO(data)
        signature = cr.generate_stream_signature(
            sign_input_stream,
            key_pair.private_key
        )
        verify_input_stream = io.BytesIO(data)
        verified = cr.verify_stream_signature(
            verify_input_stream,
            signature,
            key_pair.public_key
        )
        self.assertTrue(verified)

    def test_private_key_identifier_is_correct(self):
        # STC-33
        crypto_1 = VirgilCrypto()
        key_pair_1 = crypto_1.generate_key_pair()

        self.assertEqual(
            hashlib.sha512(bytearray(crypto_1.export_public_key(key_pair_1.public_key))).digest()[0:8],
            bytes(key_pair_1.private_key.identifier)
        )

        crypto_2 = VirgilCrypto()
        crypto_2.use_sha256_fingerprints = True
        key_pair_2 = crypto_2.generate_key_pair()

        self.assertEqual(
            hashlib.sha256(bytearray(crypto_2.export_public_key(key_pair_2.public_key))).digest(),
            bytearray(key_pair_2.private_key.identifier)
        )

    def test_public_key_identifier_is_correct(self):
        # STC-33
        crypto_1 = VirgilCrypto()
        key_pair_1 = crypto_1.generate_key_pair()
        public_key_1 = crypto_1.extract_public_key(key_pair_1.private_key)
        self.assertEqual(public_key_1.identifier, key_pair_1.public_key.identifier)
        self.assertEqual(crypto_1.export_public_key(public_key_1), crypto_1.export_public_key(key_pair_1.public_key))
        self.assertEqual(
            hashlib.sha512(bytearray(crypto_1.export_public_key(key_pair_1.public_key))).digest()[0:8],
            bytearray(key_pair_1.public_key.identifier)
        )

        crypto_2 = VirgilCrypto()
        crypto_2.use_sha256_fingerprints = True
        key_pair_2 = crypto_2.generate_key_pair()
        public_key_2 = crypto_2.extract_public_key(key_pair_2.private_key)
        self.assertEqual(public_key_2.identifier, key_pair_2.public_key.identifier)
        self.assertEqual(crypto_1.export_public_key(public_key_2), crypto_1.export_public_key(key_pair_2.public_key))
        self.assertEqual(
            hashlib.sha256(bytearray(crypto_1.export_public_key(key_pair_2.public_key))).digest(),
            bytearray(key_pair_2.public_key.identifier)
        )

    def test_signature_hash(self):
        # STC-30
        crypto = VirgilCrypto()
        key_pair = crypto.generate_key_pair()
        test_data = bytearray("test".encode())
        signature = crypto.generate_signature(test_data, key_pair.private_key)

        self.assertEqual(bytearray(signature[0:17]), b64decode("MFEwDQYJYIZIAWUDBAIDBQA="))

    def test_sign_then_encrypt(self):
        crypto = VirgilCrypto()
        key_pair_1 = crypto.generate_key_pair()
        key_pair_2 = crypto.generate_key_pair()
        key_pair_3 = crypto.generate_key_pair()
        data = [1, 2, 3]

        cipher_data = crypto.sign_and_encrypt(data, key_pair_1.private_key, key_pair_2.public_key)

        decrypted_data = crypto.decrypt_and_verify(cipher_data, key_pair_2.private_key, [key_pair_1.public_key, key_pair_2.public_key])

        self.assertEqual(data, list(decrypted_data))

        self.assertRaises(VirgilCryptoError, crypto.decrypt_and_verify, cipher_data, key_pair_2.private_key, key_pair_3.public_key)

    def test_generate_key_using_seed(self):
        crypto = VirgilCrypto()
        seed = crypto.generate_random_data(32)

        key_id = crypto.generate_key_pair(seed=seed).private_key.identifier

        retries = 5
        while retries > 0:
            key_pair = crypto.generate_key_pair(seed=seed)
            self.assertTrue(key_id, key_pair.private_key.identifier)
            self.assertTrue(key_pair.private_key.identifier, key_pair.public_key.identifier)
            retries -= 1
