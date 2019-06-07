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
from virgil_crypto_lib.foundation import AlgId


class KeyPairType(object):
    """Enumeration containing supported KeyPairTypes"""

    class KeyType(object):

        def __init__(self, alg_id, rsa_bitlen=None):
            self._alg_id = alg_id
            self._rsa_bitlen = rsa_bitlen

        def __eq__(self, other):
            return self.alg_id == other.alg_id and self.rsa_bitlen == other.rsa_bitlen

        @property
        def alg_id(self):
            return self._alg_id

        @property
        def rsa_bitlen(self):
            return self._rsa_bitlen

    class UnknownTypeException(Exception):
        """Exception raised when Unknown Type passed to convertion method"""

        def __init__(self, key_pair_type):
            super(KeyPairType.UnknownTypeException, self).__init__(key_pair_type)
            self.key_pair_type = key_pair_type

        def __str__(self):
            return "KeyPairType not found: %i" % self.key_pair_type

    CURVE25519 = KeyType(AlgId.CURVE25519)
    ED25519 = KeyType(AlgId.ED25519)
    RSA_2048 = KeyType(AlgId.RSA, 2048)
    RSA_4096 = KeyType(AlgId.RSA, 4096)
    RSA_8192 = KeyType(AlgId.RSA, 8192)
