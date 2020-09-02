# coding=utf-8
from PyMacroParser import *

test_a1 = PyMacroParser()
test_a2 = PyMacroParser()
test_a1.load("../test_data/a.cpp")
filename = "../test_data/b.cpp"
test_a1.dump(filename)  # 没有预定义宏的情况下，dump cpp
test_a2.load(filename)
a2_dict = test_a2.dumpDict()
test_a1.preDefine("MC1;MC2")  # 指定预定义宏，再dump
a1_dict = test_a1.dumpDict()
test_a1.dump("../test_data/c.cpp")

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

assert a1_dict == d1
assert a2_dict == d2
