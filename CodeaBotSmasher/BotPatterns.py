import re
import datetime
botPatterns = []
bannedDomains = ['drdrb.net',
                 '10minutemail.com',
                 'uikd.com',
                 'Guerrillamail.com',
                 'my10minutemail.com',
                 'drdrb.com',
                 'mailinator.com',
                 'meltmail.com',
                 'dayrep.com',
                 'harikirimail.com'
                 ]

botRequests = ["Chaussure Zanotti",
"Mbt",
"Scarpe",
"Miu",
"Hermes Borse",
"Chanel Borse",
"Occhiali Chanel",
"Borse",
"Ralph Lauren",
"Outlet Rolex",
"Outlet",
"Rolex",
"Calvin Klein",
"Lacoste",
"Celine",
"Borsa Burberry",
"Ray Ban",
"Carolina Herrera Vestidos",
"Lululemon",
"Erika",
"Gafas De Sol",
"Bottes UGG Broome",
"Sac Louis Vuitton Pas Cher",
"Puma Pas Cher",
"Sac Gucci",
"Pants",
"Lunette De Soleil",
"Bolsos Carolina Herrera",
"Hogan Uomo",
"Bottes UGG Adirondack Tall Pas Cher",
"Michael Kors Orologi",
"Sale",
"Occhiale",
"Air Max",
"Armani",
"Shoes",
"Burberry Soldes",
"Carolina Herrera",
"Asics",
"Cheap",
"Armani Pas Cher",
"Hogan Uomo",
"Coach",
"Kors",
"Bolsos Michael",
"Montre Michael",
"Air Jordan",
"Coach",
"Michael Kors",
"Toms Outlet",
"Michael Kors Sac",
"Sac Michael Kors",
"Bottes",
"Casio",
"Oakley",
"Oakly"
"Hogan",
"Vuitton",
"Bose",
"{I want to {",
"Timberland",
"Chaussure",
"Giuseppe",
"Zanotti"]

Month = {'January':1,
          'February':2,
          'March':3,
          'April':4,
          'May':5,
          'June':6,
          'July':7,
          'August':8,
          'September':9,
          'October':10,
          'Novemeber:':11,
          'December':12}


#Check for a large number of .
def dotCheck(str):

  mat = re.findall('(\.)',str['email'])
  if len(mat) >=3:
    return True
  else:
    return False
botPatterns.append(dotCheck)


#Check for the use of +
def plusCheck(str):
  mat = re.search('\+\w+',str['email'])
  if mat:
    return True
  else:
    return False
botPatterns.append(plusCheck)

#Check blocked domains
def domainCheck(str):
  mat = re.search('@([\w.]+)',str['email'])
  found = False
  for domain in bannedDomains:
    if mat.group(1) == domain:
      found = True
      break
  return found
botPatterns.append(domainCheck)

#check non Confirmed
def confirmCheck(str):
  #April 19, 2014  7:37PM
  found = False
  dateTbl = re.search('(\w+)[ ]*(\d+),[ ]*(\d+)',str['joined'])
  m = Month[dateTbl.group(1)]
  past = datetime.date(int(dateTbl.group(3)),m,int(dateTbl.group(2)))
  now = datetime.date.today()
  if (now - past) > datetime.timedelta(days = 1):
    found = True
  return found
botPatterns.append(confirmCheck)



##################
#Checks for bots

def botCheck(str):
  bot = False
  for func in botPatterns:
    result = func(str)
    if result == True:
      bot = True
      #break
  return bot

def requestCheck(str):
  bot = False
  for ban in botRequests:
    if ban in str:
      return True
  return False




if __name__ == "__main__":
  import sys
  #fib(int(sys.argv[1]))
  bots = [{'email' : 'test.t.y.t.@gol.com','joined':'April 30, 2014  7:37PM'},
          {'email' : 'chhrhehrerADGB@drdrb.net','joined':'May 1, 2014  7:37PM'},
          {'email':'chris@housercompany.com','joined':'April 19, 2014  7:37PM'}
          ]
  for b in bots:
    if botCheck(b) == True:
      print b
