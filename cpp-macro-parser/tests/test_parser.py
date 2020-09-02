from PyMacroParser import *
from test_util import *
def tp_(s, chunkname):
    parse(s, chunkname)


def tp(s):
    test_log(s)
    parse(s)
    tp_(s, s)


def tpf(f):
    test_log(f)
    parse(readall(f), f)
    tp_(readall(f), f)


log_style('==== test parser start', bcolors.HEADER)
tpf(test_a)

tp('')
tp('#undef a')
tp('#define a')
tp('#define a 1')
tpf(test_skip)
tpf(test_define)
tpf(test_a)
log_style('==== test parser end', bcolors.HEADER)