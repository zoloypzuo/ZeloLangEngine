#!/usr/bin/python
# -*- coding: UTF-8 -*-


from collections import namedtuple


# noinspection PyPep8Naming,PyShadowingNames


class PyMacroParser:
    def __init__(self):
        self.proto = None
        self.predefined_names = []

    def load(self, f):
        self.proto = Prototype(parse(readall(f)))

    def dump(self, filename):
        writeall(filename, dump(self.dumpDict()))

    def dumpDict(self):
        return execute(self.proto, self.predefined_names)

    def preDefine(self, s):
        if s == '':
            return
        names = [i for i in s.split(';') if i != '' and i.strip() != '']
        # 题目要求，每次调用自动清理掉之前的预定义宏序列
        self.predefined_names = names


# region common util


def readall(path):
    with open(path, 'r') as f:
        return f.read()


def writeall(path, text):
    with open(path, 'w') as f:
        f.write(text)


# python2没有enum
enum_id = -1


def auto():
    global enum_id
    enum_id += 1
    return enum_id


# endregion

# region lexer


# noinspection PyClassHasNoInit
class TokenKind:
    Eof = auto()
    Newline = auto()
    Identifier = auto()
    Int = auto()
    Float = auto()
    Char = auto()
    String = auto()
    WideString = auto()
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


# noinspection PyClassHasNoInit
class NumberType:
    Decimal = auto()
    Octal = auto()
    Hexadecimal = auto()
    Float = auto()


class LexerException(Exception):
    pass


WHITESPACE_CHARSET = set(' \t\v\f')


# str确实有一些帮助判断的函数，但是建议自己写
def is_whitespace(c):
    return c in WHITESPACE_CHARSET


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


def is_octal_digit(c):
    return '0' <= c <= '7'


Token = namedtuple('Token', ['pos', 'kind', 'value'])


# 包装Lexer为一个带前瞻的流对象
#
# 词法分析认为是复杂计算，因此前瞻时缓存结果
# 内部维护一个List<Token>包含所有已经计算的Token值，不删除旧的值，所有Token都会一直在内存
# NextToken对应于流的指针，而LookAhead(n)的n是相对于流指针的偏移
# LookAhead有单个元素和数组两个版本，因为我暂时不知道parser是否要用哪种，干脆都写
# NextToken和LookAhead在未计算所需Token时计算并缓存Token，从缓存中取出Token
class TokenStream:
    def __init__(self, lexer):
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
                #     # [x] 这个异常可以捕获，再想想；parser自己check eof token，而不是捕获异常
                #     # 比如 print(1缺一个右括号，parser调用lexer会走到这里
                #     raise LexerException('no more tokens')
                self.buffer.append(t)
                i += 1

    @property
    def pos(self):
        return self.buffer[self.pointer + 1].pos


class Lexer:
    def __init__(self, chunk):
        self.chunk = chunk  # source code
        self.line = 1  # current line number
        self.column = 1
        self.last_column = 1  # 构造Token时指针已经移动到lexeme末尾了，所以要延迟一下
        self.pointer = 0

    @property
    def next_token(self):

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
                elif is_whitespace(self.char):
                    self.advance(1)
                else:
                    break

        def res_token(kind, value=None):
            column = self.last_column
            self.last_column = self.column
            return Token((self.line, column), kind, value)

        skip()
        # 被跳过的内容不输出token，但是column要更新
        self.last_column = self.column
        if self.eof:
            return res_token(TokenKind.Eof)

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
            # [x] 没有宽字符，但是转义没有处理
            if self.eof:
                self.error("unfinished char")
            c = self.scan_char()
            if not self.test_char_is('\''):
                self.error("unfinished char")
            else:
                self.advance(1)
                # 题目要求char转int
                return res_token(TokenKind.Char, ord(c))
        elif c == '\"':
            s = self.scan_string()
            return res_token(TokenKind.String, s)
        else:
            if self.newline():
                return res_token(TokenKind.Newline)
            if self.test_prefix('L\"'):
                self.advance(1)
                # [x] 宽字符串如何处理
                s = unicode(self.scan_string())
                return res_token(TokenKind.WideString, s)
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
    def test_prefix(self, s):
        return self.chunk.startswith(s, self.pointer)

    def test_char_in_charset(self, charset):
        return self.not_eof and self.char in charset

    def test_char_predicate(self, predicate):
        return self.not_eof and predicate(self.char)

    def test_char_is_digit(self):
        return self.not_eof and is_digit(self.char)

    def try_advance_char_is(self, c):
        return self.try_advance_base(lambda: self.test_char_is(c), 1)

    def try_advance_prefix(self, s):
        return self.try_advance_base(lambda: self.test_prefix(s), len(s))

    def try_advance_char_in_charset(self, charset):
        return self.try_advance_base(lambda: self.test_char_in_charset(charset), 1)

    # 指针前进
    def advance(self, n):
        self.column += n
        self.pointer += n

    def error(self, msg):
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
            b = self.test_char_is_digit()
            while self.try_advance_base(self.test_char_is_digit, 1):
                pass
            return b

        c = self.char
        self.advance(1)
        if c == '.':  # float
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
                while self.test_char_predicate(is_octal_digit):
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
        string_builder = []
        while self.not_eof and self.char != '\"':
            string_builder.append(self.scan_char())
        if self.eof or self.char != '\"':
            self.error("unfinished string")
        else:
            self.advance(1)  # read the quote
            return ''.join(string_builder)

    def scan_char(self):
        c = self.char
        self.advance(1)
        # 处理转义
        if c != '\\':
            return c
        if self.eof:
            self.error("unfinished string")
        c = self.char
        self.advance(1)
        if c == 'a':
            return '\a'
        elif c == 'b':
            return '\b'
        elif c == 'f':
            return '\f'
        elif c == 'n':
            return '\n'
        elif c == 'r':
            return '\r'
        elif c == 't':
            return '\t'
        elif c == 'v':
            return '\v'
        elif c == '"':
            return '"'
        elif c == '\'':
            return '\''
        elif c == '\\':
            return '\\'
        elif c == '?':
            # python提示不支持这个转义字符
            self.error('python does not support escape sequence \\?')
            # return '\?'
        elif is_octal_digit(c):
            # 回退一格
            # 这里已经吃进一个八进制位了，不会出错
            p = self.pointer - 1
            while self.test_char_predicate(is_octal_digit):
                self.advance(1)
            return chr(int(self.chunk[p:self.pointer], 8))
        elif c == 'x':
            p = self.pointer
            if not self.test_char_predicate(is_hex_digit):
                self.error('unfinished hex escape char')
            while self.test_char_predicate(is_hex_digit):
                self.advance(1)
            return chr(int(self.chunk[p:self.pointer], 16))
        self.error("invalid escape sequence near '\\%s'" % c)


# endregion

# region parser


class ParserException(Exception):
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
def parse(chunk):
    token_steam = TokenStream(Lexer(chunk))

    def error(msg):
        raise ParserException("%s %s" % (pos().__str__(), msg.__str__()))

    def test_lookahead_kind(kind, n=1):
        return lookahead(n).kind == kind

    def next_token():
        return token_steam.next_token

    def lookahead(n=1):
        return token_steam.lookahead(n)

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

    def test_lookahead_kind_in(kind_set):
        return lookahead().kind in kind_set

    def test_lookahead_kind_not_in(kind_set):
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
            if not test_lookahead_kind(kind_sequence[i], i + 1):
                return False
            i += 1
        return True

    # star返回一个可空的tuple
    # plus返回非空的tuple
    # optional返回None或者ctx

    def block():
        def end_of_block():
            return test_lookahead_kind(TokenKind.Eof) or test_lookahead_kind_sequence(
                [TokenKind.Sep_Pound, TokenKind.Kw_Else]) or test_lookahead_kind_sequence(
                [TokenKind.Sep_Pound, TokenKind.Kw_EndIf])

        stat_star = []
        while not end_of_block():
            if test_lookahead_kind(TokenKind.Sep_Pound):
                stat_star.append(stat())
                if end_of_block():
                    break
                else:
                    assert_lookahead_kind_and_read(TokenKind.Newline)
            else:
                assert_lookahead_kind_and_read(TokenKind.Newline)
        return block_ctx(stat_star=tuple(stat_star))

    def stat():
        assert_lookahead_kind(TokenKind.Sep_Pound)
        k = lookahead(2).kind
        if k == TokenKind.Kw_Define:
            return define_stat()
        elif k == TokenKind.Kw_UnDef:
            return undef_stat()
        else:
            assert k == TokenKind.Kw_IfDef or k == TokenKind.Kw_IfNDef, pos()
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
                                       TokenKind.String, TokenKind.WideString,
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
        elif k == TokenKind.WideString:
            return wide_string_exp()
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
        # [x] 我的string是一起的，要处理一下L字符串
        return string_exp_ctx(is_long_str=False, value=next_token().value)

    def wide_string_exp():
        return string_exp_ctx(is_long_str=True, value=next_token().value)

    def aggregate_exp():
        next_token()
        fieldlist = fieldlist_optional()
        assert_lookahead_kind_and_read(TokenKind.Sep_RCurly)
        return aggregate_exp_ctx(fieldlist_optional=fieldlist)

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
        if_part_ = if_part()
        else_part_optional_ = else_part_optional()
        assert_lookahead_kind_and_read(TokenKind.Sep_Pound)
        assert_lookahead_kind_and_read(TokenKind.Kw_EndIf)
        return conditional_stat_ctx(
            if_part=if_part_,
            else_part_optional=else_part_optional_
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

# region code generation
class Prototype:
    def __init__(self, ast):
        self.ast = ast


# endregion

# region vm

class RuntimeException(Exception):
    pass


# 时间紧张。。直接执行ast
def execute(proto, predefined_names=None):
    defined_variables = {}
    if predefined_names:
        for name in predefined_names:
            defined_variables[name] = None
    visit_functions = {}

    def error(msg):
        raise RuntimeException(msg)

    def visit(ctx):
        # op = locals()['visit_' + type(ctx).__name__]
        op = visit_functions['visit_' + type(ctx).__name__]
        return op(ctx)

    def visit_block_ctx(ctx):
        for stat in ctx.stat_star:
            visit_stat_ctx(stat)

    def visit_stat_ctx(ctx):
        visit(ctx)

    def visit_define_stat_ctx(ctx):
        id_ = ctx.identifier
        token_string_optional = ctx.token_string_optional
        defined_variables[id_] = visit(token_string_optional) if token_string_optional else None

    def visit_undef_stat_ctx(ctx):
        id_ = ctx.identifier
        # [Different ways to Remove a key from Dictionary in Python | del vs dict.pop() – thispointer.com](
        # https://thispointer.com/different-ways-to-remove-a-key-from-dictionary-in-python/)
        defined_variables.pop(id_, None)

    def visit_bool_exp_ctx(ctx):
        return ctx.value

    def visit_char_exp_ctx(ctx):
        return ctx.value

    def visit_int_exp_ctx(ctx):
        return ctx.value

    def visit_float_exp_ctx(ctx):
        return ctx.value

    def visit_string_exp_ctx(ctx):
        return ctx.value

    def visit_aggregate_exp_ctx(ctx):
        fieldlist_optional_ = ctx.fieldlist_optional
        return visit_fieldlist_optional_ctx(fieldlist_optional_) if fieldlist_optional_ else tuple()

    def visit_fieldlist_optional_ctx(ctx):
        return tuple(visit(token_string) for token_string in ctx.token_string_star)

    def visit_conditional_stat_ctx(ctx):
        take_if, if_block = visit_if_part_ctx(ctx.if_part)
        if take_if:
            visit_block_ctx(if_block)
        elif ctx.else_part_optional:
            else_block = ctx.else_part_optional.block
            visit_block_ctx(else_block)
        # else return

    def visit_if_part_ctx(ctx):
        return visit(ctx.if_line), ctx.block

    def visit_ifdef_ctx(ctx):
        return ctx.identifier in defined_variables

    def visit_ifndef_ctx(ctx):
        return ctx.identifier not in defined_variables

    visit_functions = {k: v for k, v in locals().items() if k.startswith('visit_')}
    block_, eof_ = proto.ast
    visit_block_ctx(block_)
    return defined_variables


# endregion

# region dumper

# 返回字符串
def dump(defined_variables):
    def py2cpp(o):
        if isinstance(o, bool):
            return 'true' if o else 'false'
        # NOTE BUG bool is int in python
        elif isinstance(o, int):
            return o.__str__()
        elif isinstance(o, float):
            return o.__str__()
        elif isinstance(o, str):
            return '"%s"' % o
        # [x] 宽字符串
        elif isinstance(o, unicode):
            return 'L"%s' % o
        else:
            assert isinstance(o, tuple)
            return "{%s}" % ', '.join(py2cpp(i) for i in o)

    def define(name, value=None):
        return '#define %s %s' % (
            name, py2cpp(value) if value is not None else '')

    return '\n'.join(
        define(name, value)
        for name, value in defined_variables.items())

# endregion
