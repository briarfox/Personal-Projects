# coding: utf-8

import ui
import plistlib
from model_interface import CameraManager
STATE = 0
view = ui.load_view('../views/test_view')

cameraMngr = CameraManager()
cameras = cameraMngr.get_group(1)



def cb(jpeg,name):
    print type(jpeg)
    view[name].image = ui.Image.from_data(jpeg)
    #view['im1'].image = ui.Image.from_data(jpeg)


def button_pressed(sender):
    for name,cam in cameras.iteritems():
        if not cam._is_playing:
            cam.start_video(callback=cb,args=cam.name)
        else:
            cam.stop_video()
            #model1.start_video(callback=cb,args='House')
view['btn'].action = button_pressed
view.present('sheet')
        



