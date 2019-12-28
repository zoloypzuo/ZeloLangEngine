#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pprint import pprint

from PyMacroParser import *

# region test util
test_id = 0


def test_log(title=''):
    global test_id
    print('---- start test %s %s' % (test_id, title))
    test_id += 1


test_skip = 'test_data/lexer/skip.cpp'
test_define = 'test_data/define.cpp'
test_a = 'test_data/a.cpp'
# endregion

# region question base test


test_a1 = PyMacroParser()
test_a2 = PyMacroParser()
test_a1.load("test_data/a.cpp")
filename = "test_data/b.cpp"
test_a1.dump(filename)  # 没有预定义宏的情况下，dump cpp
test_a2.load(filename)
a2_dict = test_a2.dumpDict()
test_a1.preDefine("MC1;MC2")  # 指定预定义宏，再dump
a1_dict = test_a1.dumpDict()
test_a1.dump("test_data/c.cpp")

# 则b.cpp输出
test_b = '''
#define data1 1.0 //浮点精度信息消失，统一转成了double 正式输出没有这个注释
#define data2 2
#define data3 false
#define data4 "this is a data"
#define data5 68 //注意：这里本是'D' 转换后成为整型十进制表示，正式输出没有这个注释
#define data6 {1, 6}
#define MCTEST //空宏，但是被定义了, 正式输出没有这个注释
'''

# a2.dump字典
d2 = {
    "data1": 1.0,
    "data2": 2,
    "data3": False,
    "data4": "this is a data",
    "data5": 68,
    "data6": (1, 6),
    "MCTEST": None,  # 空宏，但被定义了。 正式输出没有这个注释
}

# a1.dump字典：
d1 = {
    "data1": 32,
    "data2": 2.5,  # 2.5f的float标记消失，正式输出没有这个注释
    "data3": u"this is a data",  # 宽字符串成为 unicode 正式输出没有这个注释
    "data4": True,
    "data5": 97,  # 注意 这里是'a'转int。 正式输出没有这个注释
    "data6": ((2.0, "abc"), (1.5, "def"), (5.6, "7.2")),  # python数据对象与源数据类型按规则对应即可， 正式输出没有这个注释
    "MC1": None,  # 预定义的空宏，而MC2最终被undef了，所以不存在MC2
    "MCTEST": None,
}

# c.cpp 输出
test_c = '''
#define data1 32 //16进制表示消失。 正式输出没有这个注释
#define data2 2.5
#define data3 L"this is a data" //unicode 转回宽字符 正式输出没有这个注释
#define data4 true
#define data5 97 //'a', 正式输出没有这个注释
#define data6 {{2.0, "abc"}, {1.5, "def"}, {5.6, "7.2"}} #tuple转回聚合， 正式输出没有这个注释
#define MC1
#define MCTEST
'''

assert a1_dict == d1
assert a2_dict == d2


# endregion

# region test lexer
def tl(s):
    test_log(s)
    lexer = Lexer(s)
    token_steam = TokenStream(lexer)
    while token_steam.not_eos:
        t = token_steam.next_token
        print(t)
        if t.kind == TokenKind.Eof:
            break


def tlf(f):
    test_log(f)
    lexer = Lexer(readall(f))
    token_steam = TokenStream(lexer)
    while token_steam.not_eos:
        t = token_steam.next_token
        print(t)
        if t.kind == TokenKind.Eof:
            break


print('==== test lexer start')
tlf(test_skip)
tlf(test_define)
print('==== test lexer end')


# endregion

# region test parser

def tp(s):
    test_log(s)
    pprint(parse(s), width=1)


def tpf(f):
    test_log(f)
    pprint(parse(readall(f), f), width=1)


print('==== test parser start')
tpf(test_a)

tp('')
tp('#undef a')
tp('#define a')
tp('#define a 1')
tpf(test_skip)
tpf(test_define)
print('test a')
tpf(test_a)
print('==== test parser end')


# endregion


def tv(s):
    test_log(s)
    return execute(Prototype(parse(s)))


def tvf(f):
    test_log(f)
    proto = Prototype(parse(readall(f), f))
    pprint(execute(proto))


tvf(test_a)
tvf(test_define)
tvf(test_skip)

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

tvf('test_data/test6.cpp')
tvf('test_data/branch.cpp')