# BlueSpace
BlueSpace is an interpreter for the Whitespace programming language.

## Whitespace
[Whitespace](https://en.wikipedia.org/wiki/Whitespace_%28programming_language%29) is an esoteric programming language that was created by Edwin Brady and Chris Morris and is based at http://compsoc.dur.ac.uk/whitespace/ ([archived version from 2015-07-15](https://web.archive.org/web/20150717190859/http://compsoc.dur.ac.uk/whitespace/)). Its syntax consists entirely of invisible characters: space, tab and line feed.

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

## Compatibility
Known incompatibilities between BlueSpace 1.1 and WSpace 0.3:
* The ReadNumber instruction (tab-linefeed-tab-tab): WSpace accepts spaces between the negative sign and the number (e.g. `- 123` is accepted as equivalent to `-123`) which BlueSpace does not. Conversely, BlueSpace accepts a leading plus. (e.g. `+12` is equivalent to `12`) which is rejected by WSpace.
* WSpace ignores all trailling characters after the last point in the code that is visited; BlueSpace requires the entire input to be a valid Whitespace program. For example, the program consisting of four linefeeds is the null program according to WSpace, but BlueSpace reports a syntax error since the fourth linefeed does not constitute a valid command. This is due to WSpace's lazy parsing semantics.
* If a program defines the same label more than once, WSpace jumps to the first instance, while BlueSpace jumps to the last. I consider such a program to be erroneous and later versions of BlueSpace may report this as such.

## Programs
Here is some code I've written in Whitespace.
* Here's the classic [99 Bottles of Beer program](./99.wsp). It's encoded in the printable syntax, so it must be run with `./bspace.py -iprintable`. (I nearly always write code in the printable syntax, as it is much easier to read.)
* <s>Here's my [shortest quine](./quine-cs.ws) to date, weighing in at a mere 486 bytes. While we're at it, here's the [disassembly](./quine-cs.wsa) (although, of course, it is not a quine in this form).</s>
* The above has been improved to 406 bytes. Here's the [Whitespace](./quine-cs-3.ws) and the [disassembly](./quine-cs-3.wsa).

## Name
Why BlueSpace? It is, in fact, named after [Sir Lancelot's favourite colour](http://en.wikiquote.org/wiki/Monty_Python_and_the_Holy_Grail); anyone who is familiar with the Python documentation should be sufficiently conditioned to expect such silliness.

## More
I have another page about Whitespace and BlueSpace which includes some of my own Whitespace programs at http://cpjsmith.co.uk/whitespace
