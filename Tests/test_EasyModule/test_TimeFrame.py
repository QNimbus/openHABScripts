import unittest, datetime
import EasyModule
from EasyModule import TimeFrame

def p(x):
    print(x)

class Basic(unittest.TestCase):


    def test_day(self):
        t = TimeFrame('mon,8:30:00-9:31')
        self.assertEqual(t.weekdays[0], 0)
        self.assertEqual(t.time_start[0], 8)
        self.assertEqual(t.time_start[1], 30)
        self.assertEqual(t.time_start[2], 0)
        self.assertEqual(t.time_stop[0], 9)
        self.assertEqual(t.time_stop[1], 31)
        self.assertEqual(t.time_stop[2], 0)

    def test_days(self):
        t = TimeFrame('mon,tue,wed,8:6 - 9:30:12')
        self.assertEqual(t.weekdays, [0,1,2])
        self.assertEqual(t.time_start[0], 8)
        self.assertEqual(t.time_start[1], 6)
        self.assertEqual(t.time_start[2], 0)
        self.assertEqual(t.time_stop[0], 9)
        self.assertEqual(t.time_stop[1], 30)
        self.assertEqual(t.time_stop[2], 12)

    def test_weekdays(self):
        t = TimeFrame('weekdays,8:30:00-9:30:00')
        self.assertEqual(t.weekdays, [0,1,2,3,4])

    def test_weekends(self):
        t = TimeFrame('weekends,8:30:00-9:30:00')
        self.assertEqual(t.weekdays, [5,6])
    def test_all(self):
        t = TimeFrame('8:30:00-9:30:00')
        self.assertEqual(t.weekdays, [0,1,2,3,4,5,6])
    def test_none(self):
        t = TimeFrame('12:30-13:50')
        self.assertEqual(t.weekdays, [0, 1, 2, 3, 4, 5, 6])
        self.assertEqual(t.time_start[0], 12)
        self.assertEqual(t.time_start[1], 30)
        self.assertEqual(t.time_start[2], 0)
        self.assertEqual(t.time_stop[0], 13)
        self.assertEqual(t.time_stop[1], 50)
        self.assertEqual(t.time_stop[2], 0)


    def test_invalid_day(self):
        self.assertRaises(ValueError, lambda: TimeFrame('asdf,8:30:00-9:30:00'))

    def test_invalid_hour(self):
        self.assertRaises(ValueError, lambda: TimeFrame('25:30:00-9:30:00'))
    def test_invalid_min(self):
        self.assertRaises(ValueError, lambda: TimeFrame('13:60:00'))
    def test_invalid_sec(self):
        self.assertRaises(ValueError, lambda: TimeFrame('13:59:60'))
    def test_invalid_sec(self):
        self.assertRaises(ValueError, lambda: TimeFrame('13:59:59-13:59:59'))

    def test_mi(self):
        print("")
        t = TimeFrame('Mi,13:0:59-13:59:59', p)
        EasyModule.timeframe._TIME_FUNC = lambda : datetime.datetime(2018, 02, 07, 13, 30)
        self.assertEqual(t.is_now(), True)
        EasyModule.timeframe._TIME_FUNC = lambda : datetime.datetime(2018, 02, 14, 13, 30)
        self.assertEqual(t.is_now(), True)
        EasyModule.timeframe._TIME_FUNC = lambda : datetime.datetime(2018, 02, 8, 13, 30)
        self.assertEqual(t.is_now(), False)

    def test_do(self):
        t = TimeFrame('Mi,13:0:59-13:59:59')
        EasyModule.timeframe._TIME_FUNC = lambda : datetime.datetime(2018, 02, 8, 13, 30)
        t = TimeFrame('Mi,Do,13:00:59-13:59:59', p)
        EasyModule.timeframe._TIME_FUNC = lambda : datetime.datetime(2018, 02, 8, 13, 30)
        self.assertEqual(t.is_now(), True)
        EasyModule.timeframe._TIME_FUNC = lambda : datetime.datetime(2018, 02, 15, 13, 30)
        self.assertEqual(t.is_now(), True)
        EasyModule.timeframe._TIME_FUNC = lambda : datetime.datetime(2018, 02, 14, 13, 30)
        self.assertEqual(t.is_now(), True)
        EasyModule.timeframe._TIME_FUNC = lambda : datetime.datetime(2018, 02, 9, 13, 30)
        self.assertEqual(t.is_now(), False)

    def test_holiday(self):
        t = TimeFrame('So,13:00:59-13:59:59', sunday_checks_holiday=True)
        EasyModule.timeframe._TIME_FUNC = lambda : datetime.datetime(2018, 12, 24, 13, 30)
        self.assertEqual(t.is_now(), True)
        t = TimeFrame('So,13:00:59-13:59:59', sunday_checks_holiday=False)
        EasyModule.timeframe._TIME_FUNC = lambda : datetime.datetime(2018, 12, 24, 13, 30)
        self.assertEqual(t.is_now(), False)

if __name__ == '__main__':
    unittest.main()
