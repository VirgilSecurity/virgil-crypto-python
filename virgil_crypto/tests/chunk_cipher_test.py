import io
import unittest

from virgil_crypto.virgil_crypto_python import VirgilChunkCipher
from virgil_crypto.virgil_crypto_python import VirgilKeyPair
from virgil_crypto.streams import VirgilStreamDataSink
from virgil_crypto.streams import VirgilStreamDataSource

class VirgilChunkCipherTest(unittest.TestCase):
    def test_encrypts_and_decrypts_data(self):
        raw_data = bytearray("test", "utf-8")
        key_pair1 = VirgilKeyPair.generate(VirgilKeyPair.Type_FAST_EC_ED25519)
        key_pair2 = VirgilKeyPair.generate(VirgilKeyPair.Type_FAST_EC_ED25519)
        cipher = VirgilChunkCipher()
        cipher.addKeyRecipient(bytearray("1", "utf-8"), key_pair1.publicKey())
        cipher.addKeyRecipient(bytearray("2", "utf-8"), key_pair2.publicKey())
        encrypt_input_stream = io.BytesIO(raw_data)
        encrypt_output_stream = io.BytesIO()
        encrypt_source = VirgilStreamDataSource(encrypt_input_stream)
        encrypt_sink = VirgilStreamDataSink(encrypt_output_stream)
        cipher.encrypt(encrypt_source, encrypt_sink)
        encrypted_data = encrypt_output_stream.getvalue()
        decrypt_input_stream = io.BytesIO(encrypted_data)
        decrypt_output_stream = io.BytesIO()
        decrypt_source = VirgilStreamDataSource(decrypt_input_stream)
        decrypt_sink = VirgilStreamDataSink(decrypt_output_stream)
        cipher = VirgilChunkCipher()
        cipher.decryptWithKey(
            decrypt_source,
            decrypt_sink,
            bytearray("1", "utf-8"),
            key_pair1.privateKey()
        )
        decrypted_data1 = decrypt_output_stream.getvalue()
        self.assertEqual(
            raw_data,
            bytearray(decrypted_data1)
        )
        decrypt_input_stream = io.BytesIO(encrypted_data)
        decrypt_output_stream = io.BytesIO()
        decrypt_source = VirgilStreamDataSource(decrypt_input_stream)
        decrypt_sink = VirgilStreamDataSink(decrypt_output_stream)
        cipher.decryptWithKey(
            decrypt_source,
            decrypt_sink,
            bytearray("2", "utf-8"),
            key_pair2.privateKey()
        )
        decrypted_data2 = decrypt_output_stream.getvalue()
        self.assertEqual(
            raw_data,
            bytearray(decrypted_data2)
        )
