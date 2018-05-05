import unittest, time

import EasyRule
from EasyRule import BusEvent, ItemRegistry, Items

class test_BusEvent(unittest.TestCase):
    def test_postUpdateString(self):
        BusEvent.postUpdate('TestString', 'asdf')
        time.sleep(0.1)
        a = ItemRegistry.getItem('TestString')
        print('-----')
        print('issubclass: {}'.format( issubclass(EasyRule.replacements.items.StringItem, EasyRule.replacements.items._BaseItem)))
        print('isinstance: {}'.format( isinstance(a, Items.StringItem)))
        print('      type: {}'.format( type(a)))
        print('     type1: {}'.format( type(EasyRule.replacements.items.StringItem)))
        print('     type2: {}'.format( type(Items.StringItem)))
        self.assertIsInstance(a, EasyRule.replacements.items.StringItem)
        self.assertIsInstance(a, Items.StringItem)
        self.assertEqual(a.type, "String", a.type)
        self.assertEqual(a.state, "asdf", a.state)

    # def test_postUpdateNumber(self):
    #     BusEvent.postUpdate('TestNumber', 0)
    #
    # def test_postUpdateContact(self):
    #     BusEvent.postUpdate('TestContact', 'CLOSED')
    #
    # def test_postUpdateSwitch(self):
    #     BusEvent.postUpdate('TestSwitch', "ON")
    #
    # def test_postUpdateDateTime(self):
    #     BusEvent.postUpdate('TestDateTime')
    #
    # def test_postUpdateGroup(self):
    #     BusEvent.postUpdate('TestGroup')
    #
    # def test_postUpdateColor(self):
    #     BusEvent.postUpdate('TestColor')
    #
    # def test_postUpdateLocation(self):
    #     BusEvent.postUpdate('TestLocation')
    #
    # def test_postUpdatePlayer(self):
    #     BusEvent.postUpdate('TestPlayer')
