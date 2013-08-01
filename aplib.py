#-*- coding: utf-8 -*-
"""
    Copyright (C) 2013 Roman Bondarenko

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
from struct import unpack

__author__ = 'Roman Bondarenko'
__contact__ = 'roman@reu.org.ua'


class aPLib(object):
    """
    """
    def __init__(self, source, with_header=True):
        self.source = source
        self.bitcount = 0
        self.tag = 0
        self.offset = unpack('<I', source[:4])[0] if with_header else 0

    def getbit(self):
        self.bitcount -= 1
        if self.bitcount + 1 == 0:
            self.tag = ord(self.source[self.offset])
            self.offset += 1
            self.bitcount = 7
        bit = (self.tag >> 7) & 1
        self.tag <<= 1
        return bit

    def getgamma(self):
        result = 1
        while True:
            result = (result << 1) + self.getbit()
            if self.getbit() == 0:
                break
        return result

    def depack(self):
        offs = 0
        len_ = 0
        R0 = 0
        done = 0
        LWM = 0

        destination = self.source[self.offset]
        self.offset += 1

        while done == 0:
            if self.getbit() != 0:
                if self.getbit() != 0:
                    if self.getbit() != 0:
                        offs = 0
                        for i in range(4):
                            offs = (offs << 1) + self.getbit()
                        if offs != 0:
                            destination += destination[len(destination) - offs]
                        else:
                            destination += '\x00'
                        LWM = 0
                    else:
                        offs = ord(self.source[self.offset])
                        self.offset += 1
                        len_ = 2 + (offs & 1)
                        offs >>= 1
                        if offs != 0:
                            for i in range(len_):
                                destination += destination[len(destination) - offs]
                        else:
                            done = 1
                        R0 = offs
                        LWM = 1
                else:
                    offs = self.getgamma()
                    if LWM == 0 and offs == 2:
                        offs = R0
                        len_ = self.getgamma()
                        for i in range(len_):
                            destination += destination[len(destination) - offs]
                    else:
                        if LWM == 0:
                            offs -= 3
                        else:
                            offs -= 2
                        offs <<= 8
                        offs += ord(self.source[self.offset])
                        self.offset += 1
                        len_ = self.getgamma()
                        if offs >= 32000:
                            len_ += 1
                        if offs >= 1280:
                            len_ += 1
                        if offs < 128:
                            len_ += 2
                        for i in range(len_):
                            destination += destination[len(destination) - offs]
                        R0 = offs
                    LWM = 1
            else:
                destination += self.source[self.offset]
                self.offset += 1
                LWM = 0
        return destination
