from ConfigParser import SafeConfigParser
import sys
import os
conf_template = '''[mongodb]
host = host_url
'''

class Config_Loader():
    def __init__(self):
        self.check_config()
        self.parser = SafeConfigParser()
        self.parser.read('config.conf')
        self.mongo_host = self.parser.get('mongodb','host')
        if self.mongo_host == 'host_url' or self.mongo_host == '':
            sys.exit('Please add host info to config.conf')
        
    def check_config(self):
        if not os.path.isfile('config.conf'):
            f = open('config.conf','w')
            f.write(conf_template)
            f.close()
            sys.exit('Please add mongo db host info to config.conf')
            
if __name__=='__main__':
    conf = Config_Loader()
    print conf.mongo_host
