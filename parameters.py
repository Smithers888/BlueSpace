#!/usr/bin/env python3

# Copyright (C) 2014 Christopher Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name of the author shall not be used
# in advertising or otherwise to promote the sale, use or other dealings in
# this Software without prior written authorization from the author.

class numparam:
    tr = str.maketrans(' \t', '01')
    
    def parse(parser):
        i = parser.i
        j = parser.code.find('\n', i)
        if j < 0:
            raise RuntimeError('BlueSpace: Failed to parse, unterminated integer')
        elif j == i:
            raise RuntimeError('BlueSpace: Failed to parse, empty integer')
        n = 0 if j == i+1 else int(parser.code[i+1:j].translate(numparam.tr), 2)
        if parser.code[i] == '\t':
            n = -n
        parser.i = j + 1
        return numparam(n)
    
    def __init__(self, n):
        self.value = n
    
    def __str__(self):
        return str(self.value)

class stringparam:
    tr = str.maketrans(' \t', 'st')
    
    def parse(parser):
        i = parser.i
        j = parser.code.find('\n', i)
        if j < 0:
            raise RuntimeError('BlueSpace: Failed to parse, unterminated label')
        parser.i = j + 1
        return stringparam(parser.code[i:j])
    
    def __init__(self, s):
        self.value = s
    
    def __str__(self):
        return self.value.translate(stringparam.tr) + 'n'
