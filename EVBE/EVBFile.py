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
from pefile import PE

__author__ = 'Roman Bondarenko'
__contact__ = 'roman@reu.org.ua'


class EVBFile(object):
    def __init__(self, name):
        self.name = name
        self.data = None
        self.offset = 0x48

    # TODO: Add generic search for container
    def read(self):
        try:
            pe = PE(self.name, fast_load=True)
        except:
            print('File %s invalid' % self.name)
            return False

        if not pe.is_exe():
            print('This file is not exe')
            pe.close()
            return False

        section = None
        for s in pe.sections:
            if s.Name == '.enigma1':
                section = s
                break

        if section is None:
            print('This file is not Enigma Virtual Box container')
            pe.close()
            return False

        self.data = pe.get_data(section.VirtualAddress, section.SizeOfRawData)

        pe.close()

        return True