from unittest import TestCase

from ZJson import plain_json, loads
from Utils import is_namedtuple_instance
from collections import namedtuple


class A:

    def __init__(self):
        self.a = 0

    def __eq__(self, other):
        return self.__class__==other.__class__ and  self.__dict__ == other.__dict__


class B:

    def __init__(self):
        self.b = A()

    def __eq__(self, other):
        return self.__class__==other.__class__ and self.__dict__ == other.__dict__


class Test(TestCase):
    def test_serialize(self):
        # ---- test primitive types
        assert plain_json(1) == '1'
        assert plain_json(1.1) == '1.1'
        assert plain_json('abc') == '"abc"'  # note 'abc' is wrong, "'abc'" is also wrong
        assert plain_json(True) == 'true'
        assert plain_json(None) == 'null'
        # ---- test collections
        assert plain_json([1, 2, 3]) == '[1,2,3]'
        # assert plain_json({1: 2}) == r'{"1":2}' # cant pass becuz i change my mind to be strict
        # a = plain_json(A())
        # ---- test class objects
        # ---- ---- decodable
        self.assertEqual(plain_json(A()), '{"__class_module__":"Test","__class_name__":"A","__class_dict__":{"a":0}}') # 这里如果你改了本文件名字会出错，理论上应该单独写一个文件（模块）测试，但是，简单化
        b = plain_json(B())
        assert plain_json(
            B()) == '{"__class_module__":"Test","__class_name__":"B","__class_dict__":' \
                    '{"b":{"__class_module__":"Test","__class_name__":"A","__class_dict__":{"a":0}}}}'
        # ---- ---- undecodable
        a = plain_json(A(), decodable=False)
        assert plain_json(A(), decodable=False) == '{"a":0}'
        b = plain_json(B(), decodable=False)
        assert plain_json(B(), decodable=False) == '{"b":{"a":0}}'
        pass

    def test_deserialize(self):
        # ---- test primitive types
        assert loads(plain_json(1)) == 1
        assert loads(plain_json(1.1)) == 1.1
        assert loads(plain_json('abc')) == 'abc'
        assert loads(plain_json(True)) == True
        assert loads(plain_json(None)) == None
        # ---- test collections
        assert loads(plain_json([1, 2, 3])) == [1, 2, 3]
        assert loads(plain_json((1, 2, 3))) == (1, 2, 3)
        assert loads(plain_json({'a': 1})) == {'a': 1}
        assert loads(plain_json({1, 2, 3})) == {1, 2, 3}
        assert loads(plain_json(frozenset([1, 2, 3]))) == frozenset([1, 2, 3])
        assert loads(plain_json([])) == []
        assert loads(plain_json(tuple())) == tuple()
        assert loads(plain_json(set())) == set()
        assert loads(plain_json(frozenset())) == frozenset()
        assert loads(plain_json(dict())) == dict()

        a_cls = namedtuple('A', ['a'])
        a_instance = a_cls(a=1)
        a = loads(plain_json(a_instance))
        assert loads(plain_json(a_instance)) == a_instance

        # ---- test class objects
        a = loads(plain_json(A()))
        assert loads(plain_json(A())) == A()
        assert loads(plain_json(B())) == B()
        pass

    def test_util(self):
        assert not is_namedtuple_instance(1)
        assert not is_namedtuple_instance('some ...')
        assert not is_namedtuple_instance([1, 2, 3])
        assert not is_namedtuple_instance((1, 2, 3))
        assert not is_namedtuple_instance({1: 2})
        a_cls = namedtuple('A', ['a'])
        a_instance = a_cls(a=1)
        assert is_namedtuple_instance(a_instance)
