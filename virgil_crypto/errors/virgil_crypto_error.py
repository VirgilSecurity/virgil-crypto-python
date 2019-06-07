# Copyright (C) 2016-2019 Virgil Security Inc.
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


class VirgilCryptoError(Exception):

    def __init__(self, message):
        super(Exception, self).__init__(message)


class VirgilCryptoErrors(object):

    SIGNER_NOT_FOUND = VirgilCryptoError("Signer not found")
    SIGNATURE_NOT_FOUND = VirgilCryptoError("Signature not found")
    SIGNATURE_NOT_VERIFIED = VirgilCryptoError("Signature not verified")
    UNKNOWN_ALG_ID = VirgilCryptoError("Unknown alg id")
    RSA_SHOULD_BE_CONSTRUCTED_DIRECTLY = VirgilCryptoError("Rsa should be constructed directly")
    UNSUPPORTED_RSA_LENGTH = VirgilCryptoError("Unsupported rsa length")
    KEY_DOESNT_SUPPORT_SIGNING = VirgilCryptoError("Key doesn't support signing")
    PASSED_KEY_IS_NOT_VIRGIL = VirgilCryptoError("Passed key is not virgil")
    OUTPUT_STREAM_ERROR = VirgilCryptoError("Output stream has no space left")
    INPUT_STREAM_ERROR = VirgilCryptoError("Output stream has no space left")
    INVALID_SEED_SIZE = VirgilCryptoError("Invalid seed size")
