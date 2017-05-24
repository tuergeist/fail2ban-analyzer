'''
Created on 23.05.2017

@author: cb
'''
import unittest
from datetime import datetime, timedelta
from fail2ban_analyzer.analyzer import convert_time


class Test(unittest.TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_dateconversion(self):
        timestr = '2017-05-23 14:57:44,547'
        ts = datetime(2017, 5, 23, 14, 57, 44)
        conversion_result = convert_time(timestr)
        self.assertEqual(ts, conversion_result)
        self.assertEqual(timedelta(0), ts - conversion_result)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
