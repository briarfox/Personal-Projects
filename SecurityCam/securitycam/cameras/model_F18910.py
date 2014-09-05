
import requests

_actions = {'checkuser': "/check_user.cgi",
            'snapShot': "/snapshot.cgi",
            'getStatus': "/get_status.cgi",
            'getParams': "/get_params.cgi",
            'alarmToggle': "/set_alarm.cgi?user=%s&pwd=%s&motion_armed=%s",
            'irToggle': "/decoder_control.cgi?command=%s",
            'Watch': "/decoder_control.cgi?command=%s",
            'video': '/videostream.cgi'}
            
        
def snapshot(url,user,pwd):
    '''
    snapshot returns status_code, image
    '''
    payload = {'user' :user,'pwd': pwd}
    data = requests.get(url+_actions['snapShot'],params=payload)
    print data.status_code
    return (data.status_code,data.content)
    
def get_video(parent,url,user,pwd):
    print 'in model_xxxx'
    cmds = { 'user': user,'pwd': pwd, 'resolution':32, 'rate':0 }
    res = requests.get(url+_actions['video'],params=cmds,stream=True)
    print 'res recieved'
    return res

def motion(url,user,pwd,state=0):
    pass

def infrared(url,user,pwd,state=0):
    pass

def status(url,user,pwd):
    tbl = {}
    payload = {'user': user, 'pwd': pwd}
    data = requests.get(url+_actions['getStatus'])
    content = data.content.replace('var ','').replace('\n','')
    for field in content.split(';'):
        if field != '':
            keyvalue =  field.split('=')
            tbl[keyvalue[0]] = keyvalue[1]
    
    data = requests.get(url+_actions['getParams'],params=payload)
    content = data.content.replace('var ','').replace('\n','')
    for field in content.split(';'):
        if field != '':
            keyvalue =  field.split('=')
            tbl[keyvalue[0]] = keyvalue[1]


    return tbl
        
        

