# coding: utf-8

import ui
import requests
import hashlib
import threading
import time
import console
import os
from ConfigParser import SafeConfigParser

link = '/GarageOpener'
url = 'http://fakeurl.com'
passwd = 'password'#hashlib.md5('test').hexdigest()

@ui.in_background
def settings(sender):
    res = console.login_alert('Host Info','host url and password','http://www.somethings.com','password')
    if res:
        global url
        global passwd
        with open('settings.conf','w') as f:
            f.write('[settings]\n')
            f.write('host=%s\n' % res[0])
            url = res[0]+link
            passwd = hashlib.md5(res[1]).hexdigest()
            f.write('passwd=%s\n' % passwd)
    
    

def update():
    while True:
        try:
            payload = {'password': passwd}
            res = requests.post(url,data=payload)
            if res.headers['garage-state'] == '1':
                btn.background_color = 'green'
            if res.headers['garage-state'] == '0':
                btn.background_color = 'red'
            img.image = ui.Image.from_data(res.content)
        except:
            pass
        


def button_pressed(sender):
    print 'pressed'
    payload= {'password': passwd,'toggle': '1'}
    requests.post(url,data=payload)
    
if not os.path.isfile('settings.conf'):
    print 'Creating Config'
    settings('nil')
else:
    print 'config Found'
    config = SafeConfigParser()
    config.read('settings.conf')
    url = config.get('settings','host')+link
    passwd = config.get('settings','passwd')
    
print url
print passwd
view = ui.load_view()
view.present('full_screen')
img = view['imageview1']
btn = view['button1']
view['button1'].action = button_pressed
view['button2'].action = settings
t = threading.Thread(target=update)
t.start()

