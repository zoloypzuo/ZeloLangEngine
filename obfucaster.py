cppcode = '''
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <cstdlib>
#include <algorithm>
#include <map>
#include <vector>
using namespace std;

map <string, int> dict;
int mp1[100];
int mp2[100];

int main() {
    dict.clear();
    dict["Adam"] = 1;       mp1[1] = 0;     mp2[1] = 930;
    dict["Seth"] = 3;       mp1[3] = 1;     mp2[3] = 920;
    dict["Enosh"] = 4;      mp1[4] = 3;     mp2[4] = 905;
    dict["Kenan"] = 5;      mp1[5] = 4;     mp2[5] = 910;
    dict["Mahalalel"] = 6;  mp1[6] = 5;     mp2[6] = 895;
    dict["Jared"] = 7;      mp1[7] = 6;     mp2[7] = 962;
    dict["Enoch"] = 8;      mp1[8] = 7;     mp2[8] = 365;
    dict["Methuselah"] = 9; mp1[9] = 8;     mp2[9] = 969;
    dict["Lamech"] = 10;    mp1[10] = 9;    mp2[10] = 777;
    dict["Noah"] = 11;      mp1[11] = 10;   mp2[11] = -1;
    dict["Shem"] = 12;      mp1[12] = 11;   mp2[12] = -1;
    dict["Ham"] = 13;       mp1[13] = 11;   mp2[13] = -1;
    dict["Japheth"] = 14;   mp1[14] = 11;   mp2[14] = -1;
    string s1, s2;
    while(cin >> s1 >> s2) {
        if(dict[s1] == 0 || dict[s2] == 0) {
            cout << "No enough information" << endl << "No enough information" << endl;
        }
        else {
            int n1 = dict[s1], n2 = dict[s2];
            if(n1 == n2)
                cout << "No" << endl;
            else {
                while(n2 != 0 && n2 != n1)
                    n2 = mp1[n2];
                if(n1 == n2)
                    cout << "Yes" << endl;
                else
                    cout << "No" << endl;
            }
            if(mp2[dict[s1]] == -1 || mp2[dict[s2]] == -1)
                cout << "No enough information" << endl;
            else {
                if(mp2[dict[s1]] > mp2[dict[s2]])
                    cout << "Yes" << endl;
                else
                    cout << "No" << endl;
            }
        }
    }
    return 0;
}



'''

# 整个混淆过程两步走
# 第一步识别变量声明，提取可以替换的名字
# 过短的名字需要告警，总的来讲，我们需要识别所有的变量，因为如果你漏掉了一个，那就很明显了，查重率会比较高
# 第二部执行替换，这个很简单，所以第一步要识别出容易替换的，而且要过滤掉一些容易产生替换问题的，比如单字符a，不可以，关键字，不可以
#
# 除此之外，我们需要添加无效代码来降低查重率，我估计是查重，也就是看一看你的文本和其他人的提交的文本的相似度
#
# 我们在前几个问题进行测试，因为难度低，系统不会查重，这里我们就开发和测试我们的混淆器
import re

from ParseGenerator import ParserGenerator

# 用例
#     string s1, s2;
# map <string, int> dict;
# int mp1[100], mp2[100];  // 这种多重声明+array声明被放弃。
cpp_decl_grammar = r'''
cpp_decl : multi_decl | map_decl | array_decl | simple_decl ;  // NOTE simple_decl is last match
simple_decl : SimpleType Id ;
multi_decl : SimpleType Id ',' Id ;  // only support 2 decl
map_decl : 'map' '<' SimpleType ',' SimpleType '>' Id ;
array_decl : SimpleType Id '[' Integer ']' ;
// ====
SimpleType : (int|float|string|bool);
Id : [_a-zA-Z][_a-zA-Z0-9]*;
Integer : \d+;
'''
parser = ParserGenerator(cpp_decl_grammar)


class Result:
    def __init__(self):
        self.decl_type = ""
        self.typename = ""
        self.id = ""
        self.id1 = ""  # set it if exists

    def __str__(self):
        return (self.decl_type,
                self.typename,
                self.id,
                self.id1,  # set it if exists)
                ).__str__()

    def __repr__(self):
        return self.__str__()


class CppDeclVisitor:
    def __init__(self, parser):
        self.NT = parser.NT
        self.stack = []

    @property
    def last_res(self):
        return self.stack[-1]

    def visit(self, node):
        '''访问节点，节点是nt和children的对'''
        nt, *children = node
        try:
            visit_nt = getattr(self, 'visit_' + nt)
            visit_nt(children)  # AttributeError: 'RegexVisitor' object has no attribute 'visit_a'
        except AttributeError:
            if nt in self.NT:  # visit NT
                self.visit_children(children)
            else:
                pass

    def visit_children(self, ctx):
        for symbol in ctx:
            self.visit(symbol)

    def visit_cpp_decl(self, ctx):
        self.stack.append(Result())
        self.visit_children(ctx)

    def visit_multi_decl(self, ctx):
        self.visit_children(ctx)
        res = self.last_res
        res.decl_type = "multi_decl"

    def visit_map_decl(self, ctx):
        self.visit_children(ctx)
        res = self.last_res
        res.decl_type = "map_decl"

    def visit_array_decl(self, ctx):
        self.visit_children(ctx)
        res = self.last_res
        res.decl_type = "array_decl"

    def visit_simple_decl(self, ctx):
        self.visit_children(ctx)
        res = self.last_res
        res.decl_type = "simple_decl"

    def visit_SimpleType(self, ctx):
        typename = ctx[0]
        res = self.last_res
        res.typename = typename

    def visit_Id(self, ctx):
        res = self.last_res
        _id = ctx[0]
        if not res.id:
            res.id = _id
        elif not res.id1:
            res.id1 = _id
        else:
            assert False, "too many id"


visitor = CppDeclVisitor(parser)


def gen_name(oldname, typename):
    new_name = ''
    type_abbr = typename[0]

    new_name = type_abbr + 'temp'
    if new_name not in obfuscator_map.values():
        return new_name
    else:
        oldname_abbr = oldname[0] + oldname[-1]
        new_name = oldname_abbr + 'temp'
        if new_name not in obfuscator_map.values():
            return new_name
        assert False


if __name__ != '__main__':
    exit(0)

cppcode = cppcode.strip()
lines = cppcode.splitlines()
words = cppcode.split()
types = {'string', 'int', 'bool', 'float'}
obfuscator_map = {}  # old name => new name

IdMinLength = 2  # name like a, will repalce all 'a' in cppcode

# find all local variables, generate new names for them
for line in lines:
    try:
        tree = parser.parse('cpp_decl', line.rstrip(';'))
        if tree:
            visitor.visit(tree)
            res = visitor.last_res
            print(res)
            if res.decl_type == 'multi_decl':
                if len(res.id) < IdMinLength:
                    pass
                else:
                    new_name = gen_name(res.id, res.typename)
                    obfuscator_map[res.id] = new_name
                if len(res.id1) < IdMinLength:
                    pass
                else:
                    new_name = gen_name(res.id1, res.typename)
                    obfuscator_map[res.id1] = new_name
            elif res.decl_type == 'map_decl':
                if len(res.id) < IdMinLength:
                    pass
                else:
                    new_name = gen_name(res.id, 'map' + res.typename)
                    obfuscator_map[res.id] = new_name
            elif res.decl_type == 'array_decl':
                if len(res.id) < IdMinLength:
                    pass
                else:
                    new_name = gen_name(res.id, 'array' + res.typename)
                    obfuscator_map[res.id] = new_name
            elif res.decl_type == 'simple_decl':
                if len(res.id) < IdMinLength:
                    pass
                else:
                    new_name = gen_name(res.id, res.typename)
                    obfuscator_map[res.id] = new_name
    except ValueError:
        continue

print(obfuscator_map)

# replace names in cpp src code
for k, v in obfuscator_map.items():
    cppcode = cppcode.replace(k, v)

print(cppcode)
