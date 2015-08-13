# BlueSpace
BlueSpace is the name of an interpreter for the Whitespace programming language.

## Whitespace
[Whitespace](https://en.wikipedia.org/wiki/Whitespace_%28programming_language%29) is an esoteric programming language that was created by Edwin Brady and Chris Morris and is based at http://compsoc.dur.ac.uk/whitespace/. Its syntax consists entirely of characters that are usually invisible when displayed by a computer: space, horizontal tab and line feed.

## BlueSpace
This interpreter is written in Python 3 and boasts the following features:
* Interpret Whitespace code
* Compile Whitespace code to Python and optionally execute it
  * Optimise the generated Python code
* Accept and translate between Whitespace syntax, as well as:
  * A printable syntax, which substitutes space, tab and linefeed with `s`, `t` and `n`, respectively
  * An assembly-style syntax (described below)

To run a Whitespace program, simply execute `./bspace.py source.ws`; to see other options, use `./bspace.py --help`.

## Assembly Syntax
Each line of the source must match one of the following forms, where *number* is any decimal integer and *label* is any string of `s` and `t` characters with an optional trailing `n`. Each line maps to a single Whitespace instruction. A `#` begins a comment; it and any subsequent characters on the same line are ignored.

<pre>
Push <i>number</i>
Duplicate
Copy <i>number</i>
Swap
Discard
Slide <i>number</i>

Add
Subtract
Multiply
Divide
Modulo

Store
Retrieve

Label <i>label</i>
Call <i>label</i>
Jump <i>label</i>
JumpZero <i>label</i>
JumpNegative <i>label</i>
Return
End

OutputChar
OutputNum
ReadChar
ReadNum
</pre>
