from database_management import *
import sys
import os

if len(sys.argv) <= 3:
    cmd = str(sys.argv[1])
    ip = str(sys.argv[2])
else:
    ip = sys.argv[-1]
    cmd = ' '.join(sys.argv[1:(len(sys.argv)-1)])

issue_cmd(cmd,ip)

file = open('data/{}.txt'.format(ip),'a')
file.write('> Command Sent...'+'\n')
file.close()