# ZJson

## 序列化与反序列化
zjson 提供了一个功能比较弱的序列化与反序列化小工具，扩展标准库，解决其无法序列化，反序列化 class obj 的问题

对参与序列化与反序列化的类的字段的要求：
手写，无继承，符合json标准（尤其是，dict的key是str），无递归结构

requirement:
1. class should be built by yourself, to avoid tricky things like Datetime?
2. class should conform to json standard:
    1. use list, tuple, set, frozenset, collections.namedtuple
    2. use dict, and only use str as key (avoid tuple, int, float)
    3. use primitive type: int, float, str, bool, None
3. class should not use inheritance

### TODO
TODO 爆了一个bug：两个对象如果有字段引用对方，形成循环引用，那么zjson会无限递归

需要缓存一下实例，另外开一个cache存id=>instance_dict，这种思路可以让每一个实例的__dict__在json中只存储一次，然后占主体中只存id，其实就是模拟了指针
反序列化的时候，识别出id并从cache中加载

## Parser
在学完了 milo yip 的json教程后，写一个Python版的原型
### 动机
milo yip的还是太难了，考虑到了很多细节和复杂的主题。按照我的想法，一个教程其实至少需要两遍（2 pass）才能把学习曲线降下来，我这次就是写第一遍。
从抽象的角度写一个json parser的框架，或者说是从design of program的角度。我们不考虑性能，尽可能快速地开发完，过一段时间 TODO 用C++把milo的写一遍，要求掌握性能方面的细节。

### 总结

做出来了。但是自己不是很懂。还有很多问题想不清楚。而且对现在发生的问题也解决不好。

仍然是一个手写的parser，手写parser是很重要的。一般来说它会比antlr这种东西快。你在做antlr前必须先手写几个parser，才能体会错误处理为首的几个实践才能清楚的问题。当然是语言的parser，推荐实现《权威指南》里的内容。

### 关于 ZJson 本身的提问

1. 如何处理错误？
   1. parser自己有Synatx Error，细分的子类不清楚，因为有curr index，可以直接sytax error + index
   2. compile 还有自己的语言的要求，这些是在visitor里raise的，是compile error
   3. runtime error，略，一个道理
2. 如何将语法规则变成代码？
   1. 参考龙书正规方法，你需要回忆一下。手写parser就是一个翻译语法规则到代码的过程，代码里是没有规则的，通过for alt in alts match 所有alt并分派给visitor

### 关于语言应用这个领域的提问

#### 大概的架构

1. Parser类 是一个完整的，独立的 parser，启动后可以分析出语法错误，可以正确解析问题，但是不会发生任何事，因为还没有实现动作，或者说 visitor 这个语言应用层。而默认是空实现
2. Parser类 提供从 antlr语法DSL 得到的所有信息，这些可以在 visitor 中使用

3. parser 从 parse(start_symbol, remainder) 开始，你可以包装一层，这样更加自然
4. 但是这种架构是非常慢的，对于 python 而言，因为string是不可变的，这样会；另外这种先整体验证格式，再处理整个东西的方式的架构会遍历非常多次整个 text，应该是n ^ 2以上的复杂度，这是不可接受的，一定要转换成 index 风格；重新总结一遍，1. 不能这样验证整个格式，match .* 这种复杂度是O(n) 2. 不能使用remainder string，而是 curr index；至于怎么做，这是look ahead多少的问题。json十分简单，look ahead 1 char 即可得知走哪个alt；然后再验证，然后再解析；总之，目前的架构太粗糙，虽然美观，但是性能极差
5. zjson的思路是，先match以检验整体的格式正确，用match obj捕获匹配的正文后递归的解析它；思路是对的，因为龙书正规的做法前面这部分也是确定调用哪个函数来处理这段文本，但是这个会繁琐的多；visitor pattern 完全可以被按dict调用替代。

