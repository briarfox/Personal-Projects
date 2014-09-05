#Create the connection
from pymongo import MongoClient
from bson.objectid import ObjectId
import logger
from config_loader import Config_Loader

conf = Config_Loader()
#log handler
log = logger.get_log('db')

#db connection
connection = MongoClient(conf.mongo_url)
#Table list
db_users = connection.rdrlotto.users
db_draw = connection.rdrlotto.draw
db_winning = connection.rdrlotto.winning

##########
#User
#########
def get_user(tbl={}):
    return db_users.find_one(tbl)

def new_user(name,number,mega,balance,leader,phone):
    tbl = {'name': name,
          'number': number,
          'mega': mega,
          'balance': float(balance),
          'leader': leader,
          'phone': phone,
          'won': 0,
          }
    id = db_users.insert(tbl)
    log.info('New user created %s id: %s' % (name,str(id)))
    return id

def list_users():
    return list(db_users.find())

def update_user(id,tbl):
    log.info('User Updated id: %s info: %s' % (id,str(tbl)))
    db_users.update({'_id': id},tbl)

def delete_user(name):
    db_users.remove({'name': name})


################
#draw collection
################
def get_draw(id):
    return db_draw.find_one({'_id': id})

def new_draw(draw_id,date,number,mega,url,checked=False):
    tbl = {'draw_id': draw_id,
           'date': date,
           'number': number,
           'mega': mega,
           'url': url,
           'checked': checked,
           }
    log.info('New draw created id: %s' % str(draw_id))
    id = db_draw.insert(tbl)
    return id

def list_draw(search={}):
    return list(db_draw.find(search).sort('draw_id'))

def update_draw(id,tbl):
    log.info('Draw Updated id: %s info: %s' % (id,str(tbl)))
    db_draw.update({'_id': id},tbl)

def delete_draw(id):
    id = str(id)
    db_draw.remove({'_id': ObjectId(id)})

####################
#winning collection
####################
def get_win(id):
    print 'type passed'
    print type(id)
    if type(id)==str:
        id = ObjectId(id)
    print 'converted'
    print type(id)
    return db_winning.find_one({'_id': id})

def new_win(user_id,draw_id,won=0,amount=0,checked=0):
    tbl = {'user_id': user_id,
           'draw_id': draw_id,
           'won': won,
           'amount': amount,
           'checked': checked,
           }
    
    id = db_winning.insert(tbl)
    log.info('New win created id: %s' % str(id))

def list_win(tbl={}):
    return list(db_winning.find(tbl))

def update_win(id,tbl):
    log.info('Win Updated id: %s info: %s' % (id,str(tbl)))
    db_winning.update({'_id': id},tbl)

def delete_win(id):
    id = str(id)
    db_winning.remove({'_id': ObjectId(id)})

#Misc
###Get total won.
def totalWon():
    win = list_win()
    total = 0
    for won in win:
        total += won['amount']

    return total

###Delete tables






if __name__=='__main__':
    id =  new_user("Kristin","3 6 10 56 72",3,0.00,False,"7143291319")
    print 'new id %s' % id
    print get_user(id)
    update_user(id,{'name': 'Dean'})

    lis =  list_users()
    for user in lis:
        delete_user(user['_id'])

    for name in list_users():
        print name['name'],name['_id']
    connection.close()
