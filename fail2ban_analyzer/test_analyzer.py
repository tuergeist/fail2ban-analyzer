'''
Created on 23.05.2017

@author: cb
'''
import unittest
from analyzer import convert_time
import time
from time import mktime
from datetime import datetime

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_dateconversion(self):
        timestr = '2017-05-23 14:57:44,547'
        ts = datetime(2017, 5, 23, 14, 57, 44)
        self.assertEqual(ts, convert_time(timestr))
        dt2 = convert_time(timestr)
        print(ts, ts-dt2)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()