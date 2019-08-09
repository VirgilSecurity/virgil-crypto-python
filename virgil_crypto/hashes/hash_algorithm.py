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
from virgil_crypto_lib.foundation import Sha224, Sha256, Sha384, Sha512


class HashAlgorithm(object):
    """Enumeration containing supported Algorithms"""

    class UnknownAlgorithmException(Exception):
        """Exception raised when Unknown Algorithm passed to convertion method"""

        def __init__(self, algorithm):
            super(HashAlgorithm.UnknownAlgorithmException, self).__init__(algorithm)
            self.algorithm = algorithm

        def __str__(self):
            return "KeyPairType not found: %i" % self.algorithm
    SHA224 = 0
    SHA256 = 1
    SHA384 = 2
    SHA512 = 3

    _ALGORITHMS_TO_NATIVE = {
        SHA224: Sha224,
        SHA256: Sha256,
        SHA384: Sha384,
        SHA512: Sha512,
    }

    @classmethod
    def convert_to_native(cls, algorithm):
        # type: (int) -> Type[Union[Sha224, Sha256, Sha384, Sha512]]
        """Converts algorithm enum value to native value

        Args:
            algorithm: algorithm for conversion.

        Returns:
            Native library algorithm id.

        Raises:
            UnknownAlgorithmException: if algorithm is not supported.
        """
        if algorithm in cls._ALGORITHMS_TO_NATIVE:
            return cls._ALGORITHMS_TO_NATIVE[algorithm]
        raise cls.UnknownAlgorithmException(algorithm)
