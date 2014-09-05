import getpass
import re
import requests
from bs4 import BeautifulSoup
import time
import sys


class  Codea:
  data = {}
  session = requests.session()
  tKey = "nil"
  host = {}
  host['url'] = "http://Codea.io/talk/"
  host['login'] = "entry/signin"
  host['messages'] = "messages/"
  host['inbox'] = "messages/inbox"
  host['sendMessage'] = "messages/addmessage"
  host['startConversation'] = "messages/add?DeliveryType=VIEW"
  host['startDiscussion'] = "post/discussion/1"


  headers = {}
  headers["Accept"] = "text/plain"
  headers["Content-Type"] = "application/x-www-form-urlencoded"
  headers["Accept-Charset"] = "utf-8"

  #init
  #def __init__(self):
      #print 'class loaded'
      #host = {}
      #host['url'] = "http.google.com"


  #login
  def login(self,cb):
    '''Starts the authentication proccess to login to codea forums'''
    if len(sys.argv) == 3:
      self.user = sys.argv[1]
      self.password = sys.argv[2]
    else:
    #Loads saved credentials
      self.user = raw_input('Username: ')
      self.password = getpass.getpass('Password: ')

    #Assume credentials are wrong until checked
    self.legit = False
    self.authenticating = True

    # Store function to be called when credentials are confirmed and user is logged in
    self.onLogin = cb

    #Verify credentials / login
    transientKey = requests.get(Codea.host['url'] + Codea.host['login'])
    #print transientKey
    html = BeautifulSoup(transientKey.content)
    #print html
    inputTag = html.input
    #print inputTag
    Codea.tKey = inputTag['value']
    print 'First TransKey '+Codea.tKey
    #print time.strftime("%Y-%m-%d %H:%M")

    #data = {}
    Codea.data['Checkboxes[]'] = 'RememberMe'
    Codea.data['DeliveryMethod'] = 'JSON'
    Codea.data['DevliveryType'] = 'VIEW'
    Codea.data['Form/ClientHour'] = time.strftime("%Y-%m-%d %H:%M")
    Codea.data['Form/Email'] = self.user
    Codea.data['Form/htp'] = ''
    Codea.data['Form/Password'] = self.password
    Codea.data['Form/RememberMe'] = "1"
    Codea.data['Form/Sign_In'] = 'Sign In'
    Codea.data['Form/Target'] = 'discussions'
    Codea.data['Form/TransientKey'] = Codea.tKey

    res = Codea.session.post(Codea.host['url'] + Codea.host['login'],data=Codea.data)
    #data:match('"FormSaved":(.-),"')
    #<input type="hidden" id="TransientKey" value="GU2KSYGVYOYW" />

    logged_On = re.search(r'("FormSaved":)',res.content)


    if not logged_On:
      updateTransKey(res.content)
      #soup = BeautifulSoup(res.content)
      #tag = soup.find(attrs={"id" : "TransientKey"})
      #Codea.tKey = tag['value']
      print "Logged in as: " + self.user
      self.onLogin()
    else:
      print "Error Logging in."
      self.login(self.onLogin)





    #print self.user,self.password

def updateTransKey(str):
  soup = BeautifulSoup(str)
  tag = soup.find(attrs={'id' : 'TransientKey'})
  if tag:
    #print tag['value']
    Codea.tKey = tag['value']





##Run module by itself
if __name__ == "__main__":
  import sys
  #fib(int(sys.argv[1]))
  def cb():
    print 'cb called! loaded!'
  c = Codea()
  c.login(cb)
