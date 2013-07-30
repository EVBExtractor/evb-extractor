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
import os
from EVBE.EVBDataParser import DataParser

__author__ = 'Roman Bondarenko'
__contact__ = 'roman@reu.org.ua'

from struct import unpack_from

NODE = [
    ('I', 'size'),
    ('I', ''),
    ('I', ''),
    ('I', 'objects_count'),
]

NAMED_NODE = [
    ('%ds', 'name'),
    ('H', ''),
    ('B', 'type'),
]

OPTIONAL = [
    ('H', ''),
    ('I', 'original_size'),
    ('I', ''),
    ('Q', ''),
    ('Q', ''),
    ('Q', ''),
    ('B', ''),
    ('H', ''),
    ('I', ''),
    ('I', 'stored_size'),
    ('I', ''),
]


class FileSystem(object):
    """
        Parse virtual file system
    """
    class Node(object):
        """
            Directory or file
        """
        size = 0
        objects_count = 0
        name = None
        type = 0
        stored_size = 0
        original_size = 0
        name_exist = 0

        def __init__(self, data, offset):
            DataParser(self, data, NODE, offset)
            i = 0
            while unpack_from('<H', data, offset + 16 + i * 2)[0] != 0:
                i += 1
            DataParser(self, data, NAMED_NODE, offset + 16, i * 2)
            if self.name != '':
                self.name = self.name.decode('utf-16')
            if self.type == 2:
                DataParser(self, data, OPTIONAL, offset + 4 + self.size - 0x31)

    def __init__(self, data, size, offset=0):
        self.offset = offset
        self.size = size
        self.files = []
        self.data = data

    def enum(self, prefix=''):
        node = self.Node(self.data, self.offset)
        self.offset += (node.size + 4)
        if prefix != '':
            self.files.append(dict(name=prefix))
        for i in range(node.objects_count):
            child = self.Node(self.data, self.offset)
            if child.type == 3:
                self.enum(os.path.join(prefix, child.name))
            else:
                self.offset += child.size + 4
                self.files.append(dict(name=os.path.join(prefix, child.name), offset=self.offset, size=child.stored_size))
                self.offset += child.stored_size
