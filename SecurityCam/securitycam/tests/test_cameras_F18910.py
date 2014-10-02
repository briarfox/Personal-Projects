import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import  cameras.model_F18910
from model_interface import CameraManager, models,_Model

import mock

class TestCameras(object):
    
    def setup(self):
        self.cam = mock.MagicMock(spec=cameras.model_F18910)
        self.cam.snapshot.return_value = True
        models['F18910'] = self.cam
        self.camera = _Model({'user': 'chris',
                              'pwd': 'test',
                              'url': 'http://fake.com:8090',
                              'name': 'testCam',
                              'model': 'F18910'})
    
    
    def testF18910(self):
        assert(self.camera.snapshot())
        self.cam.snapshot.assert_called_with()
        #mock_cam.snapshot.return_value = True
        #print mock_cam.snapshot()
        #assert(mock_cam.snapshot({'user':'chris','pwd':'test','url':'http:,,fake.com'}))
        
if __name__=='__main__':
    test = TestCameras()
    test.testF18910()
