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


class Lexer:
    def __init__(self, chunk: str):
        self.chunk = chunk  # source code
        self.line = 0  # current line number
        self.nextToken = ""
        self.nextTokenKind = 0
        self.nextTokenLine = 0
