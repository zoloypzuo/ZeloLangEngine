# coding=utf-8
import unittest

from test_vm import *


class TestError(unittest.TestCase):
    def test_main(self):
        # \shit不是合法token，lexer会返回一个error-token
        # 然后parser发现语法错误，跳过一行继续解析语句
        self.assertRaises(ParserException, tv, r'#define a \shit')
        # [x] parser应该跳过前两行，解析出最后一行语句，然后抛出错误，怎么测试
        self.assertRaises(ParserException, tv, '''#define a \\shit
#define a \\shit
#define a 1
''')


log_style('==== test error start', bcolors.HEADER)
unittest.main()
log_style('==== test error end', bcolors.HEADER)
