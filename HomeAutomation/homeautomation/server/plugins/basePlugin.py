import abc

CAMERA = 0
IO = 1

#devices
RPI = 0
ARDUINO = 1


class  _AbstractPlugin(object):
    '''Base plugin for plugin classes'''''
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractproperty
    def type(self):
        pass
        
    @abc.abstractproperty
    def name(self):
        pass
        
    @name.setter
    def name(self,value):
        print 'tried to set'

        
class CameraPlugin(_AbstractPlugin):
    '''Inherit all camera plugins from this class
    Must include:
        @property
            self.ir - getter - setter
            self.motion - getter - setter
        
        Methods:
            snapshot
            video
            status
    '''
    
    __metaclass__ = abc.ABCMeta
    
    name = 'Generic Name'
    type = CAMERA
    
    def __init__(self,type=None,name=None):
        if type is not None:
            self.type = type
        if name is not None:
            self.name = name
            
    @abc.abstractproperty
    @property
    def ir(self):
        pass
            
    @abc.abstractmethod
    def snapshot(self):
        pass
        
    @abc.abstractmethod
    def video(self):
        pass
        
    @abc.abstractmethod
    def status(self):
        pass
        
    
    
    
                    
class IOPlugin(_AbstractPlugin):
    pass
    
if __name__=='__main__':
    class Test(CameraPlugin):
        def __init__(self):
            pass
            
    t = Test()
        
    
        

