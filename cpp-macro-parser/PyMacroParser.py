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


# noinspection PyPropertyDefinition
class ILexer:
    @property
    def eof(self):
        pass

    @property
    def not_eof(self):
        pass

    @property
    def next_token(self) -> tuple:
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
    def eos(self):
        pass

    @property
    def not_eos(self):
        pass

    # 前瞻，不前进流指针
    def lookahead(self, n=1):
        pass

    def lookahead_array(self, n):
        pass

    # 返回下一个token，前进一格流指针
    @property
    def next_token(self):
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
        self.cache_if_need(1)
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
        l = len(self.buffer)
        p = self.pointer

        # 初始值 0 <= -1 + 1
        if l <= p + n:
            # 初始值 1 = -1+1-0+1
            n_to_cache = p + n - l + 1
            i = 0
            while i < n_to_cache:
                t = self.lexer.next_token
                # if self.lexer.eof():
                #     # TODO 这个异常可以捕获，再想想；parser自己check eof token，而不是捕获异常
                #     # 比如 print(1缺一个右括号，parser调用lexer会走到这里
                #     raise LexerException('no more tokens')
                self.buffer.append(t)
                i += 1

    def add(self, item):
        self.buffer.append(item)

    def try_get(self, i):
        _i = self.pointer + i
        if _i >= len(self.buffer):
            return False, None
        else:
            return self.buffer[_i]

    def __getitem__(self, item: int):
        return self.buffer[self.pointer + item]

    def advance(self, n):
        self.pointer += n


class Lexer(ILexer):
    def __init__(self, chunk: str):
        self.chunk = chunk  # source code
        self.line = 1  # current line number
        self.column = 1
        self.last_column = 1  # 构造Token时指针已经移动到lexeme末尾了，所以要延迟一下
        self.pointer = 0

    @property
    def next_token(self) -> tuple:

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
            return (self.line, column), kind, value

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


# 返回AST，我们使用lisp
# TODO lookahead(k)
def parse(chunk) -> tuple:
    token_steam: ITokenStream = TokenStream(Lexer(chunk))

    def error(msg):
        raise ParserException(msg)

    def test_lookahead_kind(kind: TokenKind):
        _, _kind, _ = token_steam.lookahead()
        return kind == _kind

    def next_token():
        return token_steam.next_token

    def lookahead():
        return token_steam.lookahead

    def lookahead_kind():
        _, _kind, _ = token_steam.lookahead
        return _kind

    # assert grammar function
    # 每个语法成分对应一个函数
    # 函数返回一个bool和ast
    # bool代表是否有这个语法成分，交给调用者用于判断
    def assert_has_NT(g_function):
        b, ast = g_function()
        if not b:
            error("miss %s" % g_function.__name__)
        else:
            return ast

    def assert_has_T(kind):
        res = lexer.lookahead
        _, _kind, _ = res
        if kind != _kind:
            error("expect Token %s, get actual %s" % (kind, _kind))
        return res

    def star(*g_functions):
        pass

    def block():
        ctx = []
        while not test_lookahead_kind(TokenKind.Eof):
            res, ast = stat()
            if res:
                ctx.append(ast)
                k = lookahead_kind()
                if k == TokenKind.Eof:
                    return True, tuple(ctx)
                else:
                    assert_has_T(TokenKind.Newline)
        return True, tuple(ctx)

    def stat():
        b = test_lookahead_kind(TokenKind.Sep_Pound)
        if not b:
            return False, tuple()
        next_token()
        k = lookahead_kind()
        if k == TokenKind.Kw_Define:
            return True, ('stat', assert_has_NT(define_stat))
        elif k == TokenKind.Kw_UnDef:
            return True, ('stat', assert_has_NT(undef_stat))
        else:
            assert k == TokenKind.Kw_IfDef or k == TokenKind.Kw_UnDef
            return True, ('stat', assert_has_NT(conditional))

    def define_stat():
        pass

    def undef_stat():
        pass

    def conditional():
        pass

    return 'chunk', assert_has_NT(block), assert_has_T(TokenKind.Eof)


# endregion

# test

# region test lexer
def tl(s):
    lexer = Lexer(s)
    token_steam: ITokenStream = TokenStream(lexer)
    while token_steam.not_eos:
        t = token_steam.next_token
        print(t)
        pos, kind, value = t
        # print(pos, kind, value)
        # if kind == TokenKind.Float:
        #     print(pos, value)
        if kind == TokenKind.Eof:
            break


def tlf(f):
    tl(readall(f))


print('==== test lexer start')
tlf('test_data/lexer/skip.cpp')
tlf('test_data/define.cpp')
print('==== test lexer end')


# endregion

# region test parser

def tp(s):
    pprint(parse(s), width=2)


print('==== test parsr start')
tp('')
tp('#define a')
print('==== test parser end')
# endregion
