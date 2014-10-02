import cameras.model_F18910
from custom_errors import ConnError

from threading import Thread
import cStringIO
import plistlib
import os



models = {'F18910': cameras.model_F18910}


class CameraManager(object):
    def __init__(self,plist_dir=None):
        if plist_dir == None:
            self._plist_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self._plist_dir = plist_dir
             
        try: 
            self._settings = plistlib.readPlist(self._plist_dir+'/camera_settings.txt')
        except:
            self._settings = [{}, {}, {}, {},{}]
            
    def get_group(self,group):
        if group >=1 and group <=4:
            tbl = {}
            for i,setting in enumerate(self._settings[group]):
                cam = _Model(self._settings[group][setting])
                tbl[self._settings[group][setting].name] = cam 
            return tbl
        else:
            raise ValueError('Group number out of range.')
        
    def add_camera(self,group,url='http://fake.com',
                   port='8090',
                   user='johndoe',
                   password='password',
                   model='F18910',
                   name='testcam'):
        if group >=1 and group <=4:
            tbl = {'url': url+':'+port,
                   'model': model,
                   'user': user,
                   'pwd': password,
                   'name': name}
            self._settings[group][name] = tbl
        else: 
            raise ValueError('Group number out of range')
            
    def get_setting(self,key):
        return self._settings[0][key]
        
    def set_setting(self,key,value):
        self._settings[0][key] = value
        
    def save(self):
        with open(self._plist_dir + '/camera_settings.txt','w') as f: plistlib.writePlist(self._settings,f)
        
    


def _process_video(parent,fp,callback=None,args=None):
    while parent._is_playing:
        print parent._is_playing
        line = fp.raw.readline()
        if line[:len('--ipcamera')] == '--ipcamera':
            fp.raw.readline()
            content_length = int(fp.raw.readline().split(':')[1].strip())
            fp.raw.readline()
            jpeg = fp.raw.read(content_length)
            #file = cStringIO.StringIO(jpeg)
            #img = Image.open(file)
            #jpeg = Image.frombuffer('RGB',(640,480),jpeg)    
            if callback:
                callback(jpeg,args)
            
class _Model (object):
    def __init__(self,tbl):
        self.cam = tbl
        self.name = tbl['name']
        self.model = tbl['model']
        self._is_playing = False
        #settings = self.status
        self.motion_active = models[self.model].get_motion(self.cam)
        #self.ir_active = 
        
    def playing(self):
        return self._is_playing
        
    def snapshot(self):
        '''
        snapshot returns status_code, image
        '''
        return models[self.model].snapshot(self.cam)
        
    def start_video(self,callback=None,args=None):
        print 'Video Starting'
        if not self._is_playing:
            self._is_playing = True
            res = models[self.model].get_video(self,self.cam)
            self.videothread = Thread(target=_process_video, args=(self, res, callback,args))
            self.videothread.start()
        
        
    def stop_video(self):
        if self._is_playing:
            self._is_playing = False
            #self.videothread.join()
        
        
    def set_motion(self,state=False):
        self.motion_active = state
        models[self.model].set_motion(self.cam,state)
        
    def set_infrared(self,cam,state=False):
        pass
        
    def status(self):
        return models[self.model].status(self.cam)
        
if __name__=='__main__':
    
    def cb(jpeg):
        console.show_image('test.jpg')
        time.sleep(.09)
        console.clear()
        
    camM = CameraManager()
    #camM.add_camera(1,user='chouser56',password='i43kr13t1n',url='http://houserip.dyndns.tv',port='8090',name='House')
    cams = camM.get_group(1)
    print cams
    
