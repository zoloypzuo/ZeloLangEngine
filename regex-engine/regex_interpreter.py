# class RegexInterpreter:  # 本来试图使用class，但是不太好，是多余的

# region 用于构造pattern的辅助函数

dot = ('dot',)
eol = ('eol',)  # eol是$


def oneof(chars):
    return ('oneof', tuple(chars))


def opt(x):
    return alt(lit(''), x)  # opt(x) means that x is optional


def plus(x):
    return seq(x, star(x))


def star(x):
    return ('star', x)
    # return opt(plus(x))  # 这是错误的写法，构造tuple时就调用死循环了


def alt(x, y):
    return ('alt', x, y)


def seq(x, y):
    return ('seq', x, y)


def lit(string):
    return ('lit', string)


# endregion


def match_set(pattern, text):
    '''从开头开始匹配，返回剩余的子串的集合'''
    # region 解码pattern
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    op = pattern[0]
    # endregion
    null = set()  # null set，直接写{}是错误的，会被认为是空字典

    if 'lit' == op:
        # match(lit('abc'), 'abcde') => {'de'}
        # 注意任何串都能匹配空串开头，返回本身
        return {text[len(x):]} if text.startswith(x) else null
    elif 'seq' == op:
        return set(t2 for t1 in match_set(x, text) for t2 in match_set(y, t1))  # 先match x，再match y
    elif 'alt' == op:
        return match_set(x, text) | match_set(y, text)  # match x 和 match y 的并集
    elif 'dot' == op:
        # dot不匹配空串
        return {text[1:]} if text else null  # 跳过一格即可
    elif 'oneof' == op:
        return {text[1:]} if text.startswith(tuple(x)) else null  # 匹配前缀则跳过一格即可
    elif 'eol' == op:
        # eol是$
        return {''} if text == '' else null  # 如果是空串则匹配
    elif 'star' == op:
        # a* iff epsilon|aa*，a的分支必须消耗掉至少一个字符
        return ({text} |  # start可以直接返回本身
                set(t2
                    for t1 in match_set(x, text) if t1 != text  # 匹配掉一个x，在剩余串中继续匹配pattern，
                    # 这一步过滤掉返回本身的串，因为这是上一个情况已经讨论的
                    # 而且这是必须的，总之，这一步必须消耗掉至少一个字符才行
                    for t2 in match_set(pattern, t1)))
    else:
        raise ValueError('pattern syntax error: %s' % pattern)


def match(pattern, text):
    '''
    从源文本开头开始匹配，返回最长的匹配，如果不匹配返回None
    :param pattern: 嵌套的tuple形式的AST
    :param text:
    :return:

    >>> match(('star', ('lit', 'a')), 'aaabcd')
    'aaa'  # a*
    >>> match(('alt', ('lit', 'b'), ('lit', 'c')), 'ab')
    None  # b|c
    >>> match(('alt', ('lit', 'b'), ('lit', 'a')), 'ab')
    'a'  # b|a
    '''
    remainders = match_set(pattern, text)  # 得到匹配后剩余的子串的集合
    if remainders:
        shortest = min(remainders, key=len)  # 取最短的那个，意味着匹配的是最长的
        return text[:len(text) - len(shortest)]  # 返回匹配的文本部分
    else:
        return None


def search(pattern, text):
    '''
    返回最长最早的匹配或None

    >>> search(('lit', ''), '')
    ''  # ''
    >>> search(('alt', ('lit', 'b'), ('lit', 'c')), 'ab')
    'b'  # b|c
    '''
    # length = len(text) or 1  # 短路表达式，用到0判断为False
    length = len(text) if len(text) > 0 else 1  # 更加长，但更加稳定
    # region 比如 search('ab', 'bbbba')，则先调用match('bbbba')，再是'bbba'，'bba'，'ba'
    for i in range(length):
        m = match(pattern, text[i:])
        if m is not None:
            return m
    return None
    # endregion
