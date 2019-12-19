# noinspection PyPep8Naming,PyShadowingNames
class PyMacroParser:
    def load(self, f):
        """
        从指定文件中读取CPP宏定义，存为python内部数据，以备进一步解析使用。
        :param f: f为文件路径
        :return: 无返回值
        :exception: 文件操作失败抛出异常；若在初步解析中遇到宏定义格式错误 或 常量类型数据定义错误应该抛出异常
        """
        pass

    def dump(self, filename):
        """
        结合类中的CPP宏定义数据与预定义宏序列，解析输出所有可用宏存储到新的CPP源文件，
        f为CPP文件路径，文件若存在则覆盖，文件操作失败抛出异常。
        若遇到宏定义格式错误 或 常量类型数据定义错误应该抛出异常。
        注意，转换后的常量数据表示应与Python对应类型兼容， 所以常量类型的长度存储信息可能丢失
        （例如 short 转为 int; float 转为 double 等）,
        允许特别表示方法信息丢失（例如原本16进制 统一变成10进制表示等）。 导出宏的顺序不做特别要求。
        :param filename:
        :return:
        """
        pass

    def dumpDict(self):
        """
        返回一个dict， 结合类中存储的CPP宏定义与预定义的宏序列，解析输出所有的可用宏到一个字典，
        其中宏名转为字符串后作为字典的key, 若有与宏名对应的常量转为python数据对象，无常量则存为None,
        注意不要返回类中内置的对象的引用。 解析过程若遇到宏定义格式错误 或 常量类型数据定义错误应该抛出异常；
        :return:
        """
        pass

    def preDefine(self, s):
        """
        输入一堆预定义宏名串，宏名与宏名之间以”;” 分割。

        比如串"mcname1;mcname2"相当于把
        #define mcname1
        #define mcname2
        加在了CPP宏数据的最前面。
        而空串"" 表示没有任何预定义宏。 显然，预定义宏会影响对CPP文件数据内的可用宏解析。

        preDefine函数可被反复调用，每次调用自动清理掉之前的预定义宏序列。
        preDefine 与 load的CPP宏定义数据，一起决定最终可用的宏。
        :return:
        """
        pass


a1 = PyMacroParser()
a2 = PyMacroParser()
a1.load("a.cpp")
filename = "b.cpp"
a1.dump(filename)  # 没有预定义宏的情况下，dump cpp
a2.load(filename)
a2.dumpDict()
a1.preDefine("MC1;MC2")  # 指定预定义宏，再dump
a1.dumpDict()
a1.dump("c.cpp")

# 则b.cpp输出
b = \
    '''
#define data1 1.0 //浮点精度信息消失，统一转成了double 正式输出没有这个注释
#define data2 2
#define data3 false
#define data4 "this is a data"
#define data5 68 //注意：这里本是'D' 转换后成为整型十进制表示，正式输出没有这个注释
#define data6 {1, 6}
#define MCTEST //空宏，但是被定义了, 正式输出没有这个注释
'''

# a2.dump字典
d2 = \
    {
        "data1": 1.0,
        "data2": 2,
        "data3": False,
        "data4": "this is a data",
        "data5": 68,
        "data6": (1, 6),
        "MCTEST": None,  # 空宏，但被定义了。 正式输出没有这个注释
    }

# a1.dump字典：
d1 = \
    {
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
c = \
    '''
#define data1 32 //16进制表示消失。 正式输出没有这个注释
#define data2 2.5
#define data3 L"this is a data" //unicode 转回宽字符 正式输出没有这个注释
#define data4 true
#define data5 97 //'a', 正式输出没有这个注释
#define data6 {{2.0, "abc"}, {1.5, "def"}, {5.6, "7.2"}} #tuple转回聚合， 正式输出没有这个注释
#define MC1
#define MCTEST
'''

# test tool
# 比较文件输出与目标字符串（或文件）
# 比较dict
