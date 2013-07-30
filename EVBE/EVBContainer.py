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
from EVBE.EVBDataParser import DataParser
from EVBE.EVBFileSystem import FileSystem

__author__ = 'Roman Bondarenko'
__contact__ = 'roman@reu.org.ua'


HEADER_STRUCT = [
    ('I', ''),    # some value
    ('I', ''),    # some value (maybe size or address)
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value (maybe size)
    ('I', ''),    # some value
    ('I', ''),    # some value (some size)
    ('B', 'compress_files'),    # Compress Files
    ('B', 'delete_on_exit'),    # Delete Extracted On Exit
    ('H', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('Q', ''),    # some value
    ('B', 'files_virtualization'),    # Enable Files Virtualization
    ('B', 'registry_virtualization'),    # Enable Registry Virtualization
    ('B', 'share_virtual_system'),    # Share virtual system to child processes
    ('B', 'using_temp_files'),    # Map executable files using temporary file
    ('B', 'allow_running'),    # Allow running of virtual executable files
    ('B', ''),    #
    ('B', ''),    #
    ('B', ''),    #
    ('B', ''),    #
    ('B', ''),    #
    ('B', ''),    #
    ('B', ''),    #
    ('I', ''),    #
    ('4s', 'signature'),   # EVB signature ('EVB\x00')
    ('I', ''),    # some value
    ('Q', 'env_value'),    # environment value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', 'data_size'),    # size of data
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some value
    ('I', ''),    # some size
    ('I', ''),    # some value
    ('I', 'registry_size'),    # size of registry data
    ('I', ''),    # some value
]


class Container(object):
    class Header(object):
        signature = None
        files_virtualization = 0
        compress_files = 0
        delete_on_exit = 0
        registry_virtualization = 0
        share_virtual_system = 0
        using_temp_files = 0
        allow_running = 0
        data_size = 0
        registry_size = 0

    def __init__(self, data, offset=0):
        self.data = data
        self.offset = offset
        self.header = self.Header

    def read_header(self):
        if len(self.data) < 0x98:
            print('Header is too small')
            return False

        DataParser(self.header, self.data, HEADER_STRUCT, self.offset)

        if self.header.signature != 'EVB\x00':
            print('Signature not found')
            return False

        self.offset += 0x98
        return True

    def read_data(self):
        if self.header.files_virtualization:
            fs = FileSystem(self.data, self.header.data_size, self.offset)
            fs.enum()
            return fs.files
        return []

    def info(self):
        s = '''
        Enable Files Virtualization:                %s
            Compress Files:                         %s
            Delete Extracted On Exit:               %s
        Enable Registry Virtualization:             %s
        Share virtual system to child processes:    %s
        Map executable files using temporary file:  %s
        Allow running of virtual executable files:  %s

        Size of file data:                          %d
        Size of registry data                       %d
        '''
        u = lambda i: 'Disabled' if i == 0 else 'Unknown value: %d' % i
        f = lambda i: 'Enabled' if i == 1 else u(i)
        print(s %
              (f(self.header.files_virtualization), f(self.header.compress_files), f(self.header.delete_on_exit),
               f(self.header.registry_virtualization), f(self.header.share_virtual_system),
               f(self.header.using_temp_files), f(self.header.allow_running),
               self.header.data_size, self.header.registry_size))