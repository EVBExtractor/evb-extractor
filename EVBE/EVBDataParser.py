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
from struct import unpack_from

__author__ = 'Roman Bondarenko'
__contact__ = 'roman@reu.org.ua'


class DataParser(object):
    def __init__(self, obj, data, fmt, offset=0, str_size=-1):
        format_ = '<' + ''.join([f for f, _ in fmt])
        if str_size >= 0:
            format_ = format_ % str_size
        unpacked = unpack_from(format_, data, offset)
        for i in range(len(fmt)):
            name = fmt[i][1]
            if name == '':
                name = 'some_value_%d' % i
            setattr(obj, name, unpacked[i])