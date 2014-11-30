# coding: utf-8

import ui
from cable_db import CableManager

db = CableManager()

class MyTextFieldDelegate (object):
    #def __init__(self,view):
    #    self.view = view
        
    def textfield_did_begin_editing(self, sender):
        pass
    def textfield_did_change(self, sender):
        view = sender.superview
        try:
            num = view['space'].text
            space = db.get(int(num))
            view['space_lbl'].text = 'Space: '+ str(num)
            view['street'].text = space['front']
            view['carport'].text = space['carport']
            view['notes'].text = space['notes']
            view['buried'].value = space['buried']
            view.set_needs_display()
        except:
            print 'ERROR'



def button_pressed(sender):
    if sender.name =='go':
        view = sender.superview
        try:
            num = view['space'].text
            space = db.get(int(num))
            print space
            view['space_lbl'].text = 'Space: '+ str(num)
            view['street'].text = space['front']
            view['carport'].text = space['carport']
            view['notes'].text = space['notes']
            view['buried'].value = space['buried']
            view['space'].text = ''
        except:
            print 'Error'
            
    elif sender.name == 'update':
        print 'updating'
        view = sender.superview
        try:
            num = int(view['space'].text)
            tbl = {}
            tbl['front'] = view['street'].text
            tbl['carport'] = view['carport'].text
            tbl['notes'] = view['notes'].text
            tbl['buried'] = view['buried'].value
            
            print db.set(num,tbl)
            
            
        except:
            print 'error'
        
view = ui.load_view()
view['go'].action = button_pressed
view['update'].action = button_pressed
view['space'].delegate = MyTextFieldDelegate()
view.present('sheet')

