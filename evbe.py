#-*- coding: utf-8 -*-
"""
    Copyright (C) 2013, Roman Bondarenko

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

__version__ = '1.0.1'
__author__ = 'Roman Bondarenko'
__contact__ = 'roman@reu.org.ua'

import sys
from argparse import ArgumentParser
from pefile import PE
from struct import unpack_from, unpack


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
    ('B', 'enable_files_virtualization'),    # Enable Files Virtualization
    ('B', 'enable_registry_virtualization'),    # Enable Registry Virtualization
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
    ('4s', 'signature'),   # EVB signature
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
    ('I', ''),    # some value
    ('I', ''),    # some value
]

FILESYSTEM_DESCRIPTION = [
    ('I', 'size'),   # size of structure (0x0F)
    ('I', ''),   #
    ('I', ''),   #
    ('I', 'root_count'),
    ('H', ''),   #
    ('B', ''),   #
]

NODE_DESCRIPTION = [
    ('I', 'size'),
    ('I', ''),
    ('I', ''),
    ('I', 'files_count'),
    ('%ds', 'name'),
    ('H', ''),
    ('B', 'flag'),
]


class EVBError(Exception):
    """
        Generic EVB format error exception
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Header(object):
    """
        Virtual system header
    """
    def __init__(self, data):
        format_ = '<' + ''.join([fmt for fmt, _ in HEADER_STRUCT])
        unpacked = unpack(format_, data)
        for i in range(len(HEADER_STRUCT)):
            name = HEADER_STRUCT[i][1]
            if name == '':
                name = 'some_value_%d' % i
            setattr(self, name, unpacked[i])





class RegistryDescription(object):
    def __init__(self, data):
        pass


class Node(object):
    def __init__(self, data, skip_size=0):
        size = unpack_from('<I', data)[0] - skip_size
        format_ = '<' + ''.join([fmt for fmt, _ in NODE_DESCRIPTION])
        unpacked = unpack_from(format_ % (size - 15), data)
        for i in range(len(NODE_DESCRIPTION)):
            name = NODE_DESCRIPTION[i][1]
            if name == '':
                name = 'some_value_%d' % i
            print(name, unpacked[i])
            # setattr(self, name, unpacked[i])
        self.name = self.name.decode('utf-16')


class RootDirectory(Node):
    def __init__(self, data):
        super(RootDirectory, self).__init__(data)


class File(None):
    def __init__(self, data):
        super(File, self).__init__(data, 0x31)


class FileSystem(object):
    """
        Parse virtual file system and extracts files
    """
    class FileSystemDescription(object):
        """
            Parse filesystem description
        """
        def __init__(self, data):
            format_ = '<' + ''.join([fmt for fmt, _ in FILESYSTEM_DESCRIPTION])
            unpacked = unpack(format_, data)
            for i in range(len(FILESYSTEM_DESCRIPTION)):
                name = FILESYSTEM_DESCRIPTION[i][1]
                if name == '':
                    name = 'some_value_%d' % i
                setattr(self, name, unpacked[i])

    def __init__(self, data):
        self.offset = 0
        self.data = data

    def parse_format(self, fmt_desc):
        pass


def dump_header(header):
    s = '''
    Enable Files Virtualization:                %d
        Compress Files:                         %d
        Delete Extracted On Exit:               %d
    Enable Registry Virtualization:             %d
    Share virtual system to child processes:    %d
    Map executable files using temporary file:  %d
    Allow running of virtual executable files:  %d
    '''
    print(s %
          (header.enable_files_virtualization, header.compress_files, header.delete_on_exit,
           header.enable_registry_virtualization, header.share_virtual_system, header.using_temp_files,
           header.allow_running))
    if header.data_size > 0:
        print('    Size of data:                               %d bytes' % header.data_size)


def get_data(input_file):
    """

    """
    pe = PE(input_file, fast_load=True)
    section = None
    for s in pe.sections:
        if s.Name == '.enigma1':
            section = s
            break
    if section is None:
        raise EVBError('This file is not EVB container')

    rva = section.VirtualAddress
    header = Header(pe.get_data(rva + 0x48, 0x98))
    if header.signature != 'EVB\x00':
        # TODO: Add generic search for header
        raise EVBError('Signature not found')

    data = pe.get_data(rva + 0xE0, header.data_size)
    pe.close()

    return data, header
    # dir_header = unpack_from('<III%dsHB' % (size - 15), pe.get_data(rva + 0xF3 + 4, size))
    # objects_count, dir_name = dir_header[2], dir_header[3].decode('utf-16')
    # print(objects_count, dir_name)
    # t_rva = rva + 0xF3 + 4 + size
    # for i in range(objects_count):
    #     size = unpack_from('<I', pe.get_data(t_rva))
    #     t_rva += 4
    #     file_ = unpack_from('<III%dsHB' % (size - 15), pe.get_data(rva + 0xF3 + 4, size))[3].decode('utf-16')


def get_files(data, root_count, extract, output_dir=None):
    offset = 19
    for i in range(root_count):
        root = RootDirectory(data)
        offset += root.size
        print('%s (files: %d)' % (root.name, root.files_count))
        for


if __name__ == '__main__':
    parser = ArgumentParser(description='Enigma Virtual Box Extractor v%s, by Roman Bondarenko' % __version__)
    parser.add_argument('file', nargs='?')
    parser.add_argument('-e', help='extract data')
    parser.add_argument('-o', help='path to folder into which the data will be retrieved (default: <file name>_data)')
    args = parser.parse_args()
    if args.file is None:
        parser.print_help()
        sys.exit(2)

    data, header = get_data(args.file)
    dump_header(header)

    if header.enable_files_virtualization:
        fs_desc = FileSystemDescription(data[:19])
        get_files(data[19:], fs_desc.root_count, False)
