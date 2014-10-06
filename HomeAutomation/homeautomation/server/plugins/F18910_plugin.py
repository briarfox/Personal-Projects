from basePlugin import CameraPlugin
import requests
#from custom_errors import ConnError

_actions = {'checkuser': "/check_user.cgi",
            'snapShot': "/snapshot.cgi",
            'getStatus': "/get_status.cgi",
            'getParams': "/get_params.cgi",
            'alarmToggle': "/set_alarm.cgi",
            'irToggle': "/decoder_control.cgi?command=%s",
            'Watch': "/decoder_control.cgi?command=%s",
            'video': '/videostream.cgi'}
class Camera(CameraPlugin):
    '''Foscam F18910 Plugin'''
    def __init__(self,user=None,passwd=None,host=None):
       CameraPlugin.__init__(self,user=user,passwd=passwd,host=None) 
        
    def snapshot(self):
        '''
        snapshot returns status_code, image
        '''
        payload = {'user' :self.username,'pwd': self.passwd}
        data = requests.get(self.host+_actions['snapShot'],params=payload)
        return data.content

    @property
    def ir(self):
        print 'ir not setup'

    @ir.setter
    def ir(self,value):
        print value

    def video(self):
        pass

    def status(self):
        pass

    
'''
def get_video(parent,tbl):
    cmds = { 'user': tbl['user'],'pwd': tbl['pwd'], 'resolution':32, 'rate':0 }
    res = requests.get(tbl['url']+_actions['video'],params=cmds,stream=True)
    return res

def set_motion(cam,state=False):
    cmd = 1 if state else 0
    payload = {'user': cam['user'],'pwd': cam['pwd'],'motion_armed': cmd}
    data = requests.get(cam['url']+_actions['alarmToggle'],params=payload)
    if data == None:
        raise ConnError('set_motion failed.')
    
def get_motion(cam):
    settings = status(cam)
    if settings['alarm_motion_armed'] == '1':
        return True
    elif settings['alarm_motion_armed'] == '0':
        return False
    else: 
        raise ConnError('Cannot get alarm_motion_armed.')
        
def infrared(cam,state=0):
    pass

def status(cam):
    tbl = {}
    payload = {'user': cam['user'], 'pwd': cam['pwd']}
    data = requests.get(cam['url']+_actions['getStatus'])
    if data == None:
        raise ConnError('Cannot get camera status.')
    content = data.content.replace('var ','').replace('\n','')
    for field in content.split(';'):
        if field != '':
            keyvalue =  field.split('=')
            tbl[keyvalue[0]] = keyvalue[1]
    
    data = requests.get(cam['url']+_actions['getParams'],params=payload)
    if data == None:
        raise ConnError('Cannot get camera params.')
    content = data.content.replace('var ','').replace('\n','')
    for field in content.split(';'):
        if field != '':
            keyvalue =  field.split('=')
            tbl[keyvalue[0]] = keyvalue[1]


    return tbl
        
        
'''
if __name__=='__main__':
    c = Camera(user='briarfox',passwd='test',host='localhost:8090')
    print c.username
    print c.passwd
    print c.host
