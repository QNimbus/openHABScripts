import unittest, datetime
from EasyModule.core import Subscribable

class NotificationSender(Subscribable):
    def notification(self, obj, value):
        pass

class TestClass(Subscribable):

    def __init__(self):
        super(TestClass, self).__init__()
        self.last_received_notification1 = None
        self.last_received_notification = None
        self.last_sent_notification = None
        self._set_notification_target(NotificationSender, lambda x,y : self.notification1(x,y))

    def notify(self, value):
        self.last_sent_notification = (self, value)
        super(TestClass, self).notify(value)

    def notification(self, obj, value):
        self.last_received_notification = (obj, value)
    def notification1(self, obj, value):
        self.last_received_notification1 = (obj, value)

class Basic(unittest.TestCase):

    def test_constructor_abc(self):
        class TestA(Subscribable):
            pass
        self.assertRaises(TypeError, lambda : TestA())

    def test_constructor(self):
        a = TestClass()

    def test_func(self):
        a = TestClass()
        self.assertRaises( AssertionError, lambda :  a._set_notification_target(NotificationSender, lambda x : None))
        self.assertRaises( AssertionError, lambda :  a._set_notification_target(NotificationSender, lambda x,y,z : None))


class Functional(unittest.TestCase):
    def test_notification(self):
        a = TestClass()
        b = TestClass()

        a.subscribe(b)
        b.notify('Leberwurst')

        self.assertEqual(a.last_received_notification[0], b)
        self.assertEqual(a.last_received_notification[1], 'Leberwurst')
        self.assertEqual(a.last_received_notification[0], b.last_sent_notification[0])
        self.assertEqual(a.last_received_notification[1], b.last_sent_notification[1])
        b.notify('Leberwurst1')
        self.assertEqual(a.last_received_notification[0], b)
        self.assertEqual(a.last_received_notification[1], 'Leberwurst1')
        self.assertEqual(a.last_received_notification[0], b.last_sent_notification[0])
        self.assertEqual(a.last_received_notification[1], b.last_sent_notification[1])

    def test_custom_notification(self):
        a = TestClass()
        b = NotificationSender()

        a.subscribe(b)
        b.notify('Kaese')
        self.assertEqual(a.last_received_notification, None)
        self.assertEqual(a.last_received_notification1[0], b)
        self.assertEqual(a.last_received_notification1[1], 'Kaese')
        b.notify('Wurst')
        self.assertEqual(a.last_received_notification, None)
        self.assertEqual(a.last_received_notification1[0], b)
        self.assertEqual(a.last_received_notification1[1], 'Wurst')


if __name__ == '__main__':
    unittest.main()