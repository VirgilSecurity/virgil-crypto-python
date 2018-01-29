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

from virgil_crypto.virgil_crypto_python import VirgilDataSink
from virgil_crypto.virgil_crypto_python import VirgilDataSource


class VirgilStreamDataSink(VirgilDataSink):
    def __init__(self, stream):
        super(VirgilStreamDataSink, self).__init__()
        self.stream = stream

    def isGood(self):
        return self.stream.writable()

    def write(self, data):
        self.stream.write(bytearray(data))


class VirgilStreamDataSource(VirgilDataSource):
    def __init__(self, stream, buffer_size=1024):
        super(VirgilStreamDataSource, self).__init__()
        self.stream = stream
        self.has_data = True
        self.buffer = bytearray(buffer_size)

    def hasData(self):
        return self.stream.readable() and self.has_data

    def read(self):
        read_count = self.stream.readinto(self.buffer)
        if not read_count:
            self.has_data = False
            return []
        return self.buffer[0:read_count]
