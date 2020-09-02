# coding=utf-8
from functools import partial
from random import choice

from PyMacroParser import *
from test_util import *


def tl_(s, chunkname):
    lexer = Lexer(s, chunkname)
    token_steam = TokenStream(lexer)
    res = []
    while token_steam.not_eos:
        t = token_steam.next_token()
        res.append(t)
        if t.kind == TokenKind.Eof:
            break
    return tuple(res)


def tl(s):
    test_log(s)
    return tl_(s, s)


def tlf(f):
    test_log(f)
    return tl_(readall(f), f)


def test_lexeme(s, expected_kind):
    '''s包含一个token，测试这个token的kind和lexeme'''
    token = tl(s)[0]
    assert token.kind == expected_kind
    assert token.lexeme == s


WHITESPACE_CHAR_TUPLE = tuple(WHITESPACE_CHARSET)


def generate_whitespace_sequence(length):
    assert length > 0
    return ''.join(choice(WHITESPACE_CHAR_TUPLE) for _ in xrange(length))


test_lexeme_int = partial(test_lexeme, expected_kind=TokenKind.Int)
test_lexeme_float = partial(test_lexeme, expected_kind=TokenKind.Float)
test_lexeme_char = partial(test_lexeme, expected_kind=TokenKind.Char)
test_lexeme_string = partial(test_lexeme, expected_kind=TokenKind.String)
test_lexeme_wide_string = partial(test_lexeme, expected_kind=TokenKind.WideString)

log_style('==== test lexer start', bcolors.HEADER)
Lexer.OPTION_LEXEME_USE_SLICE = False

test_lexeme('', TokenKind.Eof)

# region skip comment and whitespaces
Lexer.OPTION_OUTPUT_SKIP_TOKEN = True
test_lexeme('// this is a comment', TokenKind.Skip_LineComment)
test_lexeme('/* this is a comment*/', TokenKind.Skip_BlockComment)
test_lexeme('''/* Comments can contain keywords such as
for and while without generating errors. */''', TokenKind.Skip_BlockComment)
test_lexeme('''/* MATHERR.C illustrates writing an error routine
* for math functions.
*/''', TokenKind.Skip_BlockComment)

for length in xrange(1, 3):
    for _ in xrange(3):
        test_lexeme(generate_whitespace_sequence(length), TokenKind.Skip_Whitespaces)

Lexer.OPTION_OUTPUT_SKIP_TOKEN = False
# endregion

test_lexeme('\n', TokenKind.Newline)  # unix
test_lexeme('\r\n', TokenKind.Newline)  # windows
test_lexeme('\r', TokenKind.Newline)  # windows

for k, v in KEYWORDS.items():
    test_lexeme(k, v)

for k, v in PUNCTUATORS.items():
    test_lexeme(k, v)

test_lexeme('abc', TokenKind.Identifier)
test_lexeme('_abc', TokenKind.Identifier)
test_lexeme('__', TokenKind.Identifier)

# NOTE 没有空字符，和字符串不同
test_lexeme_char("'0'")
test_lexeme_char("'c'")
test_lexeme_char("'\\n'")

test_lexeme_int('28')
test_lexeme_int('0x1C')
test_lexeme_int('034')
test_lexeme_int("0")
test_lexeme_int("-0")
test_lexeme_int("1")
test_lexeme_int("-1")
# Decimal Constants
test_lexeme_int('4000000024u')
test_lexeme_int('2000000022l')
test_lexeme_int('4000000000ul')
test_lexeme_int('9000000000LL')
test_lexeme_int('900000000001ull')

# Octal Constants
test_lexeme_int('024')
test_lexeme_int('04000000024u')
test_lexeme_int('02000000022l')
test_lexeme_int('04000000000UL')
test_lexeme_int('044000000000000ll')
test_lexeme_int('044400000000000001Ull')

# Hexadecimal Constants
test_lexeme_int('0x2a')
test_lexeme_int('0XA0000024u')
test_lexeme_int('0x20000022l')
test_lexeme_int('0XA0000021uL')
test_lexeme_int('0x8a000000000000ll')
test_lexeme_int('0x8A40000000000010uLL')

test_lexeme_float("-0.0")  # BUG 0可能是float或者oct
test_lexeme_float("1.5")
test_lexeme_float("-1.5")
test_lexeme_float("3.1416")
test_lexeme_float("1E10")
test_lexeme_float("1e10")
test_lexeme_float("1E+10")
test_lexeme_float("1E-10")
test_lexeme_float("-1E10")
test_lexeme_float("-1e10")
test_lexeme_float("-1E+10")
test_lexeme_float("-1E-10")
test_lexeme_float("1.234E+10")
test_lexeme_float("1.234E-10")
test_lexeme_float("1e-10000")  # must underflow */

test_lexeme_float("1.0000000000000002")  # the smallest number > 1 */
test_lexeme_float("4.9406564584124654e-324")  # minimum denormal */
test_lexeme_float("-4.9406564584124654e-324")
test_lexeme_float("2.2250738585072009e-308")  # Max subnormal double */
test_lexeme_float("-2.2250738585072009e-308")
test_lexeme_float("2.2250738585072014e-308")  # Min normal positive double */
test_lexeme_float("-2.2250738585072014e-308")
test_lexeme_float("1.7976931348623157e+308")  # Max double */
test_lexeme_float("-1.7976931348623157e+308")

test_lexeme_float('0.0')
test_lexeme_float('0.0f')
test_lexeme_float('.0f')

test_lexeme_string("\"\"")
test_lexeme_string("\"Hello\"")
test_lexeme_string("\"Hello\\nWorld\"")
test_lexeme_string("\"\\\" \\\\ \\/ \\b \\f \\n \\r \\t\"")

test_lexeme_wide_string("L\"\"")
test_lexeme_wide_string("L\"Hello\"")
test_lexeme_wide_string("L\"Hello\\nWorld\"")
test_lexeme_wide_string("L\"\\\" \\\\ \\/ \\b \\f \\n \\r \\t\"")

# POPO群里的，比较复杂的测试
tlf('../test_data/test6.cpp')
tlf('../test_data/test7.cpp')

# 《C程序语言现代方法》
test_lexeme_int('15')
test_lexeme_int('255')
test_lexeme_int('32767')
test_lexeme_int('017')
test_lexeme_int('0377')
test_lexeme_int('07777')
test_lexeme_int('0xf')
test_lexeme_int('0x7fff')
test_lexeme_int('15L')
test_lexeme_int('0377L')
test_lexeme_int('0x7fffL')
test_lexeme_int('15U')
test_lexeme_int('0377U')
test_lexeme_int('0x7fffU')
test_lexeme_int('0xffffUL')

test_lexeme_float('57.0')
test_lexeme_float('57.')
test_lexeme_float('57.0e0')
test_lexeme_float('57E0')
test_lexeme_float('5.7e1')
test_lexeme_float('5.7e+1')
test_lexeme_float('.57e2')
test_lexeme_float('570.e-1')
test_lexeme_float('570.e-1f')
test_lexeme_float('570.e-1L')

test_lexeme_char("'a'")
test_lexeme_char("'A'")
test_lexeme_char("'0'")
test_lexeme_char("' '")
test_lexeme_char(r"'\a'")
test_lexeme_char(r"'\033'")
test_lexeme_char(r"'\33'")
test_lexeme_char(r"'\x1b'")
test_lexeme_char(r"'\x1B'")

test_lexeme_string('"when go shit"')
test_lexeme_string(r'"when go shit\nwhen go shit\n"')
test_lexeme_string(r'"when go shit\1234when go shit\189"')

Lexer.OPTION_LEXEME_USE_SLICE = True

log_style('==== test lexer end', bcolors.HEADER)
