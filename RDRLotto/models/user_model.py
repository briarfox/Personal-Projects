from singleton import Singleton
from db_connect import DB_Connect
from bson.objectid import ObjectId


class Users(Singleton):
    
    def __init__(self):
        self.users = DB_Connect.getInstance().user
        
    def new(self):
        id = self.users.insert({'name': 'New User',
                                'balance': 0.00,
                                'number': ' ',
                                'mega': ' ',
                                'phone': ' ',
                                'leader': False})
        return User(self.users.find_one({'_id': id}))
        
    def get_from_name(self,name):
        users = self.users.find({'name': name})
        print users.count()
        if users.count() > 1:
            lst = []
            for user in users:
                lst.append(User(user))
            return lst
        else:
            return User(users[0])
        
    def get_from_id(self,id):
        if type(id) == str:
            id = ObjectId(id)
        return User(self.users.find_one({'_id': id}))
        
    def update(self,user):
        d = user.dict()
        self.users.update({'_id': d['_id']},d)
        
    def delete(self,id):
        if type(id) == str:
            id = ObjectId(id)
        self.users.remove({'_id': id})
        
    def list(self):
        tbl = []
        users = self.users.find()
        for user in users:
            tbl.append(User(user))
        return tbl
        
        
class User(object):
    '''
    user object created by Users
    '''
    
    def __init__(self,user):
        self._id = user['_id']
        self._balance = float(user['balance'])
        self._name = user['name']
        self._number = user['number']
        self._mega = user['mega']
        self._leader = user['leader']
        self._phone = user['phone']
        
    def __repr__(self):
        return '<id: %s name: %s number: %s mega: %s balance: %s leader: %s phone: %s>' % (str(self._id),
                                                                               self._name,
                                                                               self._number,
                                                                               self._mega,
                                                                               self._balance,
                                                                               self._leader,
                                                                               self._phone)
    
    def dict(self):
        return {'name': self._name,
                'number': self._number,
                'mega': self._mega,
                'phone': self._phone,
                'leader': self._leader,
                'balance': self._balance,
                '_id': self._id}
        
    def get_name(self):
        return self._name
        
    def set_name(self,name):
        self._name = name
        
    def get_number(self):
        return str(self._number)
        
    def set_number(self,num):
        self._number = num
        
    def get_mega(self):
        return str(self._number)
        
    def set_mega(self,num):
        self._mega = num
        
    def get_phone(self):
        return str(self._number)
        
    def set_phone(self,num):
        self._phone = num
        
    def get_balance(self):
        return str(self._number)
        
    def add_balance(self,num):
        self._balance += float(num)
        
    def sub_balance(self,num):
        self._balance -= float(num)
        
        
    

        
        

        
if __name__=='__main__':
    u = Users.getInstance()
    
    
    #user = u.new()
    #print user
    #for user in u.list():
    #    print user
