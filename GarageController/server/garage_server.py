from ConfigParser import SafeConfigParser
from datetime import datetime
import smtplib
import requests
import threading
import time

from bottle import route, run, request, HTTPResponse, post
#from nanpy import 

config = SafeConfigParser()
config.read('config.conf')

#Try to load GPIO
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    global sensor_pin 
    sensor_pin= int(config.get('rpi','sensor'))
    garage_pin = int(config.get('rpi','open'))
    print 'Pin Loaded'
    print sensor_pin
    GPIO.setup(sensor_pin,GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(garage_pin,GPIO.OUT, initial = GPIO.HIGH)
    
    GPIO_installed = True
except Exception, e:
    GPIO_installed = False
    print e
    print 'RPi.GPIO not installed'
    
#garage_state= False
toggle_time=0
garage_state = 'setup'
garage_user = 'System'
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
  
def sendEmail(state,user='Unknown'):
  server = initmail()
  if server:
    msg = 'Not Set'
    #msg = 'Wake up Sr. Charles Trowbridge! It is your last day!' #+ make_name()
    t = datetime.now().strftime('%H:%M:%S')
    if state == GARAGE_OPEN:
        msg = '\n%s Opened Garage at (%s)' % (user,t)
    if state == GARAGE_CLOSED:
        msg = '\n%s Closed Garage at (%s)' % (user,t)
        
    try:
        print msg + msg
        server.sendmail( config.get('mail','send_as'), config.get('mail','recipients'), msg )
    except Exception, e:# smtplib.SMTPRecipientsRefused, e:
        print e
    finally:
        server.close()
      
def toggle_garage():
    if GPIO_installed:
        print 'Garage Pin True'
        GPIO.output(garage_pin, GPIO.LOW)
        time.sleep(1)
        print 'Garage Pin False'
        GPIO.output(garage_pin, GPIO.HIGH)
        
    
    
def garage_status():
    global garage_state
    global garage_user
    if GPIO_installed:
        while True:
            if garage_state == 'setup':
                garage_state = GPIO.input(int(config.get('rpi','sensor')))
                time.sleep(1)
                sendEmail(garage_state,user=garage_user)
                garage_user = 'Unknown'
            if garage_state != GPIO.input(int(config.get('rpi','sensor'))):
                #sendEmail(garage_state)
                garage_state = GPIO.input(int(config.get('rpi','sensor')))
                
                sendEmail(garage_state,user=garage_user)
                garage_user = 'Unknown'


@post('/GarageOpener')
def trigger():
    global garage_user
    try:
        passwd = request.forms.get('password')
        if passwd == config.get('host','passwd'):
            if request.forms.get('toggle'):
                if request.forms.get('user'):
                    garage_user = request.forms.get('user')
                toggle_garage()
                #if config.get('mail','notify') == 'True':
                #    sendEmail('Garage Opened!')
            else:
                res = snapshot()
                resp = HTTPResponse(body=res,status=400)
                resp.set_header('content_type', 'image/jpeg')
                resp.set_header('garage_state', garage_state)
                return resp
        else:
            resp = HTTPResponse(body='test',status=404)
            return resp
    except IOError, e:
        print e
#print snapshot()   

t = threading.Thread(target=garage_status)
t.start()
#print GPIO.input(4)

try:
    run(host=config.get('host','server'), port=config.get('host','port'))
except IOError,e:
    print e
#sendEmail('Test')
