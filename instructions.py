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

from parameters import numparam, stringparam

import sys

class instruction:
    def __init__(self, itype, param):
        self.rep = itype.rep
        self.name = itype.name
        self.param = param
    
    def towhitespace(self):
        if self.param is None:
            return self.rep
        else:
            return self.rep + self.param.towhitespace()
    
    def toprintable(self):
        tr = str.maketrans(' \t\n', 'stn')
        if self.param is None:
            return self.rep.translate(tr)
        else:
            return self.rep.translate(tr) + ' ' + self.param.towhitespace().translate(tr)
    
    def toassembly(self):
        if self.param is None:
            return self.name
        else:
            return self.name + ' ' + self.param.toassembly()

class instructiontype:
    def __init__(self, rep, name, paramtype=None):
        self.rep = rep
        self.name = name
        self.paramtype = paramtype
    
    def parse(self, parser):
        if self.paramtype is not None:
            param = self.paramtype.parse(parser)
        else:
            param = None
        return instruction(self, param)

instructions = [
    # Stack instructions (' ')
    instructiontype('  ', 'Push', numparam),
    instructiontype(' \n ', 'Duplicate'),
    instructiontype(' \t ', 'Copy', numparam),
    instructiontype(' \n\t', 'Swap'),
    instructiontype(' \n\n', 'Discard'),
    instructiontype(' \t\n', 'Slide', numparam),
    
    # Arithmetic instructions ('\t ')
    instructiontype('\t   ', 'Add'),
    instructiontype('\t  \t', 'Subtract'),
    instructiontype('\t  \n', 'Multiply'),
    instructiontype('\t \t ', 'Divide'),
    instructiontype('\t \t\t', 'Modulo'),
    
    # Heap instructions ('\t\t')
    instructiontype('\t\t ', 'Store'),
    instructiontype('\t\t\t', 'Retrieve'),
    
    # Flow control instructions ('\n')
    instructiontype('\n  ', 'Label', stringparam),
    instructiontype('\n \t', 'Call', stringparam),
    instructiontype('\n \n', 'Jump', stringparam),
    instructiontype('\n\t ', 'JumpZero', stringparam),
    instructiontype('\n\t\t', 'JumpNegative', stringparam),
    instructiontype('\n\t\n', 'Return'),
    instructiontype('\n\n\n', 'End'),
    
    # IO instructions ('\t\n')
    instructiontype('\t\n  ', 'OutputChar'),
    instructiontype('\t\n \t', 'OutputNum'),
    instructiontype('\t\n\t ', 'ReadChar'),
    instructiontype('\t\n\t\t', 'ReadNum'),
    ]
