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

from virgil_crypto import crypto, VirgilKeyPair
from virgil_crypto import VirgilCrypto
from virgil_crypto.hashes import HashAlgorithm


class CryptoTest(unittest.TestCase):
    def _crypto(self):
        return VirgilCrypto()

    def test_strtobytes(self):
        self.assertEqual(self._crypto().strtobytes('test'), (116, 101, 115, 116))

    def test_import_private_key(self):
        key_pair = self._crypto().generate_keys()
        private_key_data = key_pair.private_key.raw_key
        self.assertEqual(
            self._crypto().import_private_key(private_key_data),
            key_pair.private_key
        )

    def test_import_public_key(self):
        key_pair = self._crypto().generate_keys()
        public_key_data = key_pair.public_key.raw_key
        self.assertEqual(
            self._crypto().import_public_key(public_key_data),
            key_pair.public_key
        )

    def test_export_and_import_private_key_with_password(self):
        password = '123456'
        key_pair = self._crypto().generate_keys()
        exported_private_key = self._crypto().export_private_key(
            key_pair.private_key,
            password
        )
        self.assertNotEqual(
            exported_private_key,
            key_pair.private_key.raw_key
        )
        imported_private_key = self._crypto().import_private_key(
            exported_private_key,
            password
        )
        self.assertEqual(
            imported_private_key,
            key_pair.private_key
        )

    def test_export_public_key(self):
        key_pair = self._crypto().generate_keys()
        exported_public_key = self._crypto().export_public_key(
            key_pair.public_key
        )
        self.assertEqual(
            exported_public_key,
            key_pair.public_key.raw_key
        )

    def test_extract_public_key(self):
        key_pair = self._crypto().generate_keys()
        extracted_public_key = self._crypto().extract_public_key(
            key_pair.private_key,
        )
        self.assertEqual(
            extracted_public_key,
            key_pair.public_key
        )

    def test_encrypt_and_decrypt_values(self):
        data = [1, 2, 3]
        key_pair = self._crypto().generate_keys()
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
        data = bytearray([1, 2, 3])
        key_pair = self._crypto().generate_keys()
        encrypt_input_stream = io.BytesIO(data)
        encrypt_output_stream = io.BytesIO()
        self._crypto().encrypt_stream(
            encrypt_input_stream,
            encrypt_output_stream,
            key_pair.public_key
        )
        encrypt_stream_result = encrypt_output_stream.getvalue()
        decrypt_input_stream = io.BytesIO(encrypt_stream_result)
        decrypt_output_stream = io.BytesIO()
        self._crypto().decrypt_stream(
            decrypt_input_stream,
            decrypt_output_stream,
            key_pair.private_key
        )
        decrypt_stream_result = decrypt_output_stream.getvalue()
        self.assertEqual(
            data,
            decrypt_stream_result
        )

    def test_sign_and_verify_values(self):
        data = [1, 2, 3]
        key_pair = self._crypto().generate_keys()
        signature = self._crypto().sign(
            data,
            key_pair.private_key
        )
        verified = self._crypto().verify(
            data,
            signature,
            key_pair.public_key
        )
        self.assertTrue(verified)

    def test_sign_and_verify_values_sha265(self):
        data = [1, 2, 3]
        cr = self._crypto()
        cr.signature_hash_algorithm = HashAlgorithm.SHA256
        key_pair = cr.generate_keys()
        signature = cr.sign(
            data,
            key_pair.private_key
        )
        verified = cr.verify(
            data,
            signature,
            key_pair.public_key
        )
        self.assertTrue(verified)

    def test_sign_and_verify_stream(self):
        data = bytearray([1, 2, 3])
        key_pair = self._crypto().generate_keys()
        sign_input_stream = io.BytesIO(data)
        signature = self._crypto().sign_stream(
            sign_input_stream,
            key_pair.private_key
        )
        verify_input_stream = io.BytesIO(data)
        verified = self._crypto().verify_stream(
            verify_input_stream,
            signature,
            key_pair.public_key
        )
        self.assertTrue(verified)

    def test_sign_and_verify_stream_sha256(self):
        data = bytearray([1, 2, 3])
        cr = self._crypto()
        cr.signature_hash_algorithm = HashAlgorithm.SHA256
        key_pair = cr.generate_keys()
        sign_input_stream = io.BytesIO(data)
        signature = cr.sign_stream(
            sign_input_stream,
            key_pair.private_key
        )
        verify_input_stream = io.BytesIO(data)
        verified = cr.verify_stream(
            verify_input_stream,
            signature,
            key_pair.public_key
        )
        self.assertTrue(verified)

    def test_calculate_fingerprint(self):
        data = bytearray([1, 2, 3])
        fingerprint = self._crypto().calculate_fingerprint(data)
        self.assertTrue(fingerprint.value)
        self.assertIsInstance(fingerprint, crypto.Fingerprint)

    def test_private_key_identifier_is_correct(self):
        # STC-33
        crypto_1 = VirgilCrypto()
        key_pair_1 = crypto_1.generate_keys()

        self.assertEqual(
            hashlib.sha512(bytearray(crypto_1.export_public_key(key_pair_1.public_key))).digest()[0:8],
            bytearray(key_pair_1.private_key.identifier)
        )

        crypto_2 = VirgilCrypto()
        crypto_2.use_sha256_fingerprints = True
        key_pair_2 = crypto_2.generate_keys()

        self.assertEqual(
            hashlib.sha256(bytearray(crypto_2.export_public_key(key_pair_2.public_key))).digest(),
            bytearray(key_pair_2.private_key.identifier)
        )

    def test_public_key_identifier_is_correct(self):
        # STC-33
        crypto_1 = VirgilCrypto()
        key_pair_1 = crypto_1.generate_keys()
        public_key_1 = crypto_1.extract_public_key(key_pair_1.private_key)
        self.assertEqual(public_key_1.identifier, key_pair_1.public_key.identifier)
        self.assertEqual(crypto_1.export_public_key(public_key_1), crypto_1.export_public_key(key_pair_1.public_key))
        self.assertEqual(
            hashlib.sha512(bytearray(crypto_1.export_public_key(key_pair_1.public_key))).digest()[0:8],
            bytearray(key_pair_1.public_key.identifier)
        )

        crypto_2 = VirgilCrypto()
        crypto_2.use_sha256_fingerprints = True
        key_pair_2 = crypto_2.generate_keys()
        public_key_2 = crypto_2.extract_public_key(key_pair_2.private_key)
        self.assertEqual(public_key_2.identifier, key_pair_2.public_key.identifier)
        self.assertEqual(crypto_1.export_public_key(public_key_2), crypto_1.export_public_key(key_pair_2.public_key))
        self.assertEqual(
            hashlib.sha256(bytearray(crypto_1.export_public_key(key_pair_2.public_key))).digest(),
            bytearray(key_pair_2.public_key.identifier)
        )

    def test_private_key_is_der(self):
        # STC-31
        crypto = VirgilCrypto()
        key_pair_1 = crypto.generate_keys()
        private_key_data_1 = crypto.export_private_key(key_pair_1.private_key)
        self.assertEqual(VirgilKeyPair.privateKeyToDER(private_key_data_1), private_key_data_1)

        private_key_2_bytes = "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1DNENBUUF3QlFZREsyVndCQ0lFSUg4bnIyV05nblkya1ZScjRValp4UnJWVGpiMW4wWGdBZkhOWE1ocVkwaVAKLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLQo="
        private_key_2 = crypto.import_private_key(bytearray(b64decode(private_key_2_bytes)))
        private_key_2 = key_pair_1.private_key
        private_key_2_data = crypto.export_private_key(private_key_2)
        self.assertEqual(VirgilKeyPair.privateKeyToDER(private_key_2_data), private_key_2_data)

        private_key_3_bytes = "LS0tLS1CRUdJTiBFTkNSWVBURUQgUFJJVkFURSBLRVktLS0tLQpNSUdoTUYwR0NTcUdTSWIzRFFFRkRUQlFNQzhHQ1NxR1NJYjNEUUVGRERBaUJCQ3kzSkk3V0VDcGVHZGFIdEc2CktHcjRBZ0lkWXpBS0JnZ3Foa2lHOXcwQ0NqQWRCZ2xnaGtnQlpRTUVBU29FRUp1Wlpqb0oyZGJGdUpZN0ZNSisKN3g0RVFEcnRpZjNNb29rQk5PRTBUaGZmSEtrV0R3K3lvZ0ZRRk1RRFJtU0kwSXl2T2w4RTVnck5QcFNxU3dQNApIL2lzYzJvQVJzSW03alVRQXkrQjl5aTRZK3c9Ci0tLS0tRU5EIEVOQ1JZUFRFRCBQUklWQVRFIEtFWS0tLS0tCg=="
        private_key_3 = crypto.import_private_key(bytearray(b64decode(private_key_3_bytes)), password="qwerty")
        private_key_3_data = crypto.export_private_key(private_key_3)
        self.assertEqual(VirgilKeyPair.privateKeyToDER(private_key_3_data), private_key_3_data)

    def test_public_key_is_der(self):
        # STC-32
        crypto = VirgilCrypto()
        key_pair_1 = crypto.generate_keys()
        public_key_data_1 = crypto.export_public_key(key_pair_1.public_key)
        self.assertEqual(VirgilKeyPair.publicKeyToDER(public_key_data_1), public_key_data_1)

        public_key_bytes = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUNvd0JRWURLMlZ3QXlFQXYycWRHa0w2RmRxc0xpLzdPQTA1NjJPOVYvVDhFN3F6RmF0RjZMcW9TY3M9Ci0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQo="
        public_key_2 = crypto.import_public_key(bytearray(b64decode(public_key_bytes)))
        public_key_data_2 = crypto.export_public_key(public_key_2)
        self.assertEqual(VirgilKeyPair.publicKeyToDER(public_key_data_2), public_key_data_2)

    def test_signature_hash(self):
        # STC-30
        crypto = VirgilCrypto()
        key_pair = crypto.generate_keys()
        test_data = bytearray("test".encode())
        signature = crypto.sign(test_data, key_pair.private_key)

        self.assertEqual(bytearray(signature[0:17]), b64decode("MFEwDQYJYIZIAWUDBAIDBQA="))
