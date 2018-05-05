import unittest, time
from EasyRule import ItemRegistry

from EasyModule import FiFo


class Basic(unittest.TestCase):

    def test_constructor1(self):
        a = FiFo('TestNumber', 10)

        item = ItemRegistry.getItem('TestNumber')
        self.assertIsInstance(item, FiFo)
        ItemRegistry.RemoveCustomItem('TestNumber')

    def test_push_int(self):

        a = FiFo('TestNumber', 10)
        ItemRegistry.RemoveCustomItem('TestNumber')

        a.push(0)
        time.sleep(0.1)
        self.assertEqual(ItemRegistry.getItem('TestNumber0').state, 0)

        a.push(1)
        time.sleep(0.1)
        self.assertEqual(ItemRegistry.getItem('TestNumber0').state, 1)
        self.assertEqual(ItemRegistry.getItem('TestNumber1').state, 0)

        a.push(3)
        time.sleep(0.1)
        self.assertEqual(ItemRegistry.getItem('TestNumber0').state, 3)
        self.assertEqual(ItemRegistry.getItem('TestNumber1').state, 1)
        self.assertEqual(ItemRegistry.getItem('TestNumber2').state, 0)

        a.push(5)
        time.sleep(0.1)
        self.assertEqual(ItemRegistry.getItem('TestNumber0').state, 5)
        self.assertEqual(ItemRegistry.getItem('TestNumber1').state, 3)
        self.assertEqual(ItemRegistry.getItem('TestNumber2').state, 1)
        self.assertEqual(ItemRegistry.getItem('TestNumber3').state, 0)

    def test_push_str(self):

        a = FiFo('TestString', 10)
        ItemRegistry.RemoveCustomItem('TestString')

        a.push('Leberwurst')
        time.sleep(0.1)
        self.assertEqual(ItemRegistry.getItem('TestString0').state, 'Leberwurst')

        a.push('Schinkenwurst')
        time.sleep(0.1)
        self.assertEqual(ItemRegistry.getItem('TestString0').state, 'Schinkenwurst')
        self.assertEqual(ItemRegistry.getItem('TestString1').state, 'Leberwurst')

        a.push('Streichwurst')
        time.sleep(0.1)
        self.assertEqual(ItemRegistry.getItem('TestString0').state, 'Streichwurst')
        self.assertEqual(ItemRegistry.getItem('TestString1').state, 'Schinkenwurst')
        self.assertEqual(ItemRegistry.getItem('TestString2').state, 'Leberwurst')

        a.push('Erdberkaese')
        time.sleep(0.1)
        self.assertEqual(ItemRegistry.getItem('TestString0').state, 'Erdberkaese')
        self.assertEqual(ItemRegistry.getItem('TestString1').state, 'Streichwurst')
        self.assertEqual(ItemRegistry.getItem('TestString2').state, 'Schinkenwurst')
        self.assertEqual(ItemRegistry.getItem('TestString3').state, 'Leberwurst')

    def test_iter(self):

        a = FiFo('TestNumber', 10)
        for element in a:
            print(element)

    def test_push_11int(self):

        a = FiFo('TestNumber', 10)
        ItemRegistry.RemoveCustomItem('TestNumber')
        a.push(0)
        a.push(9)
        a.push(8)
        a.push(7)
        a.push(6)
        a.push(5)
        a.push(4)
        a.push(3)
        a.push(2)
        a.push(1)
        a.push(0)

        self.assertEqual(a[0], 0)
        self.assertEqual(a[1], 1)
        self.assertEqual(a[2], 2)
        self.assertEqual(a[3], 3)
        self.assertEqual(a[4], 4)
        self.assertEqual(a[5], 5)
        self.assertEqual(a[6], 6)
        self.assertEqual(a[7], 7)
        self.assertEqual(a[8], 8)
        self.assertEqual(a[9], 9)

    def test_set(self):
        a = FiFo('TestString', 10)
        ItemRegistry.RemoveCustomItem('TestString')

        SET_STR = 'asfdasdfasf'
        a[7] = SET_STR

        time.sleep(0.1)
        self.assertEqual(ItemRegistry.getItem('TestString7').state, SET_STR)
