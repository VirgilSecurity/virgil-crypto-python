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

from virgil_crypto import VirgilCrypto
from virgil_crypto.private_key_exporter import PrivateKeyExporter


class PrivateKeyExporterTest(unittest.TestCase):

    def test_export_private_key_with_password(self):
        crypto = VirgilCrypto()
        key_pair = crypto.generate_keys()
        passwd = "test"
        pke = PrivateKeyExporter(passwd)
        exported_key_data = pke.export_private_key(key_pair.private_key)
        self.assertIsNotNone(exported_key_data)
        self.assertEqual(crypto.import_private_key(exported_key_data, passwd), key_pair.private_key)

    def test_import_private_key_with_password(self):
        crypto = VirgilCrypto()
        key_pair = crypto.generate_keys()
        passwd = "test"
        pke = PrivateKeyExporter(passwd)
        exported_key_data = pke.export_private_key(key_pair.private_key)
        imported_key = pke.import_private_key(exported_key_data)
        self.assertIsNotNone(imported_key)
        self.assertEqual(imported_key, key_pair.private_key)

    def test_export_private_key(self):
        crypto = VirgilCrypto()
        key_pair = crypto.generate_keys()
        pke = PrivateKeyExporter()
        exported_key_data = pke.export_private_key(key_pair.private_key)
        self.assertIsNotNone(exported_key_data)
        self.assertEqual(crypto.export_private_key(key_pair.private_key), exported_key_data)

    def test_import_private_key(self):
        crypto = VirgilCrypto()
        key_pair = crypto.generate_keys()
        pke = PrivateKeyExporter()
        exported_key_data = pke.export_private_key(key_pair.private_key)
        imported_key = pke.import_private_key(exported_key_data)
        self.assertIsNotNone(imported_key)
        self.assertEqual(imported_key, key_pair.private_key)
