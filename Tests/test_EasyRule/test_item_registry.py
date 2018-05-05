import unittest
from EasyRule import ItemRegistry


class Basic(unittest.TestCase):

    def test_ItemExists(self):
        self.assertEqual(ItemRegistry.ItemExists('TestString'), True)
        self.assertEqual(ItemRegistry.ItemExists('zzzzzzzzzzzzzzzz'), False)

    def test_getItemString(self):
        self.assertEqual(ItemRegistry.getItem('TestString').type, 'String')

    def test_getItemNumber(self):
        self.assertEqual(ItemRegistry.getItem('TestNumber').type, 'Number')

    def test_getItemContact(self):
        self.assertEqual(ItemRegistry.getItem('TestContact').type, 'Contact')

    def test_getItemSwitch(self):
        self.assertEqual(ItemRegistry.getItem('TestSwitch').type, 'Switch')

    def test_getItemDateTime(self):
        self.assertEqual(ItemRegistry.getItem('TestDateTime').type, 'DateTime')

    def test_getItemGroup(self):
        self.assertEqual(ItemRegistry.getItem('TestGroup').type, 'Group')

    def test_getItemColor(self):
        self.assertEqual(ItemRegistry.getItem('TestColor').type, 'Color')

    def test_getItemLocation(self):
        self.assertEqual(ItemRegistry.getItem('TestLocation').type, 'Location')

    def test_getItemPlayer(self):
        self.assertEqual(ItemRegistry.getItem('TestPlayer').type, 'Player')



    def test_getItems(self):
        self.assertEqual(len(ItemRegistry.getItems('TestString\d+')), 10)
        self.assertEqual(len(ItemRegistry.getItems('TestString')), 1)



class Custom(unittest.TestCase):
    def setUp(self):
        self.__name = 'adsfadsfr32z4536563564563456'
        ItemRegistry.AddCustomItem(self.__name, {'val' : 9999})

    def test_AddCustomItem(self):

        CUSTOM_NAME = 'afdsvdadsffadsfadsf'
        l = ['TestCase', 'asdf']

        ItemRegistry.AddCustomItem(CUSTOM_NAME, l)
        a = ItemRegistry.getItem(CUSTOM_NAME)

        self.assertIsInstance(a, list)
        for a,b in zip(l, a):
            self.assertEquals(a,b)

    def test_AddCustomItem1(self):
        a = ItemRegistry.getItem(self.__name)
        self.assertEqual(a['val'], 9999)