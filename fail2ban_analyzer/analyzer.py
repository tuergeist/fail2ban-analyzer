'''
Created on 23.05.2017

@author: christophbecker
'''
import fileinput


class BanAlyzer():

    def __init__(self):
        self.bandict = {}

    def add_ban(self, timest, ip):
        if ip not in self.bandict:
            self.bandict[ip] = {'ban':[], 'unban':[]}
        self.bandict[ip]['ban'].append(timest)

    def add_unban(self, timest, ip):
        if ip not in self.bandict:
            self.bandict[ip] = {'ban':[], 'unban':[]}
        self.bandict[ip]['unban'].append(timest)

    def process(self, line):
        if 'fail2ban.actions' in line:
            #print(line[:-1])
            if ' Ban ' in line:
                line_parts = line.split(' ')
                timest = " ".join(line_parts[0:2])
                banned_ip = line_parts[-1].strip()
                self.add_ban(timest, banned_ip)
            elif ' Unban ' in line:
                line_parts = line.split(' ')
                timest = " ".join(line_parts[0:2])
                banned_ip = line_parts[-1].strip()
                self.add_unban(timest, banned_ip)
            
    def report(self):
        for key, value in self.bandict.items():
            print(key, value)
            
if __name__ == '__main__':
    ba = BanAlyzer()
    with fileinput.input() as f:
        for line in f:
            ba.process(line)
    ba.report()
