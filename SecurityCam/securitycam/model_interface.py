import cameras.model_F18910
from threading import Thread


models = {'F18910': cameras.model_F18910}

def process_video(parent,fp,callback=None):
    while parent._is_playing:
        line = fp.raw.readline()
        if line[:len('--ipcamera')] == '--ipcamera':
            fp.raw.readline()
            content_length = int(fp.raw.readline().split(':')[1].strip())
            fp.raw.readline()
            jpeg = fp.raw.read(content_length)
                
            if callback:
                callback(jpeg)
            
class Model (object):
    def __init__(self,model,url,user,pwd):
        self.url = url
        self.user = user
        self.pwd = pwd
        self.model = model
        self._is_playing = False

        
    def snapshot(self):
        '''
        snapshot returns status_code, image
        '''
        return models[self.model].snapshot(self.url,self.user,self.pwd)
        
    def start_video(self,callback=None):
        print 'Video Starting'
        if not self._is_playing:
            self._is_playing = True
            res = models[self.model].get_video(self,self.url,self.user,self.pwd)
            self.videothread = Thread(target=process_video, args=(self, res, callback))
            self.videothread.start()
            print 'video started!'
        
        
    def stop_video(self):
        if self._is_playing:
            print 'Video Stopped!'
            self._is_playing = False
            self.videothread.join()
        
        
    def motion(self,state=False):
        pass
        
    def infrared(self,state=False):
        pass
        
    def status(self):
        return models[self.model].status(self.url,self.user,self.pwd)
        
if __name__=='__main__':
    import plistlib
    import console
    import time
    def cb(jpeg):
        with open('test.jpg','w') as f:
            f.write(jpeg)
        console.show_image('test.jpg')
        time.sleep(.09)
        console.clear()
        
    cams = plistlib.readPlist('settings.plist')
    cam = cams['cam2']
    model = Model(cam['model'],cam['url'],cam['user'],cam['pwd'])
    model.start_video(callback=cb)
    time.sleep(5)
    model.stop_video()
    #for line in res.content.readline():
    #    print line
    #    break
