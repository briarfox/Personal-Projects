from model_interface import Model,get_cameras
import ui

#def video_cb(video,args):
    

class MainPresenter(object):
    def __init__(self):
        self.view = ui.load_view('../views/main_view')
        self.cameras = get_cameras()
        self.cam_view = self.view['cam_view']
        cam = Model(self.cameras['group1'][0])
        img = ui.ImageView()
        img.name = 'Garage'
        img.width = 400
        img.height = 400
        
        img.image = ui.Image.from_data(cam.snapshot())
        self.cam_view.add_subview(img)
        cam.start_video(callback=self.cb,args='Garage')
        self.active = True
        
    def cb(self,img,args):
        print 'Callback!'
        self.cam_view[args].image = ui.Image.from_data(img)
        
        
    def add_cams(self):
        for cam in self.cameras['group1']:
            c = Model(cam)
            c_view = ui.ImageView()
            c_view.name = cam['name']
            c_view.width = 400
            c_view.height = 400
            c.get_video(callback=self.cb,args=cam['name'])
        
        
if __name__=='__main__':
    main = MainPresenter()
    main.view.present('sheet')
