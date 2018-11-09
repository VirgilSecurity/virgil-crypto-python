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

from virgil_crypto.access_token_signer import AccessTokenSigner


class AccessTokenSignerTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(AccessTokenSignerTest, self).__init__(*args, **kwargs)
        self.token = bytearray("test_token".encode())
        self.signer = AccessTokenSigner()
        key_pair = self.signer.crypto.generate_keys()
        self.private_key = key_pair.private_key
        self.public_key = key_pair.public_key

    def test_generate_token_signature(self):
        self.assertIsNotNone(self.signer.generate_token_signature(self.token, self.private_key))

    def test_generate_token_signature_empty_token(self):
        self.assertRaises(ValueError, self.signer.generate_token_signature, None, self.private_key)

    def test_generate_token_signature_empty_key(self):
        self.assertRaises(ValueError, self.signer.generate_token_signature, self.token, None)

    def test_verify_token_signature(self):
        signature = self.signer.generate_token_signature(self.token, self.private_key)
        self.assertTrue(self.signer.verify_token_signature(signature, self.token, self.public_key))

    def test_verify_token_signature_wrong_signature(self):
        signature = self.signer.generate_token_signature(self.token, self.private_key)
        self.assertRaises(RuntimeError, self.signer.verify_token_signature, signature[:-2], self.token, self.public_key)
        wrong_key_pair = self.signer.crypto.generate_keys()
        self.assertFalse(self.signer.verify_token_signature(signature, self.token, wrong_key_pair.public_key))

    def test_verify_token_signature_empty_token(self):
        signature = self.signer.generate_token_signature(self.token, self.private_key)
        self.assertRaises(ValueError, self.signer.verify_token_signature, signature, None, self.public_key)

    def test_verify_token_signature_empty_key(self):
        signature = self.signer.generate_token_signature(self.token, self.private_key)
        self.assertRaises(ValueError, self.signer.verify_token_signature, signature, self.token, None)
