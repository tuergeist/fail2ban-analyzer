'''
Created on 23.05.2017

@author: christophbecker
'''
from datetime import datetime
import fileinput
import time


def convert_time(timest):
    """Converts a string into a datetime
    
    timestr -- input time string of '%Y-%m-%d %H:%M:%S'
    """
    fixed_ts = timest.split(',')[0]
    time_tuple = time.strptime(fixed_ts, '%Y-%m-%d %H:%M:%S')
    return datetime.fromtimestamp(time.mktime(time_tuple))


class BanAlyzer():
    def __init__(self):
        self.bandict = {}

    def _check_init_ip(self, ip):
        if ip not in self.bandict:
            self.bandict[ip] = {'ban': [], 'unban': []}

    def _strip_timest_and_ip(self, line):
        line_parts = line.split(' ')
        timest = " ".join(line_parts[0:2])
        banned_ip = line_parts[-1].strip()
        return timest, banned_ip

    def add_ban(self, timest, ip):
        self._check_init_ip(ip)
        self.bandict[ip]['ban'].append(timest)

    def add_unban(self, timest, ip):
        self._check_init_ip(ip)
        self.bandict[ip]['unban'].append(timest)

    def process(self, line):
        if 'fail2ban.actions' in line:
            if ' Ban ' in line:
                
                timest, banned_ip = self._strip_timest_and_ip(line)
                self.add_ban(timest, banned_ip)
            elif ' Unban ' in line:
                line_parts = line.split(' ')
                timest = " ".join(line_parts[0:2])
                banned_ip = line_parts[-1].strip()
                self.add_unban(timest, banned_ip)
            
    def report(self):
        for key, value in self.bandict.items():
            if len(value['ban']) > 1:
                print(key, value)
                old = None
                for timest in value['ban']:
                    dt = convert_time(timest)
                    if old is not None:
                        print(old, dt, dt - old)
                    old = dt
            
if __name__ == '__main__':
    ba = BanAlyzer()
    with fileinput.input() as f:
        for line in f:
            ba.process(line)
    ba.report()
