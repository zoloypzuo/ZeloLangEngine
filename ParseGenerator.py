# BUG cpp_decl_grammar中，cpp语句用分号结尾，但是逻辑中分号被当作语法中一行的结尾，会直接截断
# 出于短平快的考虑，我直接从源文本中去除了分号

import re


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
