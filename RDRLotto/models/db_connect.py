#Create the connection
from singleton import Singleton
from pymongo import MongoClient
#import logger
from config_loader import Config_Loader

class DB_Connect(Singleton):
    ignoreSubsequent = True
    
    def __init__(self):
        conf = Config_Loader()
        #log = logger.get_log('db')
        self._connection = MongoClient(conf.mongo_host)
        self.user = self._connection.rdrlotto.users
        self.draw = self._connection.rdrlotto.draw
        self.winning = self._connection.rdrlotto.winning
        
if __name__ == '__main__':
    a = DB_Connection.getInstance()
    print id(a)
    b = DB_Connection.getInstance()
    print id(b)


