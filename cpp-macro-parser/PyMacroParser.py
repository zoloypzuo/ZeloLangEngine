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
    Op_Minus = auto()  # -
    Op_Add = auto()  # +
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


class Lexer:
    def __init__(self, chunk: str):
        self.chunk = chunk  # source code
        self.line = 1  # current line number
        self.column = 1
        self.last_column = 1  # 构造Token时指针已经移动到lexeme末尾了，所以要延迟一下
        self.cached_lookahead = tuple()
        self.pointer = 0

    # 至多前瞻一个token
    # 前瞻的token被缓存，反复调用lookahead只会返回这个缓存
    # 调用一次next_token后这个缓存被清空
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
                if self.test('//'):
                    self.advance(2)
                    while self.not_eof and not is_newline(self.char):
                        self.advance(1)
                elif self.test('/*'):
                    self.advance(2)
                    while not self.test('*/'):
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

        def Token(kind: TokenKind, lexeme: str = ''):
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
            if c == '.' or is_digit(c):
                # TODO
                pass
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
        if self.test('\r\n') or self.test('\n\r'):
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

    # 测试chunk接下来是否是s，类似于re.match
    def test(self, s: str):
        return self.chunk.startswith(s, self.pointer)

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
    def scan_number(self):
        pass

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

# l = Lexer('#define a')
l = Lexer('#define a "asda" \'c\'')
while True:
    a = l.next_token
    print(a)
    _, k, _ = a
    if k == TokenKind.Eof:
        break
# ((1, 1), <TokenKind.Sep_Pound: 8>, '')
# ((1, 2), <TokenKind.Kw_Define: 16>, '')
# ((1, 9), <TokenKind.Identifier: 3>, 'a')
# ((1, 11), <TokenKind.String: 7>, 'asda')
# ((1, 18), <TokenKind.Char: 6>, 'c')
# ((1, 21), <TokenKind.Eof: 1>, '')
