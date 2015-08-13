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

from instructions import instructions
from parameters import numparam, stringparam

import sys

_numtr = str.maketrans('01', ' \t')
_stringtr = str.maketrans('st', ' \t')

_printtr = str.maketrans(' \t\n', 'stn')

def handleparam(paramtype, code, param):
    if paramtype == numparam:
        try:
            n = int(param)
        except ValueError:
            raise RuntimeError('BlueSpace: Parameter to ' + code + ' must be an integer')
        else:
            if n < 0:
                sign = '\t'
                n = -n
            else:
                sign = ' '
            return sign + format(n, 'b').translate(_numtr) + '\n'
    elif paramtype == stringparam:
        param = param.rstrip('n')
        if not all((x in 'st' for x in param)):
            raise RuntimeError('BlueSpace: Parameter to ' + code + ' must be a string of `st\'')
        else:
            return param.translate(_stringtr) + '\n'
    else:
        print('BlueSpace: Internal error, ' + code[0] + ' requires unknown parameter', file=sys.stderr)
        sys.exit(2)

mnemonicmap = {itype.name.lower(): itype for itype in instructions}

def parseline(line, printable):
    n = line.find('#')
    if n >= 0:
        line = line[0:n]
    code = line.split()
    if not code:
        return None
    
    try:
        itype = mnemonicmap[code[0].lower()]
    except KeyError:
        raise RuntimeError('BlueSpace: Invalid mnemonic, ' + code[0])
    
    if itype.paramtype is None:
        if len(code) > 1:
            raise RuntimeError('BlueSpace: Expected end of line before ' + code[1])
        if printable:
            return itype.rep.translate(_printtr) + '\n'
        else:
            return itype.rep
    else:
        if len(code) < 2:
            raise RuntimeError('BlueSpace: Parameter required for ' + code[0])
        temp = handleparam(itype.paramtype, code[0], code[1])
        if len(code) > 2:
            raise RuntimeError('BlueSpace: Expected end of line before ' + code[2])
        if printable:
            return itype.rep.translate(_printtr) + ' ' + temp.translate(_printtr) + '\n'
        else:
            return itype.rep + temp

def assemble(f, printable):
    stillgood = True
    result = []
    for line in f:
        try:
            ret = parseline(line, printable)
        except RuntimeError as err:
            print(err, file=sys.stderr)
            stillgood = False
        else:
            if ret is not None:
                result.append(ret)
    
    if not stillgood:
        raise RuntimeError
    
    return ''.join(result)
