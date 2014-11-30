from ConfigParser import SafeConfigParser
from datetime import datetime
import smtplib
import requests
import threading

from bottle import route, run, request, HTTPResponse
#from nanpy import 

config = SafeConfigParser()
config.read('config.conf')

#Try to load GPIO
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    global sensor_pin 
    sensor_pin= int(config.get('rpi','sensor'))
    print 'Pin Loaded'
    print sensor_pin
    GPIO.setup(sensor_pin,GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO_installed = True
except Exception, e:
    print e
    print 'RPi.GPIO not installed'
    
#garage_state= False
toggle_time=0
garage_state = 'setup'
GARAGE_OPEN = 1
GARAGE_CLOSED = 0

def snapshot():
    
    url = 'http://'+config.get('camera','server')+':'+config.get('camera','port')+'/snapshot.cgi'
    payload = {'user': config.get('camera','user'),'pwd': config.get('camera','passwd')}
    res = requests.get(url,params=payload)
    return res.content
    #return res.content

def initmail():
  #global server
  server = smtplib.SMTP( config.get('mail','smtp'), config.get('mail','port') )
  if config.get('mail','tls') == 'y':
      server.starttls()
  try:
    server.login( config.get('mail','user'), config.get('mail', 'passwd') )
  except:
    return False
    
  return server
  
def sendEmail(state):
  server = initmail()
  if server:
    msg = 'Not Set'
    #msg = 'Wake up Sr. Charles Trowbridge! It is your last day!' #+ make_name()
    t = datetime.now().strftime('%H:%M:%S')
    if state == GARAGE_OPEN:
        msg = '\nGarage Open (%s)' % t
    if state == GARAGE_CLOSED:
        msg = '\nGarage Closed (%s)' % t
        
    try:
        print msg + msg
        server.sendmail( config.get('mail','send_as'), config.get('mail','recipients'), msg )
    except Exception, e:# smtplib.SMTPRecipientsRefused, e:
        print e
    finally:
        server.close()
      
def toggle_garage():
    t = datetime.now().strftime('%H:%M:%S')
    print t
    
def garage_status():
    global garage_state
    if GPIO_installed:
        while True:
            if garage_state == 'setup':
                garage_state = GPIO.input(int(config.get('rpi','sensor')))
                sendEmail(garage_state)
            
            if garage_state != GPIO.input(int(config.get('rpi','sensor'))):
                #sendEmail(garage_state)
                garage_state = GPIO.input(int(config.get('rpi','sensor')))
                
                sendEmail(garage_state)

@route('/GarageOpener')
def trigger():
    passwd = request.forms.get('password')
    if 'test' == config.get('host','passwd'):
        if request.forms.get('toggle'):
            toggle_garage()
            if config.get('mail','notify') == 'True':
                sendEmail('Garage Opened!')
        else:
            res = snapshot()
            resp = HTTPResponse(body=res,status=400)
            resp.set_header('content_type', 'image/jpeg')
            resp.set_header('garage_state', garage_state)
            return resp
    else:
        resp = HTTPResponse(body='test',status=404)
        return resp
#print snapshot()   

t = threading.Thread(target=garage_status)
t.start()


run(host=config.get('host','server'), port=config.get('host','port'))
#sendEmail('Test')
