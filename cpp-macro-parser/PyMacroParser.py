#!/usr/bin/python
# -*- coding: UTF-8 -*-

# region 简易沙箱，你不应该再import任何东西了

import sys

blacklist = ['re']
for mod in blacklist:
    i = __import__(mod)
    sys.modules[mod] = None
eval = None
exec = None
copy = None
deepcopy = None

from enum import Enum, auto


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
    # 至多前瞻一个token
    # 前瞻的token被缓存，反复调用lookahead只会返回这个缓存
    # 调用一次next_token后这个缓存被清空
    @property
    def lookahead(self):
        pass

    def next_token_of_kind(self, kind: TokenKind):
        pass

    @property
    def next_identifier(self):
        pass

    @property
    def next_token(self) -> tuple:
        pass


class Lexer(ILexer):
    def __init__(self, chunk: str):
        self.chunk = chunk  # source code
        self.line = 1  # current line number
        self.column = 1
        self.last_column = 1  # 构造Token时指针已经移动到lexeme末尾了，所以要延迟一下
        self.cached_lookahead = tuple()
        self.pointer = 0

    @property
    def lookahead(self):
        if not self.cached_lookahead:
            self.cached_lookahead = self.next_token
        return self.cached_lookahead

    def next_token_of_kind(self, kind: TokenKind):
        line, _kind, lexeme = self.next_token
        assert kind == _kind, "syntax error near '%s'" % lexeme
        return line, lexeme

    @property
    def next_identifier(self):
        return self.next_token_of_kind(TokenKind.Identifier)

    @property
    def next_token(self) -> tuple:

        def skip():
            while self.not_eof:
                if self.test_str('//'):
                    self.advance(2)
                    while self.not_eof and not is_newline(self.char):
                        self.advance(1)
                elif self.test_str('/*'):
                    self.advance(2)
                    while not self.test_str('*/'):
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

        def Token(kind: TokenKind, lexeme=None):
            column = self.last_column
            self.last_column = self.column
            return (self.line, column), kind, lexeme

        # 尝试使用cache
        if self.cached_lookahead:
            self.cached_lookahead = tuple()
            return self.cached_lookahead

        skip()
        # 被跳过的内容不输出token，但是column要更新
        self.last_column = self.column
        if self.eof:
            return Token(TokenKind.Eof)

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
            return Token(TokenKind.Sep_Pound)
        elif c == '{':
            self.advance(1)
            return Token(TokenKind.Sep_LCurly)
        elif c == '}':
            self.advance(1)
            return Token(TokenKind.Sep_RCurly)
        elif c == ',':
            self.advance(1)
            return Token(TokenKind.Sep_Comma)
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
                return Token(TokenKind.Char, c)
        elif c == '\"':
            s = self.scan_string()
            return Token(TokenKind.String, s)
        else:
            if self.newline():
                return Token(TokenKind.Newline)
            if self.test_str('L\"'):
                self.advance(1)
                # TODO 宽字符串如何处理
                s = self.scan_string()
                return Token(TokenKind.String, s)
            if c == '.' or is_digit(c):
                t, v = self.scan_number()
                if t == NumberType.Decimal or t == NumberType.Hexadecimal or t == NumberType.Octal:
                    return Token(TokenKind.Int, v)
                elif t == NumberType.Float:
                    return Token(TokenKind.Float, v)
                else:
                    raise Exception("unreachable")
            if c == '_' or is_letter(c):
                identifier = self.scan_identifier()
                assert identifier.isidentifier()
                # 关键字是这样处理的：先用id来lex，然后优先判定关键字
                res = keywords.get(identifier)
                if res:
                    return Token(res)
                else:
                    return Token(TokenKind.Identifier, identifier)
        self.error("unexpected symbol near %s" % c)

    # 返回是否吃进换行符，如果是，更新行号和列号
    # 返回False的情况下，newline对当前字符什么都不做，交给调用者处理
    def newline(self):
        if self.test_str('\r\n') or self.test_str('\n\r'):
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

    # test类函数会检查eof，如果因为遇到eof，也是返回false
    # 下面的test类函数不必调用test-base，避免小调用，但是应该参考这个
    def test_base(self, predicate):
        return self.not_eof and predicate()

    def try_advance_base(self, test, n):
        res = test()
        if res:
            self.advance(n)
        return res

    def test_char(self, c):
        return self.not_eof and self.char == c

    # 测试chunk接下来是否是s，类似于re.match
    def test_str(self, s: str):
        return self.chunk.startswith(s, self.pointer)

    def test_charset(self, charset):
        return self.not_eof and self.char in charset

    def test_predicate(self, predicate):
        return self.not_eof and predicate(self.char)

    def try_advance_char(self, c):
        return self.try_advance_base(lambda: self.test_char(c), 1)

    def try_advance_str(self, s: str):
        return self.try_advance_base(lambda: self.test_str(s), len(s))

    # 自己决定charset是str还是set
    def try_advance_charset(self, charset):
        return self.try_advance_base(lambda: self.test_charset(charset), 1)

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

        # 转为python都是int，所以后缀信息没用
        # 而且实测int函数不能解析后缀，所以要先解析再advance
        def abandon_int_suffix():
            self.try_advance_str('ll')
            self.try_advance_str('LL')
            self.try_advance_charset(set('lLuU'))

        def exponent_part():
            if self.not_eof and self.try_advance_charset('eE'):
                self.try_advance_charset('+-')
                while not self.not_eof and is_digit(c):
                    self.advance(1)

        c = self.char
        self.advance(1)
        if c == '.':  # float
            pass
        elif c == '0':  # oct or hex
            c = self.char
            if self.try_advance_charset('xX'):  # hex
                if not self.test_predicate(is_hex_digit):
                    raise LexerException("unfinished hex int")
                while self.test_predicate(is_hex_digit):
                    self.advance(1)
                value = int(lexeme(), 16)
                abandon_int_suffix()
                return NumberType.Hexadecimal, value
            else:  # oct
                while self.not_eof and '0' <= self.char <= '7':
                    self.advance(1)
                value = int(lexeme(), 8)
                abandon_int_suffix()
                return NumberType.Octal, value
        else:  # int or float
            assert '1' <= c <= '9'
            # 不管是int还是float，首先解析出整数
            while self.not_eof and is_digit(self.char):
                self.advance(1)
            else:  # while else
                if self.not_eof and self.test_charset('.eE'):  # float
                    if self.not_eof and self.try_advance_char('.'):
                        while not self.not_eof and is_digit(c):
                            self.advance(1)
                    exponent_part()
                    value = float(lexeme())
                    self.try_advance_charset('fF')
                    return NumberType.Float, value
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


# Lexer('a').error("asd")
# TODO 这里应该有很多地方没有check eof就读了，再想想


def t(s):
    lexer = Lexer(s)
    while True:
        a = lexer.next_token
        print(a)
        _, k, _ = a
        if k == TokenKind.Eof:
            break


def tf(f):
    t(readall(f))


tf('test_data/lexer/skip.cpp')
tf('test_data/define.cpp')
