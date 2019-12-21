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
    Identifier = auto()
    Int = auto()
    Float = auto()
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


class Token:

    def __init__(self, line: int, kind: TokenKind, lexeme: str):
        self.line: int = line
        self.kind: TokenKind = kind
        self.lexeme: str = lexeme


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


class Lexer:
    def __init__(self, chunk: str):
        self.chunk = chunk  # source code
        self.line = 1  # current line number
        self.column = 1
        self.nextToken = ""
        self.nextTokenKind = 0
        self.nextTokenLine = 0
        self.pointer = 0

    def next_token(self) -> Token:

        def skip():
            while self.not_eof:
                if self.test('//'):
                    self.next(2)
                    while self.not_eof and not is_newline(self.char):
                        self.next(1)
                elif self.test('/*'):
                    self.next(2)
                    while not self.test('*/'):
                        # 注释会包含换行
                        if self.test('\r\n') or self.test('\n\r') or is_newline(self.char):
                            self.line += 1
                        self.next(1)
                    else:  # while else
                        self.next(2)
                # elif self.test('\r\n') || self.test('\n\r'):
                #     self.next(2)
                #     self.line+=1
                elif is_whitespace(self.char):
                    self.next(1)
                else:
                    break

        skip()

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
    def next(self, n: int):
        self.pointer += n

    def error(self, msg: str):
        raise LexerException(self.line, self.column, msg)

    @property
    def char(self):
        return self.chunk[self.pointer]
# Lexer('a').error("asd")
