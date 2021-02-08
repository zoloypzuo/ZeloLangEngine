# ZeloLangEngine

一个极简的语法制导解析器框架
以及相关的语言应用

# 特点

* 简单，100行代码实现，可以自己调试和修改

# 用途

* 编写简单的语言工具
* 生成各种语言的代码
* 解析小型文件格式

# 例子

例子来源于以往的需求，为公司编写的工具不会包含在其中

| 名字 | 描述 |
| --- | --- |
cpp-macro-parser | C预处理器解析器
cpp-obfucastor | C代码混淆器
regex-engine | 正则表达式实现
unity-doc-generate-python-api | 从unity文档生成python接口
zjson | 扩展json序列化库
zlua-util | zlua工具
generate-csharp-test | 从lua代码生成C#单元测试代码
generate-csharp-vmloop | 生成虚拟机主循环代码
lua-manual-generate-csharp-api-and-xml-doc | 从lua官方文档生成C#接口

## C代码混淆器

大三学校内开了一门根本没人管的课程，其实就是用他的一套系统刷算法题 

网上找到以往的答案库直接复制粘贴

为了避免查重，打算混淆一下变量名

## zlua工具

写zlua中后期是一个比较琐碎的过程，一条一条指令实现，再一条一条实现C API，再编写单元测试

其实有些代码的架子是非常固定的，比如接口（和接口文档），虚拟机循环解析指令参数，执行一些lua代码来测试

因此这些代码都是一次性批量生成，避免了重复琐碎工作

## zjson

语法制导的入门，就是json语法

语法简单，测试用例完备

大概像下面这样用，直接就可以解析json了

```python
parse_literal, parse_number, parse_string, value, parse_array, pair, parse_obj = [0,0,0,0,0,0,0]
grammar = {
    'null|true|false': parse_literal,
    '-?[0-9]+(\.[0-9]+)?': parse_number,
    '\"(\\.|.)*\"': parse_string,
    (r'\[((%s\,)*%s)\]' % (value, value)): parse_array,
    (r'\{((%s,)*%s)\}' % (pair, pair)): parse_obj
}
```

## 正则表达式

这个可以说是比较硬核的，非常“编译原理”，用ZeloLangEngine开发的最复杂的语言应用了

实现了两套，一个是编译器，一个是解释器

正则的语法要复杂得多，还有坑，不过最简单的语法仍然很简单

如果支持标准的正则库的各种功能，比如捕获，这套框架肯定是不行了

正则表达式语法如下，喂给`ParserGenerator`即可解析出ast，然后用虚拟机执行

```python
regex_grammar = r'''
re : simple_re re_;
re_ : union re_ | Epsilon;
union : '|' simple_re;
simple_re : basic_re simple_re_;
simple_re_ : concat simple_re_ | Epsilon;
concat : basic_re;
basic_re :  star | plus | question | elementary_re;
star : elementary_re '*';
plus : elementary_re '+';
question : elementary_re '?';
elementary_re : group | any | eos | char | set;
group : '(' re ')';
any : '.';
eos : '$';
char : NonMetaChar | '\' MetaChar;
set : positive_set | negative_set;
positive_set : '[' set_items ']';
negative_set : '[^' set_items ']';
// set_items : set_item set_items | set_item;  使用下面这个debug方便
set_items : NonMetaChar set_items | NonMetaChar;
set_item : char | range;
range : char '-' char;
NonMetaChar : [^|*.+$()\\\[\]^?];  // regex [^|*.+$()\\[\]^]
MetaChar : [|*.+$()\\\[\]^?];  // '-' ???
Epsilon : '';
'''

```