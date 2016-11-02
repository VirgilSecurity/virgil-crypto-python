import io
import unittest

from virgil_crypto.virgil_crypto_python import VirgilKeyPair
from virgil_crypto.virgil_crypto_python import VirgilSigner

class VirgilSignerTest(unittest.TestCase):
    def test_signs_and_verifies_data(self):
        raw_data = bytearray("test", "utf-8")
        key_pair = VirgilKeyPair.generate(VirgilKeyPair.Type_FAST_EC_ED25519)
        signer = VirgilSigner()
        signature = signer.sign(raw_data, key_pair.privateKey())
        signer = VirgilSigner()
        is_valid = signer.verify(raw_data, signature, key_pair.publicKey())
        self.assertTrue(is_valid)
