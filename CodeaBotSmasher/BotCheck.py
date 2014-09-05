import getpass
import re
import requests
from bs4 import BeautifulSoup
import time
import string
import CodeaForum
import BotPatterns
import BotSmasher
#import clipboard



killed = 0

userTable = []


def getUsers():
  global killed
  print '***Checking Bots***'
  #print 'Killed: ',killed
  pages = 3
  for i in range(pages):
    #print '***Page ',i+1, '***'
    url = "http://codea.io/talk/dashboard/user?Page=p{}&order=DateFirstVisit".format(i+1)
    res = CodeaForum.Codea.session.get(url,data = CodeaForum.Codea.data)
    CodeaForum.updateTransKey(res.content)
    #com = re.compile(r'(.*)')
    mat = re.search(r'(<tbody.*</tbody>)',res.content,re.M|re.I|re.S)
    #print mat.group()
    mat = '<table>'+mat.group()+'</table>'
    mat = mat.replace('<strong>at</strong>','@')
    mat = mat.replace('<em>dot</em>','.')
    parseUsers(mat)

    checkBots()


    #print soup.find('table', {'class': 'AltColumns'})
    #for line in soup.stripped_strings:
    #   print line.strip()
  print 'Checking Memeber Requests'
  checkRequests()

def parseUsers(str):
  ''' Parses forum users '''

  soup = BeautifulSoup(str)


  tag = soup.find_all('tr')
  #print tag

  #print tag
  for sibling in tag:
    tmpusers = {}
    #print sibling
    cell = sibling.find_all('td')

    tmpusers['name'] = cell[0].get_text()
    tmpusers['id'] = re.search(r'/talk/profile/(\d*)',cell[0].a['href']).group(1)
    #tmpusers['id'] =
    tmpusers['email'] =  cell[1].get_text()
    if re.search('Member',cell[2].get_text()):
      tmpusers['confirm'] = True
    else:
      tmpusers['confirm'] = False
    tmpusers['joined'] = cell[3].span['title']
    tmpusers['ip'] = cell[5].string
    userTable.append(tmpusers)




    #print d
    #data = sibling.find_all('td')
    #for d in data:
    #   print d

def checkBots():

  for user in userTable:
    global killed
    if not user['confirm']:
      result = BotPatterns.botCheck(user)
      if result:

        url = 'http://codea.io/talk/user/delete/{}/delete'.format(user['id'])

        d = {'Form/Delete_User_Forever' : 'Delete User Forever',
                'Form/htp':'',
                'Form/TransientKey': CodeaForum.Codea.tKey}


        res = CodeaForum.Codea.session.post(url,data = d)
        #print CodeaForum.Codea.tKey
        killed = killed + 1
        #print res.text
        #print '***Bot Found***'
        #print user['name']
        #print user['email']
        #print user['ip']
  #print 'Bots Deleted: ', killed

def checkRequests():

  #http://codea.io/talk/dashboard/user/applicants
  global killed
  content = CodeaForum.Codea.session.get('http://codea.io/talk/dashboard/user/applicants')
  mat = re.search(r'(<tbody.*</tbody>)',content.content,re.M|re.I|re.S)
  if mat:

    mat = '<table>'+mat.group()+'</table>'
    soup = BeautifulSoup(mat)


    tag = soup.find_all('tr')
  #print tag

  #print tag
    str = ''
    for sibling in tag:

      #print sibling
      cell = sibling.find_all('td')
      reason = cell[1].blockquote.string
      bot = BotPatterns.requestCheck(reason)
      str = str + '"' + reason + '",\n'
      if bot:
        killed = killed +1

        CodeaForum.Codea.session.get('http://codea.io' + cell[2].a.next_sibling.next_sibling['href'])



  print 'Bots killed: ', killed

  #clipboard.set(str)

##Run module by itself
if __name__ == "__main__":
  import sys
  #fib(int(sys.argv[1]))
  c = CodeaForum.Codea()
  def cb():
    getUsers()

  #c = CodeaForum.Codea()
  c.login(cb)
