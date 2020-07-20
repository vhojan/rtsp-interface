from .camera import Camera
import atexit
import cv2
import numpy as np
import threading
import traitlets

#version 0.3 hallo?

class RTSPCamera(Camera):
    
    capture_fps = traitlets.Integer(default_value=15)
    capture_width = traitlets.Integer(default_value=640)
    capture_height = traitlets.Integer(default_value=480)  
    capture_device = traitlets.Unicode(default_value='rtsp://Your_IP_Cam_Address')        
    
    def __init__(self, *args, **kwargs):
        super(RTSPCamera, self).__init__(*args, **kwargs)
        try:
            self.cap = cv2.VideoCapture(self.capture_device, cv2.CAP_FFMPEG)

            re , image = self.cap.read()
            
            if not re:
                raise RuntimeError('Could not read image from camera, phase 1.')
            
        except:
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace, phase 2.')

        atexit.register(self.cap.release)
                
    def _gst_str(self):
        return (self.capture_device, self.capture_width, self.capture_height)
          
    def _read(self):
        re, image = self.cap.read()
        if re:
            image_resized = cv2.resize(image,(int(self.width),int(self.height)))
            return image_resized
        else:
            raise RuntimeError('Could not read image from camera, phase 3')
