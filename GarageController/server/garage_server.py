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
    global sensor_pin = int(config.get('rpi','sensor'))
    print 'Pin Loaded'
    print sensor_pin
    GPIO.setup(sensor_pin,GPIO.IN, pull_up_down = GPIO.pud_up)
    GPIO_installed = True
except:
    print 'RPi.GPIO not installed'
    
#garage_state= False
toggle_time=0
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
  print config.get('mail','smtp')
  print config.get('mail','port')
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
    #msg = 'Wake up Sr. Charles Trowbridge! It is your last day!' #+ make_name()
    t = datetime.now().strftime('%H:%M:%S')
    if state == GARAGE_OPEN:
        msg = 'Garage Open (%s)'%t
    if state == GARAGE_CLOSED:
        msg = 'Garage Closed (%s)'%t
        
    try:
      server.sendmail( config.get('mail','send_as'), config.get('mail','recipients'), msg )
    except Exception, e:# smtplib.SMTPRecipientsRefused, e:
      print e
    finally:
      server.close()
      
def toggle_garage():
    t = datetime.now().strftime('%H:%M:%S')
    print t
    
def garage_status():
    if GPIO_installed:
        while True:
            if not garage_state:
                global garage_state = GPIO.input(config.get('rpi','sensor'))
                sendEmail(garage_state)
            
            if garage_state != GPIO.input(config.get('rpi','sensor')):
                sendEmail(garage_state)
                garage_state = GPIO.input(config.get('rpi','sensor'))
        

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

t = threading.thread(target=garage_status)
t.start()


run(host=config.get('host','server'), port=config.get('host','port'))
#sendEmail('Test')
