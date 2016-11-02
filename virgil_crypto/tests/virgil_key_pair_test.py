import io
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
