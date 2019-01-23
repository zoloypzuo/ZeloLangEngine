from unittest import TestCase

from lesson3_regex_other_languages_and_interpreters.regex_engine import match


class TestRegexEngine(TestCase):
    def setUp(self):
        self.match_equal = lambda pattern, text, ret: \
            self.assertEqual(match(pattern, text), ret)

    def test_match(self):
        self.assertEqual(match('a|b', 'a'), 'a')
        self.assertEqual(match('a|b', 'b'), 'b')
        self.assertEqual(match('ab', 'ab'), 'ab')
        self.assertEqual(match('a*', 'aaabcd'), 'aaa')
        self.assertEqual(match('b|c', 'ab'), None)
        self.assertEqual(match('b|a', 'ab'), 'a')

        self.assertEqual(match('abc', 'abcdef'), 'abc')
        self.assertEqual(match('hi there', 'hi there nice to meet you'), 'hi there')
        self.assertEqual(match('dog|cat', 'dog and cat'), 'dog')
        self.assertEqual(match('.', 'am i missing something?'), 'a')
        self.assertEqual(match('.', ''), None)  # dot does not match epsilon
        self.assertEqual(match('[a]', 'aabc123'), 'a')
        self.assertEqual(match('[abc]', 'babc123'), 'b')
        self.assertEqual(match('[abc]', 'dabc123'), None)
        self.assertEqual(match('$', ''), '')
        self.assertEqual(match('$', 'not end of line'), None)
        self.assertEqual(match('(hey)*', 'heyheyyoyo'), 'heyhey')

    def test_lit(self):
        self.assertEqual(match('abc', 'abc'), 'abc')

    def test_seq(self):
        self.assertEqual(match('ab', 'ab'), 'ab')

    def test_alt(self):
        self.assertEqual(match('a|b', 'a'), 'a')

    def test_star(self):
        self.assertEqual(match('a*', 'a'), 'a')

    def test_plus(self):
        self.assertEqual(match('c+', 'c'), 'c')

    def test_opt(self):
        self.assertEqual(match('x?', 'x'), 'x')
        self.assertEqual(match('x?', ''), '')

    def test_oneof(self):
        self.assertEqual(match('[abc]', 'a'), 'a')
        self.assertEqual(match('[abc]', 'b'), 'b')
