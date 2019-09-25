from functools import partial
from unittest import TestCase

from ZJson import parse, ZJsonValueError


class TestParse(TestCase):
    def test_basic(self):
        # test the 3 literal types in json
        assert None == parse('null')
        assert True == parse('true')
        assert False == parse('false')

        # test the 2 simple types in json
        assert 1 == parse('1')  # 1 == 1.0 in python
        assert 1.1 == parse('1.1')
        assert 'abc' == parse('"abc"')  # note that 'abc' is wrong, "'abc'" is also wrong

        # test the 2 composite types in json
        assert [1, 2, 3] == parse('[1,2,3]')
        assert {'a': 1} == parse(r'{"a": 1}')  # {'a': 1} == {'a': 1} is True

    def test_number(self):
        ''''''
        # TODO numbers: ...

    def test_string(self):
        ''''''
        # TODO strings: escape utf-8

    def test_error(self):
        ''''''
        # TODO more test to error
        assert_value_error = partial(self.assertRaises, ZJsonValueError, parse)
        assert_value_error('ull')
        assert_value_error('tre')

        assert_value_error('')
