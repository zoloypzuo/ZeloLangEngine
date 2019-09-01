# regex_engine
一个用python写的正则引擎

这里实现的正则的功能比较弱，关注点在于简洁优美的实现。

嗯，算是个玩具。

用例如下：

```Python
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
```
