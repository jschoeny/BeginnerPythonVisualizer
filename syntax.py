# syntax.py

import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QColor


def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    if type(color) is QColor:
        _color = color
    else:
        _color = QColor()
        _color.setNamedColor(color)

    _format = QtGui.QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QtGui.QFont.Weight.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES_LIGHT = {
    'keyword': format(QColor(0, 51, 179)),
    'method': format(QColor(0, 0, 123)),
    'operator': format(QColor(8, 8, 8)),
    'brace': format(QColor(8, 8, 8)),
    'defclass': format(QColor(0, 98, 122), 'bold'),
    'string': format(QColor(6, 125, 23)),
    'string2': format(QColor(140, 140, 140)),
    'comment': format(QColor(140, 140, 140), 'italic'),
    'self': format(QColor(135, 16, 148), 'italic'),
    'numbers': format(QColor(23, 80, 235)),
}

STYLES_DARK = {
    'keyword': format(QColor(207, 142, 109)),
    'method': format(QColor(136, 136, 193)),
    'operator': format(QColor(188, 190, 196)),
    'brace': format(QColor(188, 190, 196)),
    'defclass': format(QColor(86, 168, 245)),
    'string': format(QColor(106, 171, 115)),
    'string2': format(QColor(95, 130, 107)),
    'comment': format(QColor(122, 126, 133), 'italic'),
    'self': format(QColor(199, 125, 187), 'italic'),
    'numbers': format(QColor(42, 172, 184)),
}


class PythonHighlighter(QtGui.QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    # Python built-in methods
    methods = [
        'print', 'super', 'len', 'input', 'open', 'range',
        'enumerate', 'int', 'str', 'float', 'list', 'tuple',
        'dict', 'set', 'bool', 'abs', 'all', 'any', 'ascii',
        'bin', 'bool', 'bytearray', 'bytes', 'callable',
        'chr', 'classmethod', 'compile', 'complex', 'delattr',
        'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec',
        'filter', 'float', 'format', 'frozenset', 'getattr',
        'globals', 'hasattr', 'hash', 'help', 'hex', 'id',
        'input', 'int', 'isinstance', 'issubclass', 'iter',
        'len', 'list', 'locals', 'map', 'max', 'memoryview',
        'min', 'next', 'object', 'oct', 'open', 'ord', 'pow',
        'print', 'property', 'range', 'repr', 'reversed',
        'round', 'set', 'setattr', 'slice', 'sorted',
        'staticmethod', 'str', 'sum', 'super', 'tuple',
        'type', 'vars', 'zip'
    ]

    # Python operators
    operators = [
        r'=',
        # Comparison
        r'==', r'!=', r'<', r'<=', r'>', r'>=',
        # Arithmetic
        r'\+', r'-', r'\*', r'/', r'//', r'\%', r'\*\*',
        # In-place
        r'\+=', r'-=', r'\*=', r'/=', r'\%=',
        # Bitwise
        r'\^', r'\|', r'\&', r'\~', r'>>', r'<<',
    ]

    # Python braces
    braces = [
        r'\{', r'\}', r'\(', r'\)', r'\[', r'\]',
    ]

    def __init__(self, parent: QtGui.QTextDocument, base_text_color: QColor) -> None:
        super().__init__(parent)
        self.style = STYLES_LIGHT
        if base_text_color.lightness() > 128:
            self.style = STYLES_DARK

        # Multi-line strings (expression, flag, style)
        self.tri_single = (QtCore.QRegularExpression("'''"), 1, self.style['string2'])
        self.tri_double = (QtCore.QRegularExpression('"""'), 2, self.style['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, self.style['keyword'])
                  for w in PythonHighlighter.keywords]
        rules += [(r'\b%s\(' % w, 0, self.style['method'])
                  for w in PythonHighlighter.methods]
        rules += [(r'%s' % o, 0, self.style['operator'])
                  for o in PythonHighlighter.operators]
        rules += [(r'%s' % b, 0, self.style['brace'])
                  for b in PythonHighlighter.braces]

        # All other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, self.style['self']),

            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, self.style['defclass']),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, self.style['defclass']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, self.style['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, self.style['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, self.style['numbers']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.style['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.style['string']),

            # From '#' until a newline
            (r'#[^\n]*', 0, self.style['comment']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QtCore.QRegularExpression(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text."""
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            iterator = expression.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                start = match.capturedStart(nth)
                length = match.capturedLength(nth)
                self.setFormat(start, length, format)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings."""
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            match = delimiter.match(text)
            if match.hasMatch():
                start = match.capturedStart()
                add = match.capturedLength()
            else:
                return False

        while start >= 0:
            match = delimiter.match(text, start + add)
            if match.hasMatch():
                end = match.capturedEnd()
                length = end - start + match.capturedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start
            self.setFormat(start, length, style)
            if match.hasMatch():
                start = match.capturedEnd()
            else:
                start = -1

        return self.currentBlockState() == in_state
