'''
Created on 23.05.2017

@author: cb
'''
import unittest
from analyzer import convert_time
import time
import datetime
from time import mktime

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_dateconversion(self):
        timestr = '2017-05-23 14:57:44,547'
        ts = datetime.datetime(2017, 5, 23, 14, 57, 44).timetuple()
        self.assertEqual(ts, convert_time(timestr))
        print(datetime)
        print(dir(datetime))
        dt = datetime.datetime.fromtimestamp(mktime(ts))
        print(dt)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()