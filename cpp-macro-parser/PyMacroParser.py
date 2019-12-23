#!/usr/bin/python
# -*- coding: UTF-8 -*-

# region 简易沙箱，你不应该再import任何东西了

# blacklist = ['re']
# for mod in blacklist:
#     i = __import__(mod)
#     sys.modules[mod] = None
# eval = None
# exec = None
# copy = None
# deepcopy = None

from collections import namedtuple
from enum import Enum, auto
from pprint import pprint


# endregion

# region common


def readall(path):
    with open(path, 'r', encoding='utf8') as f:
        return f.read()


def writeall(path, text):
    with open(path, 'w') as f:
        f.write(text)


# endregion

# noinspection PyPep8Naming,PyShadowingNames
class PyMacroParser:
    def load(self, f):
        pass

    def dump(self, filename):
        pass

    def dumpDict(self):
        pass

    def preDefine(self, s):
        pass


# region lexer

class TokenKind(Enum):
    Eof = auto()
    Newline = auto()
    Identifier = auto()
    Int = auto()
    Float = auto()
    Char = auto()
    String = auto()
    Sep_Pound = auto()  # '#'，百度说井字叫pound
    Sep_LCurly = auto()  # {
    Sep_RCurly = auto()  # }
    Sep_Comma = auto()  # ,
    Kw_IfDef = auto()  # ifdef
    Kw_IfNDef = auto()  # ifndef
    Kw_Define = auto()  # define
    Kw_UnDef = auto()  # undef
    Kw_Else = auto()  # else
    Kw_EndIf = auto()  # endif
    Kw_True = auto()  # true
    Kw_False = auto()  # false


keywords = {
    'ifdef': TokenKind.Kw_IfDef,
    'ifndef': TokenKind.Kw_IfNDef,
    'define': TokenKind.Kw_Define,
    'undef': TokenKind.Kw_UnDef,
    'else': TokenKind.Kw_Else,
    'endif': TokenKind.Kw_EndIf,
    'true': TokenKind.Kw_True,
    'false': TokenKind.Kw_False
}


class NumberType(Enum):
    Decimal = auto()
    Octal = auto()
    Hexadecimal = auto()
    Float = auto()


class LexerException(Exception):
    pass


# str确实有一些帮助判断的函数，但是建议自己写
def is_whitespace(c):
    return c in set(' \t\v\f')  # 这种写法会导致每次构造一个set，建议提取变量


def is_digit(c):
    return '0' <= c <= '9'


def is_letter(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z'


def is_newline(c):
    return c == '\n' or c == '\r'


def is_identifier_char(c):
    return c == '_' or is_digit(c) or is_letter(c)


def is_hex_digit(c):
    return '0' <= c <= '9' or 'A' <= c <= "F" or 'a' <= c <= 'f'


class Token:
    def __init__(self, pos, kind, value):
        self.pos: tuple = pos
        self.kind: TokenKind = kind
        self.value = value

    def __str__(self):
        return (self.pos, self.kind, self.value).__str__()

    __repr__ = __str__


# noinspection PyPropertyDefinition
class ILexer:
    @property
    def eof(self):
        pass

    @property
    def not_eof(self):
        pass

    @property
    def next_token(self) -> Token:
        pass


# 包装Lexer为一个带前瞻的流对象
#
# 词法分析认为是复杂计算，因此前瞻时缓存结果
# 内部维护一个List<Token>包含所有已经计算的Token值，不删除旧的值，所有Token都会一直在内存
# NextToken对应于流的指针，而LookAhead(n)的n是相对于流指针的偏移
# LookAhead有单个元素和数组两个版本，因为我暂时不知道parser是否要用哪种，干脆都写
# NextToken和LookAhead在未计算所需Token时计算并缓存Token，从缓存中取出Token
class ITokenStream:
    @property
    def eos(self) -> bool:
        pass

    @property
    def not_eos(self) -> bool:
        pass

    # 前瞻，不前进流指针
    def lookahead(self, n=1) -> Token:
        pass

    # def lookahead_array(self, n) -> tuple:
    #     pass

    # 返回下一个token，前进一格流指针
    @property
    def next_token(self) -> Token:
        pass

    @property
    def pos(self) -> tuple:
        pass


class TokenStream(ITokenStream):
    def __init__(self, lexer: ILexer):
        self.buffer = []
        # NOTE 注意指针初始值为-1，总是指向第一个可用的token前一格
        # 这样比如初始时lookahead(1)返回buffer[0]
        self.pointer = -1
        self.lexer = lexer

    @property
    def eos(self):
        return self.lexer.eof and self.pointer >= len(self.buffer)

    @property
    def not_eos(self):
        return not self.eos

    # 前瞻，不前进流指针
    def lookahead(self, n=1):
        self.cache_if_need(n)
        return self.buffer[self.pointer + n]

    def lookahead_array(self, n):
        self.cache_if_need(n)
        p = self.pointer
        return tuple(self.buffer[p:p + n])

    # 返回下一个token，前进一格流指针
    @property
    def next_token(self):
        self.cache_if_need(1)
        self.pointer += 1
        return self.buffer[self.pointer]

    def cache_if_need(self, n):
        _len = len(self.buffer)
        p = self.pointer

        # 初始值 0 <= -1 + 1
        if _len <= p + n:
            # 初始值 1 = -1+1-0+1
            n_to_cache = p + n - _len + 1
            i = 0
            while i < n_to_cache:
                t = self.lexer.next_token
                # if self.lexer.eof():
                #     # TODO 这个异常可以捕获，再想想；parser自己check eof token，而不是捕获异常
                #     # 比如 print(1缺一个右括号，parser调用lexer会走到这里
                #     raise LexerException('no more tokens')
                self.buffer.append(t)
                i += 1

    @property
    def pos(self) -> tuple:
        return self.buffer[self.pointer + 1].pos


class Lexer(ILexer):
    def __init__(self, chunk: str):
        self.chunk = chunk  # source code
        self.line = 1  # current line number
        self.column = 1
        self.last_column = 1  # 构造Token时指针已经移动到lexeme末尾了，所以要延迟一下
        self.pointer = 0

    @property
    def next_token(self) -> Token:

        def skip():
            while self.not_eof:
                if self.test_prefix('//'):
                    self.advance(2)
                    while self.not_eof and not is_newline(self.char):
                        self.advance(1)
                elif self.test_prefix('/*'):
                    self.advance(2)
                    while not self.test_prefix('*/'):
                        # 注释会包含换行
                        # 另一种方法是解析出来，然后数一下有多少换行
                        if not self.newline():
                            self.advance(1)
                    else:  # while else
                        self.advance(2)
                # elif self.test('\r\n') || self.test('\n\r'):
                #     self.next(2)
                #     self.line+=1
                elif is_whitespace(self.char):
                    self.advance(1)
                else:
                    break

        # 返回token
        # value尽早在lexer就解析出值，字符串的转义也处理好
        def res_token(kind: TokenKind, value=None):
            column = self.last_column
            self.last_column = self.column
            return Token((self.line, column), kind, value)

        skip()
        # 被跳过的内容不输出token，但是column要更新
        self.last_column = self.column
        if self.eof:
            return res_token(TokenKind.Eof)

        '''
接下来的大switch
有的token靠第一个字符就能区别出来，很简单

第二简单的是比如<和<=
例子：
case ':':
    if self.test("::") {
        self.next(2)
        return self.line, TOKEN_SEP_LABEL, "::"
    } else {
        self.next(1)
        return self.line, TOKEN_SEP_COLON, ":"
    }

比较难的是.
.在编程语言中一般用于访问成员，但是，浮点数可以直接用点开头
这需要判断是否是数字，然后把数字解析扔到default里去解析        
        '''

        c = self.char

        if c == '#':
            self.advance(1)
            return res_token(TokenKind.Sep_Pound)
        elif c == '{':
            self.advance(1)
            return res_token(TokenKind.Sep_LCurly)
        elif c == '}':
            self.advance(1)
            return res_token(TokenKind.Sep_RCurly)
        elif c == ',':
            self.advance(1)
            return res_token(TokenKind.Sep_Comma)
        elif c == '\'':
            self.advance(1)
            # TODO 没有宽字符，但是转义没有处理
            if self.eof:
                self.error("unfinished char")
            c = self.char
            self.advance(1)
            if self.eof or self.char != '\'':
                self.error("unfinished char")
            else:
                self.advance(1)
                return res_token(TokenKind.Char, c)
        elif c == '\"':
            s = self.scan_string()
            return res_token(TokenKind.String, s)
        else:
            if self.newline():
                return res_token(TokenKind.Newline)
            if self.test_prefix('L\"'):
                self.advance(1)
                # TODO 宽字符串如何处理
                s = self.scan_string()
                return res_token(TokenKind.String, s)
            if c == '.' or is_digit(c):
                t, v = self.scan_number()
                if t == NumberType.Decimal or t == NumberType.Hexadecimal or t == NumberType.Octal:
                    return res_token(TokenKind.Int, v)
                elif t == NumberType.Float:
                    return res_token(TokenKind.Float, v)
                else:
                    self.error("unreachable")
            if c == '_' or is_letter(c):
                identifier = self.scan_identifier()
                assert identifier.isidentifier()
                # 关键字是这样处理的：先用id来lex，然后优先判定关键字
                res = keywords.get(identifier)
                if res:
                    return res_token(res)
                else:
                    return res_token(TokenKind.Identifier, identifier)
        self.error("unexpected symbol near %s" % c)

    # 返回是否吃进换行符，如果是，更新行号和列号
    # 返回False的情况下，newline对当前字符什么都不做，交给调用者处理
    def newline(self):
        if self.test_prefix('\r\n') or self.test_prefix('\n\r'):
            self.advance(2)
            self.line += 1
            self.column = 0
            return True
        elif is_newline(self.char):
            self.advance(1)
            self.line += 1
            self.column = 0
            return True
        else:
            return False

    # 如果eof，你不应该索引chunk了
    @property
    def eof(self):
        return self.pointer >= len(self.chunk)

    @property
    def not_eof(self):
        return self.pointer < len(self.chunk)

    # test类函数会检查eof，如果因为遇到eof而失败，也是返回false
    # 下面的test类函数不必调用test-base，避免小调用，但是应该参考这个
    def test_base(self, predicate):
        return self.not_eof and predicate()

    # test是test类函数
    def try_advance_base(self, test, n):
        res = test()
        if res:
            self.advance(n)
        return res

    def test_char_is(self, c):
        return self.not_eof and self.char == c

    # 测试chunk接下来是否是s，类似于re.match
    def test_prefix(self, s: str):
        return self.chunk.startswith(s, self.pointer)

    def test_char_in_charset(self, charset):
        return self.not_eof and self.char in charset

    def test_char_predicate(self, predicate):
        return self.not_eof and predicate(self.char)

    def test_char_is_digit(self):
        return self.not_eof and is_digit(self.char)

    def try_advance_char_is(self, c):
        return self.try_advance_base(lambda: self.test_char_is(c), 1)

    def try_advance_prefix(self, s: str):
        return self.try_advance_base(lambda: self.test_prefix(s), len(s))

    # 自己决定charset是str还是set
    def try_advance_char_in_charset(self, charset):
        return self.try_advance_base(lambda: self.test_char_in_charset(charset), 1)

    # 指针前进
    # 不要叫next，避免和python-generator的next冲突
    def advance(self, n: int):
        self.column += n
        self.pointer += n

    def error(self, msg: str):
        raise LexerException(self.line, self.column, msg)

    @property
    def char(self):
        return self.chunk[self.pointer]

    # Identifier :  [a-zA-Z_][a-zA-Z_0-9]*;
    def scan_identifier(self):
        pointer = self.pointer
        self.advance(1)  # first char is checked
        while self.not_eof and is_identifier_char(self.char):
            self.advance(1)
        return self.chunk[pointer:self.pointer]

    # HARD 想想办法逃课把。。。
    # 首字母无法判断是int还是float
    # 返回Token
    def scan_number(self):
        pointer = self.pointer

        def lexeme():
            return self.chunk[pointer: self.pointer]

        def res_float():
            return NumberType.Float, float(lexeme())

        # 转为python都是int，所以后缀信息没用
        # 而且实测int函数不能解析后缀，所以要先解析再advance
        def abandon_int_suffix():
            self.try_advance_prefix('ll')
            self.try_advance_prefix('LL')
            self.try_advance_char_in_charset('lLuU')

        def abandon_float_suffix():
            self.try_advance_char_in_charset('fF')

        # 可以看到，手工人肉lex浮点数的ifelse复杂度已经超出了控制
        # 必须抽象可靠的模式，否则无法做错误处理
        # 写多了就发现模式了，而且这个和parser是一致的
        # 一个语法成分，要返回是否有这个成分，给调用者断言
        # 然后要处理内部发生的错误
        # 这个显然可以进一步抽象，从语法生成代码

        # exponent-part:
        #     e signopt digit-sequence
        #     E signopt digit-sequence
        def exponent_part():
            res = self.try_advance_char_in_charset('eE')
            if res:
                self.try_advance_char_in_charset('+-')
                if not digit_sequence():
                    self.error('float miss digit-sequence')
            return res

        # digit-sequence:
        #     digit
        #     digit-sequence digit
        def digit_sequence():
            res = self.test_char_is_digit()
            while self.try_advance_base(self.test_char_is_digit, 1):
                pass
            return res

        c = self.char
        self.advance(1)
        if self.try_advance_char_is('.'):  # float
            # . digit-sequence exponent-part? float-suffix?
            if not digit_sequence():
                self.error('float miss digit-sequence')
            exponent_part()
            res = res_float()
            abandon_float_suffix()
            return res
        elif c == '0':  # oct or hex
            if self.try_advance_char_in_charset('xX'):  # hex
                # hexadecimal-constant:
                #     hexadecimal-prefix hexadecimal-digit
                #     hexadecimal-constant hexadecimal-digit
                if not self.test_char_predicate(is_hex_digit):
                    self.error("unfinished hex int")
                while self.test_char_predicate(is_hex_digit):
                    self.advance(1)
                value = int(lexeme(), 16)
                abandon_int_suffix()
                return NumberType.Hexadecimal, value
            else:  # oct
                # octal-constant:
                #     0
                #     octal-constant octal-digit
                while self.not_eof and '0' <= self.char <= '7':
                    self.advance(1)
                value = int(lexeme(), 8)
                abandon_int_suffix()
                return NumberType.Octal, value
        else:  # int or float
            assert '1' <= c <= '9'
            # 不管是int还是float，首先解析出整数
            digit_sequence()
            if self.test_char_in_charset('.eE'):  # float
                # floating-point-constant:
                #     fractional-constant exponent-part? floating-suffix?
                #     digit-sequence exponent-part floating-suffix?
                #
                # fractional-constant:
                #     digit-sequence? . digit-sequence  # ?的情况上面处理过了
                #     digit-sequence .
                if self.try_advance_char_is('.'):
                    digit_sequence()
                    exponent_part()
                    res = res_float()
                    abandon_float_suffix()
                    return res
                else:
                    assert self.test_char_in_charset('eE')
                    if not exponent_part():
                        self.error('float miss exponent-part')
                    res = res_float()
                    abandon_float_suffix()
                    return res
            else:  # int
                value = int(lexeme())
                abandon_int_suffix()
                return NumberType.Decimal, value

    # 扫描，完成转移，返回没有两端引号的文本内容
    def scan_string(self):
        self.advance(1)  # first char is checked
        string_builder = []  # 没有找到StringBuilder
        while self.not_eof and self.char != '\"':
            c = self.char
            self.advance(1)
            # 处理转义
            if c != '\\':
                string_builder.append(c)
                continue
            if self.eof:
                self.error("unfinished string")
            c = self.char
            self.advance(1)
            if c == 'a':
                string_builder.append('\a')
                continue
            elif c == 'b':
                string_builder.append('\b')
                continue
            elif c == 'f':
                string_builder.append('\f')
                continue
            elif c == 'n':
                string_builder.append('\n')
                continue
            elif c == 'r':
                string_builder.append('\r')
                continue
            elif c == 't':
                string_builder.append('\t')
                continue
            elif c == 'v':
                string_builder.append('\v')
                continue
            elif c == '"':
                string_builder.append('"')
                continue
            elif c == '\'':
                string_builder.append('\'')
                continue
            elif c == '\\':
                string_builder.append('\\')
                continue
            comment = '''
    case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9': // \ddd
        if found := reDecEscapeSeq.FindString(str); found != "" {
            d, _ := strconv.ParseInt(found[1:], 10, 32)
            if d <= 0xFF {
                buf.WriteByte(byte(d))
                str = str[len(found):]
                continue
            }
            self.error("decimal escape too large near '%s'", found)
        }
    case 'x': // \\xXX
        if found := reHexEscapeSeq.FindString(str); found != "" {
            d, _ := strconv.ParseInt(found[2:], 16, 32)
            buf.WriteByte(byte(d))
            str = str[len(found):]
            continue
        }
    case 'u': // \\u{XXX}
        if found := reUnicodeEscapeSeq.FindString(str); found != "" {
            d, err := strconv.ParseInt(found[3:len(found)-1], 16, 32)
            if err == nil && d <= 0x10FFFF {
                buf.WriteRune(rune(d))
                str = str[len(found):]
                continue
            }
            self.error("UTF-8 value too large near '%s'", found)
        }                                
                    '''
            self.error("invalid escape sequence near '\\%s'" % c)
        if self.eof or self.char != '\"':
            self.error("unfinished string")
        else:
            self.advance(1)  # read the quote
            return ''.join(string_builder)


# endregion

# region parser

class Prototype:
    pass


class ParserException(Exception):
    pass


def compile(chunk: str, chunkname='') -> Prototype:
    # TODO catch error and rethrow with chunk name
    pass


block_ctx = namedtuple('block_ctx', ['stat_star'])
define_stat_ctx = namedtuple('define_stat_ctx', ['identifier', 'token_string_optional'])
undef_stat_ctx = namedtuple('undef_stat_ctx', ['identifier'])
bool_exp_ctx = namedtuple('bool_exp_ctx', ['value'])
char_exp_ctx = namedtuple('char_exp_ctx', ['value'])
int_exp_ctx = namedtuple('int_exp_ctx', ['value'])
float_exp_ctx = namedtuple('float_exp_ctx', ['value'])
# 这里不想细分了，直接加个bool区别，还没有想清楚L怎么处理
string_exp_ctx = namedtuple('string_exp_ctx', ['is_long_str', 'value'])
aggregate_exp_ctx = namedtuple('aggregate_exp_ctx', ['fieldlist_optional'])
fieldlist_optional_ctx = namedtuple('fieldlist_optional_ctx', ['token_string_star'])
conditional_stat_ctx = namedtuple('conditional_stat_ctx',
                                  ['if_part', 'else_part_optional'])
if_part_ctx = namedtuple('if_part_ctx', ['if_line', 'block'])
else_part_optional_ctx = namedtuple('else_part_optional_ctx', ['block'])
ifdef_ctx = namedtuple('ifdef_ctx', ['identifier'])
ifndef_ctx = namedtuple('ifndef_ctx', ['identifier'])


# 返回AST，我们使用lisp
# TODO lookahead(k)
def parse(chunk) -> tuple:
    token_steam: ITokenStream = TokenStream(Lexer(chunk))

    def error(msg):
        raise ParserException(msg)

    def test_lookahead_kind(kind: TokenKind, n=1):
        return lookahead(n).kind == kind

    def next_token():
        return token_steam.next_token

    def lookahead(n=1):
        return token_steam.lookahead(n)

    # assert grammar function
    # 每个语法成分对应一个函数
    # 函数返回一个bool和ast
    # bool代表是否有这个语法成分，交给调用者用于判断
    # def assert_has_NT(g_function):
    #     b, ast = g_function()
    #     if not b:
    #         error("miss %s" % g_function.__name__)
    #     else:
    #         return ast

    def assert_lookahead_kind(kind):
        t = lookahead()
        if kind != t.kind:
            error("expect Token %s, get actual %s" % (kind, t.kind))
        return t

    def assert_lookahead_kind_and_read(kind):
        t = lookahead()
        if kind != t.kind:
            error("expect Token %s, get actual %s" % (kind, t.kind))
        else:
            next_token()
            return t

    def test_kind_and_read(kind):
        t = lookahead()
        return t.kind == kind

    def test_lookahead_kind_in(kind_set: set):
        return lookahead().kind in kind_set

    def test_lookahead_kind_not_in(kind_set: set):
        return not lookahead().kind in kind_set

    # 验证下一Token是标识符并返回标识符的名字
    def next_identifier():
        return assert_lookahead_kind_and_read(TokenKind.Identifier).value

    def pos():
        return token_steam.pos

    def test_lookahead_kind_sequence(kind_sequence):
        i = 0
        _len = len(kind_sequence)
        while i < _len:
            if not test_lookahead_kind(kind_sequence[i], i):
                return False
        return True

    # star返回一个可空的tuple
    # plus返回非空的tuple
    # optional返回None或者ctx

    def block() -> block_ctx:
        stat_star = []
        while not test_lookahead_kind(TokenKind.Eof):
            if test_lookahead_kind(TokenKind.Sep_Pound):
                stat_star.append(stat())
                k = lookahead().kind
                if k == TokenKind.Eof:
                    return block_ctx(stat_star=tuple(stat_star))
                else:
                    assert_lookahead_kind_and_read(TokenKind.Newline)
            else:
                assert_lookahead_kind_and_read(TokenKind.Newline)

    def stat():
        assert_lookahead_kind(TokenKind.Sep_Pound)
        k = lookahead(2).kind
        if k == TokenKind.Kw_Define:
            return define_stat()
        elif k == TokenKind.Kw_UnDef:
            return undef_stat()
        else:
            assert k == TokenKind.Kw_IfDef or k == TokenKind.Kw_UnDef, pos()
            return conditional_stat()

    def define_stat():
        assert_lookahead_kind_and_read(TokenKind.Sep_Pound)
        assert_lookahead_kind_and_read(TokenKind.Kw_Define)
        return define_stat_ctx(
            identifier=next_identifier(),
            token_string_optional=token_string_optional())

    def undef_stat():
        assert_lookahead_kind_and_read(TokenKind.Sep_Pound)
        assert_lookahead_kind_and_read(TokenKind.Kw_UnDef)
        identifier = next_identifier()
        return undef_stat_ctx(identifier=identifier)

    # 这个难一点
    def token_string_optional():
        if test_lookahead_kind_not_in({TokenKind.Kw_True, TokenKind.Kw_False,
                                       TokenKind.Char,
                                       TokenKind.Int, TokenKind.Float,
                                       TokenKind.String,
                                       TokenKind.Sep_LCurly}):
            return None
        k = lookahead().kind
        if k == TokenKind.Kw_True or k == TokenKind.Kw_False:
            return bool_exp()
        elif k == TokenKind.Char:
            return char_exp()
        elif k == TokenKind.Int:
            return int_exp()
        elif k == TokenKind.Float:
            return float_exp()
        elif k == TokenKind.String:
            return string_exp()
        else:
            assert k == TokenKind.Sep_LCurly
            return aggregate_exp()

    def bool_exp():
        k = next_token().kind
        return bool_exp_ctx(value=True if k == TokenKind.Kw_True else False)

    def char_exp():
        return char_exp_ctx(value=next_token().value)

    def int_exp():
        return int_exp_ctx(value=next_token().value)

    def float_exp():
        return float_exp_ctx(value=next_token().value)

    def string_exp():
        # TODO 我的string是一起的，要处理一下L字符串
        return string_exp_ctx(is_long_str=False, value=next_token().value)

    def aggregate_exp():
        next_token()
        fieldlist = fieldlist_optional()
        assert_lookahead_kind_and_read(TokenKind.Sep_RCurly)
        return aggregate_exp_ctx(fieldlist_optional=tuple(fieldlist))

    # fieldlist : token_string (',' token_string)* ','?;
    def fieldlist_optional():
        token_string_star = []
        i = token_string_optional()
        if i is None:
            return None
        token_string_star.append(i)
        while True:
            if test_lookahead_kind_sequence([TokenKind.Sep_Comma, TokenKind.Sep_RCurly]):
                break
            elif test_lookahead_kind(TokenKind.Sep_RCurly):
                break
            else:
                assert_lookahead_kind_and_read(TokenKind.Sep_Comma)
                t = token_string_optional()
                assert t
                token_string_star.append(t)
        return fieldlist_optional_ctx(token_string_star=token_string_star)

    def conditional_stat():
        return conditional_stat_ctx(
            if_part=if_part(),
            else_part_optional=else_part_optional()
        )

    def if_part():
        assert_lookahead_kind(TokenKind.Sep_Pound)
        k = lookahead(2).kind
        if_line = ifdef() if k == TokenKind.Kw_IfDef else ifndef()
        assert_lookahead_kind_and_read(TokenKind.Newline)
        return if_part_ctx(
            if_line=if_line,
            block=block())

    def else_part_optional():
        if test_lookahead_kind_sequence((TokenKind.Sep_Pound, TokenKind.Kw_Else)):
            next_token()
            next_token()
            assert_lookahead_kind_and_read(TokenKind.Newline)
            return else_part_optional_ctx(block=block())
        return None

    def ifdef():
        assert_lookahead_kind_and_read(TokenKind.Sep_Pound)
        assert_lookahead_kind_and_read(TokenKind.Kw_IfDef)
        return ifdef_ctx(identifier=next_identifier())

    def ifndef():
        assert_lookahead_kind_and_read(TokenKind.Sep_Pound)
        assert_lookahead_kind_and_read(TokenKind.Kw_IfNDef)
        return ifndef_ctx(identifier=next_identifier())

    return block(), assert_lookahead_kind_and_read(TokenKind.Eof)


# endregion

# test

test_id = 0


def test_log():
    global test_id
    print('---- start test %s' % test_id)
    test_id += 1


test_skip = 'test_data/lexer/skip.cpp'
test_define = 'test_data/define.cpp'
test_a = 'test_data/a.cpp'


# region test lexer
def tl(s):
    test_log()
    lexer = Lexer(s)
    token_steam: ITokenStream = TokenStream(lexer)
    while token_steam.not_eos:
        t = token_steam.next_token
        print(t)
        if t.kind == TokenKind.Eof:
            break


def tlf(f):
    tl(readall(f))


print('==== test lexer start')
tlf(test_skip)
tlf(test_define)
print('==== test lexer end')


# endregion

# region test parser

def tp(s):
    test_log()
    pprint(parse(s), width=1)


def tpf(f):
    tp(readall(f))


print('==== test parsr start')
tp('')
tp('#undef a')
tp('#define a')
tp('#define a 1')
tpf(test_skip)
tpf(test_define)
tpf(test_a)
print('==== test parser end')

# region final test

exit(0)

test_ai = PyMacroParser()
test_a2 = PyMacroParser()
test_ai.load("test_data/a.cpp")
filename = "test_data/b.cpp"
test_ai.dump(filename)  # 没有预定义宏的情况下，dump cpp
test_a2.load(filename)
a2_dict = test_a2.dumpDict()
test_ai.preDefine("MC1;MC2")  # 指定预定义宏，再dump
a1_dict = test_ai.dumpDict()
test_ai.dump("test_data/c.cpp")

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

# assert a1_dict == d1
# assert a2_dict == d2

# endregion
# endregion
