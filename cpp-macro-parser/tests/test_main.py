#!/usr/bin/python
# -*- coding: UTF-8 -*-

# [x] 提取测试框架，测试函数默认就打印start和end
# [x] 注释被当作空格，1.意义何在，和skip有什么区别
# [x] 封装自己的log替代print，pycharm有一个bug，就是普通print和std-err会混合在一起（估计是std-err在另一个线程）
#   这样就需要关掉log

from test_util import *

execfile('test_lexer.py')
execfile('test_parser.py')
execfile('test_vm.py')
execfile('test_question.py')
execfile('test_error.py')

log_style_warning('ALL TESTS PASS!')
