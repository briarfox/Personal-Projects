import pymongo

#Globals
url = 'mongodb://briarfox:bassfish@ds055689.mongolab.com:55689/rancho'

class CableManager(object):
    def __init__(self):
        
        self.client = pymongo.MongoClient(url)
        self.db = self.client.rancho
        self.cable_loc = self.db['Cable_Lines']
        if self.db['Cable_Lines'].count() == 0:
            spaces = self._setup_spaces()
            self.cable_loc.insert(spaces)
            
        
    def _setup_spaces(self):
        spaces = []
        for i in range(381):
            tbl = {'space': i+1,
                   'notes': '',
                   'front': '',
                   'carport': '',
                   'buried': False}
            spaces.append(tbl)
        return spaces
        
    def get(self,space):
        return self.cable_loc.find_one({'space':space})
        
    def set(self,num,tbl):
        num = int(num)
        space = self.cable_loc.find_one({'space': num})
        print type(space)
        if space:
            print self.cable_loc.update({'space': num}, {'$set': tbl})
            
        else:
            raise Exception("Invalid Space number")
        
if __name__=='__main__':
    cableMngr = CableManager()
    cableMngr.set(2,{'front': '1.1','carport': '6'})
    print cableMngr.get(2)
    #print cableMngr.setup_spaces()
