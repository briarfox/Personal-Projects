import requests
from bs4 import BeautifulSoup
import sys
try:
   import cPickle as pickle
except:
   import pickle
   
#roms = {}
#systems = ['nes','snes','psx','c64','atari2600']
systems = ['atari2600']
dirs = ['0','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

header = {'user-agent':'iPad'}

def get_link(url):
    data = requests.get('http://m.coolrom.com.au/%s' % url,headers=header)
    link = BeautifulSoup(data.text.encode('utf-8'))
    return link.find('form',{'name':'dlform'})['action']
    
def save(tbl):
    data = pickle.dumps(tbl)
    f = open('roms.txt','wb')
    f.write(data)
    f.close()
            
def parse_roms():
    print "Parsing CoolRoms Please wait..."
    roms = {}
    for system in systems:
        roms[system] = {}
        for dir in dirs:
            #header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
        
            data = requests.get('http://coolrom.com.au/roms/%s/%s'%(system,dir))
            soup = BeautifulSoup(data.text.encode('utf-8'))
            for link in soup.find_all('div',{'class': 'USA'}):
                tbl = {}                
                tbl[link.a.string.encode('utf-8')] = link.a['href'].encode('utf-8')
                roms[system].update(tbl)
                print 'Updated: %s - %s' % (system,link.a.string.encode('utf-8'))
    save(roms)
    

    
def load():
    try:
        f = open('roms.txt','rb')
        tbl = pickle.load(f)
        f.close()
        return tbl
    except :
        tbl = {}
        return tbl
    
if __name__ == '__main__':
    parse_roms()
    #print load()

