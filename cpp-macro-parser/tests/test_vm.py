# coding=utf-8
from PyMacroParser import *
from test_util import *

log_style('==== test vm start', bcolors.HEADER)


def tv_(s, chunkname):
    return execute(Prototype(parse(s, chunkname)))


def tv(s):
    test_log(s)
    return tv_(s, s)


def tvf(f):
    test_log(f)
    return tv_(readall(f), f)



tv('/*asd*/#/*ded*/define/*ad*/\tcharc\t\'a\'')
tv('/*asd*/#/*ded*/define/*ad*/\tcharc\t\'\123\'')
tv('/*asd*/#/*ded*/define/*ad*/\ta\t1.5e6')
tv('#define a {1,2,3,4}')
tv('#define a {80,{90}}')


def tvl(literal, expected):
    actual = tv('#define a %s' % literal)['a']
    assert actual == expected, 'expect %s, get %s' % (expected, actual)


tvl('true', True)
tvl('false', False)


def TEST_NUMBER(expected, literal):
    tvl(literal, expected)


TEST_NUMBER(0.0, "0")
TEST_NUMBER(0.0, "-0")
TEST_NUMBER(0.0, "-0.0")  # BUG 0可能是float或者oct
TEST_NUMBER(1.0, "1")
TEST_NUMBER(-1.0, "-1")
TEST_NUMBER(1.5, "1.5")
TEST_NUMBER(-1.5, "-1.5")
TEST_NUMBER(3.1416, "3.1416")
TEST_NUMBER(1E10, "1E10")
TEST_NUMBER(1e10, "1e10")
TEST_NUMBER(1E+10, "1E+10")
TEST_NUMBER(1E-10, "1E-10")
TEST_NUMBER(-1E10, "-1E10")
TEST_NUMBER(-1e10, "-1e10")
TEST_NUMBER(-1E+10, "-1E+10")
TEST_NUMBER(-1E-10, "-1E-10")
TEST_NUMBER(1.234E+10, "1.234E+10")
TEST_NUMBER(1.234E-10, "1.234E-10")
TEST_NUMBER(0.0, "1e-10000")  # must underflow */

TEST_NUMBER(1.0000000000000002, "1.0000000000000002")  # the smallest number > 1 */
TEST_NUMBER(4.9406564584124654e-324, "4.9406564584124654e-324")  # minimum denormal */
TEST_NUMBER(-4.9406564584124654e-324, "-4.9406564584124654e-324")
TEST_NUMBER(2.2250738585072009e-308, "2.2250738585072009e-308")  # Max subnormal double */
TEST_NUMBER(-2.2250738585072009e-308, "-2.2250738585072009e-308")
TEST_NUMBER(2.2250738585072014e-308, "2.2250738585072014e-308")  # Min normal positive double */
TEST_NUMBER(-2.2250738585072014e-308, "-2.2250738585072014e-308")
TEST_NUMBER(1.7976931348623157e+308, "1.7976931348623157e+308")  # Max double */
TEST_NUMBER(-1.7976931348623157e+308, "-1.7976931348623157e+308")


def TEST_STRING(expect, literal):
    tvl(literal, expect)


TEST_STRING("", "\"\"")
TEST_STRING("Hello", "\"Hello\"")
TEST_STRING("Hello\nWorld", "\"Hello\\nWorld\"")
TEST_STRING("\" \\ / \b \f \n \r \t", "\"\\\" \\\\ \\/ \\b \\f \\n \\r \\t\"")
# TEST_STRING("Hello\0World", "\"Hello\\u0000World\"")
# TEST_STRING("\x24", "\"\\u0024\"")  # Dollar sign U+0024 */
# TEST_STRING("\xC2\xA2", "\"\\u00A2\"")  # Cents sign U+00A2 */
# TEST_STRING("\xE2\x82\xAC", "\"\\u20AC\"")  # Euro sign U+20AC */
# TEST_STRING("\xF0\x9D\x84\x9E", "\"\\uD834\\uDD1E\"")  # G clef sign U+1D11E */
# TEST_STRING("\xF0\x9D\x84\x9E", "\"\\ud834\\udd1e\"")  # G clef sign U+1D11E */

tvl('{}', tuple())
tvl('{1}', (1,))
tvl('{1,2}', (1, 2))
tvl('{1,2,}', (1, 2))  # [x] BUG fixed
tvl('{1,\'c\'}', (1, ord('c')))

tvl('28', 28)
tvl('0x1C', 28)
tvl('034', 28)

# Decimal Constants */
tvl('4000000024u', 4000000024)
tvl('2000000022l', 2000000022)
tvl('4000000000ul', 4000000000)
tvl('9000000000LL', 9000000000)
tvl('900000000001ull', 900000000001)

# Octal Constants */
# tvl('024'
# tvl('04000000024u'
# tvl('02000000022l'
# tvl('04000000000UL'
# tvl('044000000000000ll'
# tvl('044400000000000001Ull'

# Hexadecimal Constants */
# tvl('0x2a'
# tvl('0XA0000024u'
# tvl('0x20000022l'
# tvl('0XA0000021uL'
# tvl('0x8a000000000000ll'
# tvl('0x8A40000000000010uLL'

tvl('{{2.0, "abc"}, {1.5, "def",}, {5.6, "7.2",},}', ((2.0, "abc"), (1.5, "def"), (5.6, "7.2")))

tvf('../test_data/test6.cpp')
tvf('../test_data/branch.cpp')
tv(r'# define a "\v\'\"\f \"\n\r\t\b\a\\"')
tvf('../test_data/test7.cpp')

print tv('#define COMPDATA  { {{1,3}, {2,3,5}, {31}},  {{12,016}, {1,30,0}}, 23 } ')

log_style('==== test vm end', bcolors.HEADER)
