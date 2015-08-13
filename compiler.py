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

_arithmap = {
    '\t   ': '+',
    '\t  \t': '-',
    '\t  \n': '*',
    '\t \t ': '//',
    '\t \t\t': '%',
    }

def _getcode(stmt):
    rep = stmt.rep
    
    if rep == '  ': # Push
        return '    stack.append(' + str(stmt.param) + ')',
    elif rep == ' \n ': # Duplicate
        return '    stack.append(stack[-1])',
    elif rep == ' \t ': # Copy
        return '    stack.append(stack[-' + str(stmt.param.value + 1) + '])',
    elif rep == ' \n\t': # Swap
        return '    stack[-1], stack[-2] = stack[-2], stack[-1]',
    elif rep == ' \n\n': # Discard
        return '    stack.pop()',
    elif rep == ' \t\n': # Slide
        return '    del stack[-' + str(stmt.param.value + 1) + ':-1]',
    elif rep.startswith('\t '): # Arithmetic
        return ('    x = stack.pop()',
                '    stack[-1] ' + _arithmap[rep] + '= x')
    elif rep == '\t\t ': # Store
        return ('    x = stack.pop()',
                '    heap[stack.pop()] = x')
    elif rep == '\t\t\t': # Retrieve
        return '    stack[-1] = heap[stack[-1]]',
    elif rep == '\n \t': # Call
        return '    run(' + str(stmt.param) + ')',
    elif rep == '\n\t ': # JumpZero
        return ('    if stack.pop() == 0:',
                '        return ' + str(stmt.param))
    elif rep == '\n\t\t': # JumpNegative
        return ('    if stack.pop() < 0:',
                '        return ' + str(stmt.param))
    elif rep == '\t\n  ': # OutputChar
        return '    sys.stdout.write(chr(stack.pop()))',
    elif rep == '\t\n \t': # OutputNum
        return '    sys.stdout.write(str(stack.pop()))',
    elif rep == '\t\n\t ': # ReadChar
        return ('    sys.stdout.flush()',
                '    try:',
                '        x = ord(sys.stdin.read(1))',
                '    except EOFError:',
                '        x = -1',
                '    heap[stack.pop()] = x')
    elif rep == '\t\n\t\t': # ReadNum
        return ('    sys.stdout.flush()',
                '    s = sys.stdin.readline()',
                '    heap[stack.pop()] = int(s)')

def topython(program):
    result = [
        '#!/usr/bin/env python3',
        'import sys',
        'stack = []',
        'heap = {}',
        'def run(f):',
        '    while f is not None:',
        '        f = f()',
        'def start():',
        ]
    
    reachable = True
    for stmt in program:
        rep = stmt.rep
        
        if rep == '\n  ': # Label
            if reachable:
                result.append('    return ' + str(stmt.param))
            result.append('def ' + str(stmt.param) + '():')
            reachable = True
        elif rep == '\n \n': # Jump
            result.append('    return ' + str(stmt.param))
            reachable = False
        elif rep == '\n\t\n': # Return
            result.append('    return')
            reachable = False
        elif rep == '\n\n\n': # End
            result.append('    sys.exit()')
            reachable = False
        else:
            result.extend(_getcode(stmt))
    
    if reachable:
        result.append('    raise IndexError')
    result.extend((
        'run(start)',
        'raise IndexError',
        ))
    
    return '\n'.join(result)
