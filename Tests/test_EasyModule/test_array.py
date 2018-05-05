import unittest, EasyRule, time

from EasyModule import Array



class Basic(unittest.TestCase):

    def tearDown(self):
        EasyRule.ItemRegistry.RemoveCustomItem('TestString')

    def test_constructor(self):
        a = Array('TestString', 10)

    def test_len(self):
        a = Array('TestString', 10)
        self.assertEqual(len(a), 10)
        a = Array('TestString', 3)
        self.assertEqual(len(a), 3)

    def test_set(self):
        a = Array('TestString', 10)
        a[0] = 'Leberkaese'
        time.sleep(0.1)
        self.assertEqual(a[0], 'Leberkaese')

    def test_iter(self):
        a = Array('TestString', 10)
        a[0] = 'test'
        a[1] = 'zzzzzz'
        for i, val in enumerate(a):
            print( '{} : {} {}'.format(i, val, type(val)))

    def test_exception(self):
        a = Array('TestString', 10)

        self.assertRaises( IndexError, lambda : a[10])
        self.assertRaises( NotImplementedError, lambda : a.insert(0, 'asdf'))

        def __del():
            del a[2]
        self.assertRaises( NotImplementedError, __del)


if __name__ == '__main__':
    unittest.main()