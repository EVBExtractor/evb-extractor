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
import sys
from argparse import ArgumentParser
from EVBE.EVBFile import EVBFile
from EVBE.EVBContainer import Container

__version__ = '1.0.9'
__author__ = 'Roman Bondarenko'
__contact__ = 'roman@reu.org.ua'

if __name__ == '__main__':
    parser = ArgumentParser(description='Enigma Virtual Box Extractor v%s, by Roman Bondarenko' % __version__)
    parser.add_argument('file', help='input file')
    parser.add_argument('-e', action='store_true', help='extract data')
    parser.add_argument('-o', dest='output_directory',
                        help='path to folder into which the data will be retrieved (default: <file name>_data)')
    args = parser.parse_args()

    file_ = EVBFile(args.file)
    if not file_.read():
        sys.exit(2)

    container = Container(file_.data, file_.offset)
    if container.read_header():
        if not args.e:
            container.info()
        else:
            output = args.output_directory
            if output is None:
                output = args.file[:-4] + '_data'
            if not os.path.exists(output):
                os.mkdir(output)
            for fs in container.read_data():
                name = os.path.join(output, fs['name'])
                if not 'offset' in fs.keys():
                    if not os.path.exists(name):
                        os.mkdir(name)
                else:
                    with open(name, 'wb+') as f:
                        offset, size = fs['offset'], fs['size']
                        f.write(file_.data[offset:offset + size])