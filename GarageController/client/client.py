# coding: utf-8

import ui
import requests
import hashlib
import threading
import time
import console
import os
from ConfigParser import SafeConfigParser

#create .pyui if needed
if not os.path.isfile('client.pyui'):
    str = '[{"class":"View","attributes":{"background_color":"RGBA(1.000000,1.000000,1.000000,1.000000)","tint_color":"RGBA(0.000000,0.478000,1.000000,1.000000)","enabled":true,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","flex":""},"frame":"{{0, 0}, {750, 1024}}","nodes":[{"class":"ImageView","attributes":{"name":"imageview1","uuid":"F4E5E73B-4022-429D-89B9-DEF503B09196","enabled":true,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","flex":"W"},"frame":"{{15.5, 75.5}, {716.5, 548}}","nodes":[]},{"class":"Button","attributes":{"font_size":50,"enabled":true,"tint_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_bold":false,"name":"button1","flex":"","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","corner_radius":52,"uuid":"516EEC52-B2B7-4444-8992-EEF1BE4946A6","background_color":"RGBA(0.834906,0.834906,0.834906,1.000000)","title":"Toggle"},"frame":"{{28.5, 668}, {689.5, 210.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":15,"enabled":true,"flex":"LB","font_bold":false,"name":"button2","uuid":"41684558-0FF5-4648-ABF5-B5142328D0E8","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","image_name":"ionicons-ios7-cog-32","title":""},"frame":"{{670, 6}, {80, 32}}","nodes":[]},{"class":"Label","attributes":{"font_size":26,"enabled":true,"text":"Garage Monitor v1.0","flex":"W","name":"label1","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"center","uuid":"46F932F3-525C-49A3-BCB6-5CD50378608A"},"frame":"{{207, 6}, {334.5, 32}}","nodes":[]}]}]'
    with open('client.pyui','w') as f:
        f.write(str)
        

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
        time.sleep(1)
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

