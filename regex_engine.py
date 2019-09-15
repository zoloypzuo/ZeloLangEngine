import re

# literal, concat, alt, opt, star, plus
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


class ParserGenerator:
    def __init__(self, description, whitespace='\s*'):
        """
        简单解析语法描述到语法数据结构
        修改如下： // 修改可能导致bug
        1. 去掉符号两侧的引号，这是antlr语法
        2. 去掉注释
        3. NT和T形式有要求，并根据这个分拣到两个集合中
        对语法的要求如下：
        0. 已使用antlr语法
        1. 每行形如 Symbol : A1 A2 ... | B1 B2 ... | C1 C2 ... ;
        2. |和=>两侧必须有空格，符号之间必须有空格
        3. 使用\来行拼接
        4. 不支持antlr的克林闭包
        5. NT小写蛇形，T大写Pascal
        6. 不支持换行，分号是为了兼容antlr编辑器
        7. 直接写在生成式中的token不必转义，
        比如 group : '\(' re '\)'; 中的括号，因为token是交给正则库的，括号是正则表达式的特殊字符
        其实就是这个[|*.+$\(\)\\[\]^]，哈哈哈
        8. 空白符会被跳过，注意比如regex，空白符不能被跳过
        """

        def split(text, sep=None, max_split=-1):
            '''类似str.split，但是返回的列表中的每个字符串两侧都没有空白，没有空串
            TODO 会有空串，t.strip后还要过滤空串依次
            这个函数不好，太糙了。多次strip和过滤空串，是非常糟糕的，使用解析一遍就可以处理这些问题
            '''
            return [t.strip() for t in text.strip().split(sep, max_split) if t]

        def map_alts(alts):
            def map_alt(alt):
                for s in alt:  # for s in alt
                    if re.match('\'.*\'$', s):  # if s is like 'xxx'
                        s = re.sub('([|*.+$(\\\)\[\]^?])', r'\\\1', s.strip('\''))  # 脱掉引号，再为特殊字符转义
                    else:
                        pass
                    yield s

            for alt in alts:
                yield tuple(map_alt(alt))

        self.G = {' ': whitespace}
        self.NT = set()  # 没用，我本来试图用这个来改parse的判断
        # 但是是错的，写在生成式中的token并没有单独写一个生成式，因此这样递归是必要的
        self.T = set()
        description = re.sub('(//.*)?', '', description)  # 移除注释
        for line in filter(
                lambda s: not re.match('\s*$', s),
                (s.replace('\n', ' ') for s in description.split(';'))):  # 根据分号分行，并用空格替代\n，最终过滤掉纯ws串
            lhs, rhs = line.split(' : ', 1)  # 这里开始我使用自定的split，简单粗暴
            lhs = lhs.strip()
            if lhs.islower():
                self.NT.add(lhs)
            else:
                self.T.add(lhs)
            alternatives = split(rhs, ' | ')
            self.G[lhs] = tuple(map_alts(map(split, alternatives)))

            # 错误得函数式写法，少一层list，很难写对
            # self.G[lhs.strip()] = tuple(  # lhs 需要strip，这是个细节，写得不好
            #     re.sub('([|*.+$(\\\)\[\]^])', r'\\\1', s.strip('\''))
            #     if re.match('\'.*\'$', s) else s  # for s in alt if s is like 'xxx'
            #     for alt in map(split, alternatives)  # for alt in alts
            #     for s in alt
            # )
            # if lhs.islower():
            #     # self.NT.add(lhs)
            #     self.G[lhs] = tuple(map(split, alternatives))
            # else:
            #     # rhs=re.compile(rhs)
            #     # self.T.add(lhs)
            #     self.G[lhs] = rhs

        self.tokenizer = self.G[' '] + '(%s)'  # 跳过空白和token
        self.Fail = (None, None)

    def parse(self, start_symbol, text):
        """
        返回AST或抛出语法错误异常
        对语法的要求：因为是回溯的LL，所以不允许左递归（左公因子没关系），各个alt是按顺序尝试的，所以顺序是有影响的

        parse_atom和parse_sequence返回(tree, remainder)，remainder是''说明成功解析完毕，remainder是None说明解析失败

        """

        def parse_sequence(sequence, text):
            """
            Try to match the sequence of atoms against text.

            Parameters:
            sequence : an iterable of atoms
            text : a string

            Returns:
            Fail : if any atom in sequence does not match
            (tree, remainder) : the tree and remainder if the entire sequence matches text
            """
            result = []
            for atom in sequence:
                tree, text = parse_atom(atom, text)
                if text is None: return self.Fail
                result.append(tree)
            return result, text

        def parse_atom(atom, text):
            """
            Parameters:
            atom : either a key in grammar or a regular expression
            text : a string

            Returns:
            Fail : if no match can be found
            (tree, remainder) : if a match is found
                tree is the parse tree of the first match found
                remainder is the text that was not matched
            """
            if atom in self.G:  # atom是左部符号，包括NT和T
                for alternative in self.G[atom]:
                    tree, rem = parse_sequence(alternative, text)
                    if rem is not None:  # parse is ok
                        return [atom] + tree, rem
                return self.Fail
            else:  # atom是token，以正则表达式形式；在NT右部直接写的token，以单引号标记，也用正则匹配
                m = re.match(self.tokenizer % atom, text)
                return self.Fail if (not m) else (m.group(1), text[m.end():])

        tree, remainder = parse_atom(start_symbol, text)
        if not remainder:
            return tree
        else:
            raise ValueError('parse failed, text has syntax error')


from regex_interpreter import \
    lit, alt, seq, match as match_core, star, plus, dot, eol, oneof, opt


class RegexVisitor:
    '''
    visitor使用指南：
    1. 不要用空函数体的visit*，没有实现就注释掉，否则该节点不继续遍历，将导致错误
    '''

    def __init__(self, parser):
        self.NT = parser.NT
        self.stack = []
        self.epsilon = lit('')

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def binary_op(self, func):
        rhs = self.pop()
        lhs = self.pop()
        ret = func(lhs, rhs)
        # 优化 当前操作是seq时检查合并lit
        # ('seq', ('seq', ('lit', 'a'), ('lit', 'b')), ('lit', 'c'))
        # => ('lit', 'abc')
        op, *children = ret
        if op == 'seq':
            child0, child1 = children
            op_child0, *children_child0 = child0
            op_child1, *children_child1 = child1
            if op_child0 == 'lit' and op_child1 == 'lit':
                ret = lit(children_child0[0] + children_child1[0])
        self.push(ret)

    def unary_op(self, func):
        operand = self.pop()
        self.push(func(operand))

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

    def visit_re(self, ctx):
        self.visit_children(ctx)
        rhs = self.pop()
        if rhs == self.epsilon:
            pass
        else:
            lhs = self.pop()
            self.push(seq(lhs, rhs))

    def visit_simple_re(self, ctx):
        '''simple_re : basic_re simple_re_;

        '''
        self.visit_children(ctx)
        rhs = self.pop()
        if rhs == self.epsilon:
            pass
        else:
            lhs = self.pop()
            self.push(seq(lhs, rhs))

    def visit_union(self, ctx):
        self.visit_children(ctx)
        self.binary_op(alt)

    def visit_concat(self, ctx):
        self.visit_children(ctx)
        self.binary_op(seq)

    # def visit_basic_re(self,tree): NO NEED
    #     pass
    #
    def visit_star(self, ctx):
        '''star : elementary_re '*';'''
        self.visit_children(ctx)
        self.unary_op(star)

    def visit_plus(self, ctx):
        self.visit_children(ctx)
        self.unary_op(plus)

    def visit_question(self, ctx):
        self.visit_children(ctx)
        self.unary_op(opt)

    # def visit_elementary_re(self,tree):
    #     pass
    #
    # def visit_group(self,tree):
    #     pass
    #
    def visit_any(self, ctx):
        self.push(dot)

    def visit_eos(self, ctx):
        # TODO check $ is used only once, or raise a syntax error
        self.push(eol)

    # def visit_char(self,tree):  NO NEED
    #     pass
    #
    # def visit_set(self,tree):
    #     pass

    def visit_positive_set(self, ctx):
        index = len(self.stack)  # mark current stack index
        self.visit_children(ctx)  # start visit children and 把chars压栈
        chars = self.stack[index:]
        del self.stack[index:]  # TODO check
        operators, operands = zip(*chars)
        assert all(map(lambda op: op == 'lit', operators))  # check all items is char
        self.push(oneof(''.join(operands)))  # join chars to str and 压栈

    # def visit_negative_set(self, ctx):
    #     pass

    # def visit_set_items(self, tree):
    #     pass
    #
    # def visit_set_item(self, tree):
    #     pass
    #
    # def visit_range(self, tree):
    #     pass

    def visit_NonMetaChar(self, tree):
        self.push(lit(tree[0]))

    def visit_MetaChar(self, tree):
        # TODO ???
        pass

    def visit_Epsilon(self, tree):
        self.push(self.epsilon)


parser = ParserGenerator(regex_grammar, whitespace='')  # 禁用空白符，这很重要，regex中不能跳过空白符
visitor = RegexVisitor(parser)


def match(pattern, text):
    '''
    从源文本开头开始匹配，返回最长的匹配，如果不匹配返回None
    :return:

    >>> match('a|b','a')
    'a'

    # >>> match(('star', ('lit', 'a')), 'aaabcd')
    # 'aaa'  # a*
    # >>> match(('alt', ('lit', 'b'), ('lit', 'c')), 'ab')
    # None  # b|c
    # >>> match(('alt', ('lit', 'b'), ('lit', 'a')), 'ab')
    # 'a'  # b|a
    '''
    tree = parser.parse('re', pattern)
    visitor.visit(tree)
    compiled_pattern = visitor.stack.pop()
    return match_core(compiled_pattern, text)


def test():
    p_1 = 'a|b'
    p0 = 'ab'
    p1 = 'a*'
    p2 = 'a+'
    p3 = '(ab)'
    p4 = '.'
    p5 = '$'
    p6 = 'a'
    p7 = '\.'
    p8 = '[a]'
    p9 = '[^a]'


if __name__ == '__main__':
    assert match('a*', 'aaabcd') == 'aaa'
