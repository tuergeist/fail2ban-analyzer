'''
Created on 23.05.2017

@author: christophbecker
'''
from datetime import datetime, timedelta
import fileinput
import time
from tkinter.constants import LAST
import statistics


def convert_time(timest):
    """Converts a string into a datetime

    timestr -- input time string of '%Y-%m-%d %H:%M:%S'
    """
    fixed_ts = timest.split(',')[0]
    time_tuple = time.strptime(fixed_ts, '%Y-%m-%d %H:%M:%S')
    return datetime.fromtimestamp(time.mktime(time_tuple))


class BanAlyzer():
    BAN = 'ban'
    UNBAN = 'unban'

    def __init__(self):
        self.bandict = {}
        self.banlist = []

    def _check_init_ip(self, ip):
        if ip not in self.bandict:
            self.bandict[ip] = {'ban': [], 'unban': [], 'list': []}

    def _strip_timest_and_ip(self, line):
        line_parts = line.split(' ')
        timest = " ".join(line_parts[0:2])
        banned_ip = line_parts[-1].strip()
        return timest, banned_ip

    def add(self, bantype, timest, ip):
        self._check_init_ip(ip)
        self.bandict[ip][bantype].append(timest)
        self.bandict[ip]['list'].append((bantype, timest))

    def process(self, line):
        if 'fail2ban.actions' in line:
            if ' Ban ' in line:
                timest, banned_ip = self._strip_timest_and_ip(line)
                self.add(self.BAN, timest, banned_ip)
            elif ' Unban ' in line:
                timest, banned_ip = self._strip_timest_and_ip(line)
                self.add(self.UNBAN, timest, banned_ip)

    def report(self):
        stat_bantime = []
        stat_rebantime = []
        for key, value in self.bandict.items():
            
            if len(value['ban']) > 1:
                print("--------- %s -------" % key)
                #print(key, value)
#                 old = None
#                 for timest in value['ban']:
#                     dt = convert_time(timest)
#                     
#                     if old is not None:
#                         print(old, dt, dt - old)
#                     old = dt
                #print(value['list'])
                banstop = None
                ban_unban_list = sorted(value['list'], key=lambda x: x[1])
                for tupl in ban_unban_list:
                    if tupl[0] == self.BAN:
                        banstart = tupl[1]
                        lastbanstop = banstop
                        banstop = None
                    elif tupl[0] == self.UNBAN and banstart is not None:
                        banstop = tupl[1]
                    if banstart is not None and banstop is not None:
                        last = ''
                        bantime = convert_time(banstop) - convert_time(banstart)
                        ts = bantime.total_seconds()
                        stat_bantime.append(ts)
#                         if ts > 1000 or ts < 1:
#                             print(key, value)
#                             print(banstart, banstop)
#                             print(ts, bantime)
                        
                        if lastbanstop is not None: 
                            unbantime = convert_time(banstart) - convert_time(lastbanstop)
                            stat_rebantime.append(unbantime.total_seconds())
                            last = 'after %s being unbanned' % (unbantime)
                            
                        print('Banned %s for %s %s' % (banstart, bantime, last))
                        banstart = None
                        
        print("\n%s IPs processed\n" % len(self.bandict))
        print_stat_details('Ban periods', stat_bantime)
        print('\n')
        print_stat_details('Reban periods', stat_rebantime)
        
        stat_rebantime.sort()
        print(stat_rebantime)
        
def print_stat_details(title, data):
    print('-- '* 10, title, ' --' * (10 - int(len(title)/3)))
    print(get_stat("Min", min, data))
    print(get_stat("Median", statistics.median, data))
    print(get_stat("Mean", statistics.mean, data))
    print(get_stat("Max", max, data))
    print("%25s: %6s" % ("Amount", len(data)))
    
        
def get_stat(title, functionptr, data):
    res = functionptr(data)
    in_secs = timedelta(seconds=res)
    return "%25s: %8.1fs (%17s)" % (title, res, in_secs)
        
        
        
if __name__ == '__main__':
    ba = BanAlyzer()
    with fileinput.input() as f:
        for line in f:
            ba.process(line)
    ba.report()
