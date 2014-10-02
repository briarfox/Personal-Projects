import ui
import os
import random
import string
from model_interface import models,read_plist, write_plist

class MyTextFieldDelegate (object):
    def textfield_did_begin_editing(self, textfield):
        print 'began editing'
    def textfield_did_end_editing(self, textfield):
        print 'end editing'
    def textfield_did_change(self, textfield):
        print 'did change'

class AddPresenter(object):
    def __init__(self,group='group1'):
        self.group=group
        self.view = ui.load_view('../views/add_view')
        self.active = True
        self.name = self.view['tf_name']
        self.model = self.view['tf_model']
        self.model.delegate = MyTextFieldDelegate()
        self.url = self.view['tf_url']
        self.port = self.view['tf_port']
        self.user = self.view['tf_user']
        self.pwd = self.view['tf_password']
        
        self.save_btn = self.view['button1']
        self.save_btn.action = self.save
        
    def save(self,sender):
        tbl = {}
        tbl['name'] = self.name.text
        tbl['model'] = 'F18910' #self.model
        tbl['url'] = self.url.text+':'+self.port.text
        tbl['user'] = self.user.text
        tbl['pwd'] = self.pwd.text
        tbl['user_pwd'] = self.pwd.text
        tbl['rand_pwd'] = self.rand_pwd()
        add_cameras(self.group,tbl)
        self.active = False
        

    def rand_pwd(self):
        length = 10
        chars = string.ascii_letters + string.digits
        random.seed = (os.urandom(1024))

        return ''.join(random.choice(chars) for i in range(length))
        
        
        
    
        
        
if __name__=='__main__':

    view = AddPresenter()
    view.view.present('sheet')

