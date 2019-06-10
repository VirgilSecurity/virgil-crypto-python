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
from virgil_crypto_lib.foundation import CtrDrbg, Signer, Sha512, Verifier, Aes256Gcm, RecipientCipher, KeyProvider, \
    KeyMaterialRng, PublicKey, KeyAsn1Serializer, AlgId

from virgil_crypto.errors.virgil_crypto_error import VirgilCryptoErrors
from virgil_crypto.keys import VirgilKeyPair
from virgil_crypto.keys import KeyPairType
from virgil_crypto.keys import VirgilPrivateKey
from virgil_crypto.keys import VirgilPublicKey
from virgil_crypto.hashes import HashAlgorithm


class VirgilCrypto(object):
    """Wrapper for cryptographic operations.

    Class provides a cryptographic operations in applications, such as hashing,
    signature generation and verification, and encryption and decryption

    """

    CUSTOM_PARAM_KEY_SIGNATURE = bytearray("VIRGIL-DATA-SIGNATURE".encode())
    CUSTOM_PARAM_KEY_SIGNER_ID = bytearray("VIRGIL-DATA-SIGNER-ID".encode())

    def __init__(self, default_key_pair_type=KeyPairType.ED25519, use_sha256_fingerprints=False):
        rng = CtrDrbg()
        rng.setup_defaults()
        self.rng = rng
        self.key_pair_type = default_key_pair_type
        self.use_sha256_fingerprints = use_sha256_fingerprints
        self.chunk_size = 1024

    class SignatureIsNotValid(Exception):
        """Exception raised when Signature is not valid"""
        def __init__(self):
            super(VirgilCrypto.SignatureIsNotValid, self).__init__()

        def __str__(self):
            return "Signature is not valid"

    @staticmethod
    def strtobytes(source):
        # type: (str) -> Tuple[int]
        """Convert string to bytes tuple used for all crypto methods.

        Args:
            source: String for conversion.

        Returns:
            Tuple containing bytes from converted source string.
        """
        return tuple(bytearray(source, 'utf-8'))

    def generate_key_pair(self, key_type=KeyPairType.ED25519, seed=None):
        # type: (KeyPairType.KeyType, Union[Tuple[int], bytearray]) -> VirgilKeyPair
        """Generates asymmetric key pair that is comprised of both public and private keys by specified type.

        Args:
            key_type: type of the generated keys.
                The possible values can be found in KeyPairType enum.
            seed: random value used to generate key

        Returns:
            Generated key pair.
        """

        if seed:
            if KeyMaterialRng.KEY_MATERIAL_LEN_MIN > len(seed) > KeyMaterialRng.KEY_MATERIAL_LEN_MAX:
                raise VirgilCryptoErrors.INVALID_SEED_SIZE
            key_material_rng = KeyMaterialRng()
            key_material_rng.reset_key_material(seed)
            rng = key_material_rng
        else:
            rng = self.rng

        key_provider = KeyProvider()

        key_provider.set_random(rng)

        if key_type.rsa_bitlen:
            key_provider.set_rsa_params(key_type.rsa_bitlen)

        key_provider.setup_defaults()

        private_key = key_provider.generate_private_key(key_type.alg_id)
        public_key = private_key.extract_public_key()

        key_id = self.compute_public_key_identifier(public_key)

        return VirgilKeyPair(
            private_key=VirgilPrivateKey(identifier=key_id, private_key=private_key, key_type=key_type),
            public_key=VirgilPublicKey(identifier=key_id, public_key=public_key, key_type=key_type)
        )

    def import_private_key(self, key_data):
        # type: (Union[Tuple[int], List[int]], bytearray) -> VirgilKeyPair
        """Imports private key from DER or PEM format

        Args:
            key_data: Private key in DER or PEM format.

        Returns:
            VirgilKeyPair.
        """
        key_provider = KeyProvider()
        key_provider.set_random(self.rng)

        key_provider.setup_defaults()

        private_key = key_provider.import_private_key(bytearray(key_data))

        if private_key.alg_id() == AlgId.RSA:
            key_type = KeyPairType.KeyType(private_key.alg_id(), private_key.key_bitlen())
        else:
            key_type = KeyPairType.KeyType(private_key.alg_id())

        public_key = private_key.extract_public_key()

        key_id = self.compute_public_key_identifier(public_key)

        return VirgilKeyPair(
            private_key=VirgilPrivateKey(identifier=key_id, private_key=private_key, key_type=key_type),
            public_key=VirgilPublicKey(identifier=key_id, public_key=public_key, key_type=key_type)
        )

    def import_public_key(self, key_data):
        # type: (Union[Tuple[int], List[int]]) -> VirgilPublicKey
        """Imports the Public key from material representation.

        Args:
            key_data: key material representation bytes.

        Returns:
            Imported public key.
        """
        if not key_data:
            raise ValueError("Key data missing")

        key_provider = KeyProvider()
        key_provider.set_random(self.rng)
        key_provider.setup_defaults()

        public_key = key_provider.import_public_key(bytearray(key_data))
        if public_key.alg_id() == AlgId.RSA:
            key_type = KeyPairType.KeyType(public_key.alg_id(), public_key.key_bitlen())
        else:
            key_type = KeyPairType.KeyType(public_key.alg_id())

        key_id = self.compute_public_key_identifier(public_key)
        return VirgilPublicKey(
            identifier=key_id,
            public_key=public_key,
            key_type=key_type
        )

    @staticmethod
    def export_private_key(private_key):
        # type: (VirgilPrivateKey) -> Union[Tuple[int], bytearray]
        """Exports private key to DER format

        Args:
            private_key: private key for export.


        Returns:
            Private key in DER format
        """
        serializer = KeyAsn1Serializer()
        serializer.setup_defaults()
        return serializer.serialize_private_key(private_key.private_key)

    @staticmethod
    def export_public_key(public_key):
        # type: (VirgilPrivateKey) -> Union[Tuple[int], bytearray]
        """Exports the Public key into material representation.

        Args:
            public_key: public key for export.

        Returns:
            Key material representation bytes.
        """
        serializer = KeyAsn1Serializer()
        serializer.setup_defaults()

        return serializer.serialize_public_key(public_key.public_key)

    @staticmethod
    def extract_public_key(private_key):
        # type: (VirgilPrivateKey) -> VirgilPublicKey
        """Extracts the Public key from Private key.

        Args:
            private_key: source private key for extraction.

        Returns:
            Exported public key.
        """
        return VirgilPublicKey(
            identifier=private_key.identifier,
            public_key=private_key.private_key.extract_public_key(),
            key_type=private_key.key_type
        )

    def encrypt(self, data, *recipients):
        # type: (Union[Tuple[int], List[int], bytearray], List[VirgilPublicKey]) -> Union[Tuple[int], bytearray]
        """Encrypts the specified data using recipients Public keys.

        Args:
            data: raw data bytes for encryption.
            recipients: list of recipients' public keys.

        Returns:
            Encrypted data bytes.
        """
        aes_gcm = Aes256Gcm()
        cipher = RecipientCipher()
        cipher.set_encryption_cipher(aes_gcm)
        cipher.set_random(self.rng)

        for public_key in recipients:
            cipher.add_key_recipient(public_key.identifier, public_key.public_key)

        cipher.start_encryption()
        result = cipher.pack_message_info()
        result += cipher.process_encryption(bytearray(data))
        result += cipher.finish_encryption()

        return result

    @staticmethod
    def decrypt(data, private_key):
        # type: (Union[Tuple[int], List[int]], VirgilPrivateKey) -> Tuple[int]
        """Decrypts the specified data using Private key.

        Args:
            data: encrypted data bytes for decryption.
            private_key: private key for decryption.

        Returns:
            Decrypted data bytes.
        """
        cipher = RecipientCipher()

        cipher.start_decryption_with_key(
            private_key.identifier,
            private_key.private_key,
            bytearray()
        )
        result = bytearray()
        result += cipher.process_decryption(bytearray(data))
        result += cipher.finish_decryption()
        return result

    def sign_then_encrypt(self, data, private_key, *recipients):
        # type: (Union[Tuple[int], List[int], bytearray], VirgilPrivateKey, List[VirgilPublicKey]) -> Union[Tuple[int], bytearray]
        """Signs and encrypts the data.

        Args:
            data: data bytes for signing and encryption.
            private_key: sender private key
            recipients: list of recipients' public keys.
                Used for data encryption.

        Returns:
            Signed and encrypted data bytes.
        """
        signature = self.generate_signature(bytearray(data), private_key)

        aes_gcm = Aes256Gcm()
        cipher = RecipientCipher()

        cipher.set_encryption_cipher(aes_gcm)
        cipher.set_random(self.rng)

        for recipient in recipients:
            cipher.add_key_recipient(recipient.identifier, recipient.public_key)

        cp = cipher.custom_params()
        cp.add_data(VirgilCrypto.CUSTOM_PARAM_KEY_SIGNATURE, signature)
        cp.add_data(VirgilCrypto.CUSTOM_PARAM_KEY_SIGNER_ID, private_key.identifier)

        cipher.start_encryption()
        result = cipher.pack_message_info()
        result += cipher.process_encryption(bytearray(data))
        result += cipher.finish_encryption()

        return result

    def decrypt_then_verify(self, data, private_key, signers_public_keys):
        # type: (Union[Tuple[int], List[int], bytearray], VirgilPrivateKey, Union[List[VirgilPublicKey], VirgilPublicKey]) -> Union[Tuple[int], bytearray]
        """Decrypts and verifies the data.

        Args:
            data: encrypted data bytes.
            private_key: private key for decryption.
            signers_public_keys: List of possible signers public keys.
                                 WARNING: data should have signature of ANY public key from list.
        Returns:
            Decrypted data bytes.

        Raises:
            VirgilCryptoError: if signature is not verified.
        """

        cipher = RecipientCipher()

        cipher.start_decryption_with_key(private_key.identifier, private_key.private_key, bytearray())
        result = bytearray()

        result += cipher.process_decryption(bytearray(data))
        result += cipher.finish_decryption()

        if isinstance(signers_public_keys, VirgilPublicKey):
            signer_public_key = signers_public_keys
        else:
            try:
                signer_id = bytearray(cipher.custom_params().find_data(VirgilCrypto.CUSTOM_PARAM_KEY_SIGNER_ID))
            except Exception:
                raise VirgilCryptoErrors.SIGNER_NOT_FOUND

            filtered_public_keys = list(filter(lambda x: x.identifier == signer_id, signers_public_keys))
            if not filtered_public_keys:
                raise VirgilCryptoErrors.SIGNER_NOT_FOUND

            signer_public_key = filtered_public_keys[0]

        signature = bytearray(cipher.custom_params().find_data(VirgilCrypto.CUSTOM_PARAM_KEY_SIGNATURE))

        is_valid = self.verify_signature(result, signature, signer_public_key)
        if not is_valid:
            raise VirgilCryptoErrors.SIGNATURE_NOT_VERIFIED
        return result

    @staticmethod
    def generate_signature(data, private_key):
        # type: (Union[Tuple[int], List[int], bytearray], VirgilPrivateKey) -> Union[Tuple[int], bytearray]
        """Generates digital signature of data using private key

        Args:
            data: raw data bytes for signing.
            private_key: private key for signing.

        Returns:
            Signature bytes.
        """
        signer = Signer()
        signer.set_hash(Sha512())
        signer.reset()
        signer.update(bytearray(data))
        signature = signer.sign(private_key.private_key)
        return signature

    @staticmethod
    def verify_signature(data, signature, public_key):
        # type: (Union[Tuple[int], List[int], bytearray], Union[Tuple[int], List[int], bytearray], VirgilPublicKey) -> bool
        """Verifies the specified signature using original data and signer's public key.

        Args:
            data: original data bytes for verification.
            signature: signature bytes for verification.
            public_key: signer public key for verification.

        Returns:
            True if signature is valid, False otherwise.
        """
        verifier = Verifier()
        verifier.reset(bytearray(signature))
        verifier.update(bytearray(data))
        return verifier.verify(public_key.public_key)

    def encrypt_stream(self, input_stream, output_stream, *recipients):
        # type: (io.IOBase, io.IOBase, List[VirgilPublicKey]) -> None
        """Encrypts the specified stream using recipients Public keys.

        Args:
            input_stream: readable stream containing input data.
            output_stream: writable stream for output.
            recipients: list of recipients' public keys.

        """

        aes_gcm = Aes256Gcm()
        cipher = RecipientCipher()

        cipher.set_encryption_cipher(aes_gcm)
        cipher.set_random(self.rng)

        for public_key in recipients:
            cipher.add_key_recipient(public_key.identifier, public_key.public_key)

        cipher.start_encryption()

        msg_info = cipher.pack_message_info()

        if output_stream.closed:
            output_stream.open()

        output_stream.write(msg_info)

        self.__for_each_chunk_output(input_stream, output_stream, cipher.process_encryption)

        finish = cipher.finish_encryption()

        output_stream.write(finish)

    def decrypt_stream(self, input_stream, output_stream, private_key):
        # type: (io.IOBase, io.IOBase, VirgilPrivateKey) -> None
        """Decrypts the specified stream using Private key.

        Args:
            input_stream: readable stream containing input data.
            output_stream: writable stream for output.
            private_key: private key for decryption.

        """
        cipher = RecipientCipher()
        cipher.start_decryption_with_key(
            private_key.identifier,
            private_key.private_key,
            bytearray()
        )

        self.__for_each_chunk_output(input_stream, output_stream, cipher.process_decryption)

        finish = cipher.finish_decryption()
        output_stream.write(finish)

    def generate_stream_signature(self, input_stream, private_key):
        # type: (Type[io.IOBase], VirgilPrivateKey) -> Tuple(*int)
        """Signs the specified stream using Private key.

        Args:
            input_stream: readable stream containing input data.
            private_key: private key for signing.

        Returns:
            Signature bytes.
        """
        signer = Signer()
        signer.set_hash(Sha512())
        signer.reset()

        self.__for_each_chunk_input(input_stream, signer.update)

        signature = signer.sign(private_key.private_key)
        return signature

    def verify_stream_signature(self, input_stream, signature, signer_public_key):
        # type: (io.IOBase, Union[Tuple[int], List[int], bytearray], VirgilPublicKey) -> bool
        """Verifies the specified signature using original stream and signer's Public key.

        Args:
            input_stream: readable stream containing input data.
            signature: signature bytes for verification.
            signer_public_key: signer public key for verification.

        Returns:
            True if signature is valid, False otherwise.
        """
        verifier = Verifier()
        verifier.reset(bytearray(signature))

        self.__for_each_chunk_input(input_stream, verifier.update)
        return verifier.verify(signer_public_key.public_key)

    @staticmethod
    def compute_hash(data, algorithm=HashAlgorithm.SHA512):
        # type: (Union[Tuple[int], List[int], bytearray], int) -> Tuple[int]
        """Computes the hash of specified data.

        Args:
            data: data bytes for fingerprint calculation.
            algorithm: hashing algorithm.
                The possible values can be found in HashAlgorithm enum.

        Returns:
            Hash bytes.
        """
        native_algorithm = HashAlgorithm.convert_to_native(algorithm)
        native_hasher = native_algorithm()
        return native_hasher.hash(bytearray(data))

    def compute_public_key_identifier(self, public_key):
        # type: (PublicKey) -> Tuple[int]
        """Computes public key identifier.

        Note: Takes first 8 bytes of SHA512 of public key DER if use_sha256_fingerprints=False
            and SHA256 of public key der if use_sha256_fingerprints=True

        Args:
            public_key: public key for compute.

        Returns:
            Public key identifier.
        """
        serializer = KeyAsn1Serializer()
        serializer.setup_defaults()

        public_key_data = serializer.serialize_public_key(public_key)

        if self.use_sha256_fingerprints:
            return self.compute_hash(public_key_data, HashAlgorithm.SHA256)
        return self.compute_hash(public_key_data)[:8]

    def generate_random_data(self, data_size):
        # type: (int) -> Tuple[int]
        """Generates cryptographically secure random bytes. Uses CTR DRBG

        Args:
            data_size: size needed

        Returns:
            Random data
        """
        return self.rng.random(data_size)

    def __for_each_chunk_input(self, input_stream, stream_callback):
        if input_stream.closed:
            input_stream.open()

        while True:
            chunk = input_stream.read(self.chunk_size)
            if not chunk:
                break
            stream_callback(chunk)

    def __for_each_chunk_output(self, input_stream, output_stream, stream_callback):
        if input_stream.closed:
            input_stream.open()

        if output_stream.closed:
            output_stream.open()

        while True:
            chunk = input_stream.read(self.chunk_size)
            if not chunk:
                break
            output_stream.write(stream_callback(chunk))
