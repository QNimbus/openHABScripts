import unittest, time
from EasyRule import ItemRegistry
from EasyRule.Items import NumberItem

from EasyModule import Counter

item = ItemRegistry.getItem('TestNumber')
#assert isinstance(item, NumberItem)

class Basic(unittest.TestCase):

    def test_constructor1(self):
        a = Counter('TestNumber')

        item = ItemRegistry.getItem('TestNumber')
        self.assertIsInstance(item, Counter)
        ItemRegistry.RemoveCustomItem('TestNumber')

    def test_Increase(self):
        a = Counter('TestNumber')
        ItemRegistry.RemoveCustomItem('TestNumber')
        a.Initialize()

        self.assertEqual(a.val, 0)
        a.Increase(1)
        time.sleep(0.1)
        self.assertEqual(item.state, 1)
        a.Increase(5)
        time.sleep(0.1)
        self.assertEqual(item.state, 6)
        a.Decrease(6)
        time.sleep(0.1)
        self.assertEqual(item.state, 0)

    def test_min(self):

        a = Counter('TestNumber', min=10)
        ItemRegistry.RemoveCustomItem('TestNumber')
        a.Initialize()

        self.assertEqual(a.val, 10)
        a.Increase(1)
        time.sleep(0.1)
        self.assertEqual(item.state, 11)
        a.Decrease(6)
        time.sleep(0.1)
        self.assertEqual(item.state, 10)

    def test_max(self):

        a = Counter('TestNumber', max=10, start=999)
        ItemRegistry.RemoveCustomItem('TestNumber')
        a.Initialize()

        self.assertEqual(a.val, 10)
        a.Decrease(1)
        time.sleep(0.1)
        self.assertEqual(item.state, 9)
        a.Increase(6)
        time.sleep(0.1)
        self.assertEqual(item.state, 10)

