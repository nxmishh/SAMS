import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('http://192.168.109.103:8000/stream')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()