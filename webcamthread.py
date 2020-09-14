from threading import Thread
import cv2
class WebcamVideoStream:
           def __init__(self, src=0):
                      self.stream = cv2.VideoCapture(src)
                      (self.grabbed, self.frame) = self.stream.read()
                      self.stopped = False

           def start(self):
                      Thread(target=self.update, args=()).start()
                      return self
           def update(self):
                      while True:
                                 (self.grabbed, self.frame1) = self.stream.read()
                                 if not self.grabbed :                                            
                                            print(self.grabbed)
                                 self.frame = self.frame1
                                 if self.stopped:
                                            self.stream.release()
                                            return None
           def read(self):
                      return self.frame
           def stop(self):
                      self.stopped = True
