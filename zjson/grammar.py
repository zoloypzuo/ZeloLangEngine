import re


def split(text, sep=None, maxsplit=-1):
    "Like str.split applied to text, but strips whitespace from each piece."
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]


def parse(start_symbol, text, grammar):
    """Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'

    See: http://en.wikipedia.org/wiki/Parsing_expression_grammar
    """

    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, remainder):
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
            ret = parse_atom(atom, remainder)
            if ret is Fail: return Fail
            tree, remainder = ret
            result.append(tree)
        return result, remainder

    # @memo # 这个memo几乎没用
    def parse_atom(atom, remainder):
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
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                ret = parse_sequence(alternative, remainder)
                if ret is not Fail:
                    tree, rem = ret
                    return [atom] + tree, rem
            return Fail
        else:  # Terminal: match characters against start of text
            match_obj = re.match(tokenizer % atom, remainder)
            return Fail if (not match_obj) else (match_obj.group(1), remainder[match_obj.end():])

    return parse_atom(start_symbol, text)


Fail = (None, None)

G = {' ': '\\s*',
     'Exp': (['Term', '[+-]', 'Exp'], ['Term']),
     'Exps': (['Exp', '[,]', 'Exps'], ['Exp']),
     'Factor': (['Funccall'], ['Var'], ['Num'], ['[(]', 'Exp', '[)]']),
     'Funccall': (['Var', '[(]', 'Exps', '[)]'],),
     'Num': (['[-+]?[0-9]+([.][0-9]*)?'],),
     'Term': (['Factor', '[*/]', 'Term'], ['Factor']),
     'Var': (['[a-zA-Z_]\\w*'],)}

if __name__ == '__main__':
    print(parse('Exp', '3*x + b', G))
