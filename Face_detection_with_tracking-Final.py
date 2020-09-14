import threading
import numpy as np
import imutils
from imutils.video import VideoStream
import cv2
import time
from webcamthread import WebcamVideoStream

c = threading.Condition()
cap = WebcamVideoStream(src = 0).start()
time.sleep(2)



class TrackerThread(threading.Thread):
           def __init__(self):
                      threading.Thread.__init__(self)
                      self.b = DNNThread()
                      self.b.start()
           def run(self):
                      try :
                                 while True:
                                            frame = cap.read()
                                            frame = imutils.resize(frame , width = 400)
                                            ok , bbox = self.b.tracker.update(frame)
                                            if ok:
                                                       p1 = ( int ( bbox[0]) , int (bbox[1]) )
                                                       p2 = ( int (bbox[0] + bbox[2]) , int(bbox[1] + bbox[3]))
                                                       cv2.rectangle(frame , p1 , p2 , ( 255 , 0 , 0 ) , 2 , 1)
                                            else :
                                                       cv2.putText(frame , "Tracking failure detected" , (100 , 80) , cv2.FONT_HERSHEY_SIMPLEX , 0.75 , (0 , 0 , 255) , 2)
                                            cv2.imshow('frame' , frame)
                                            if  cv2.waitKey(1) & 0xff  == 27 or self.b.out :
                                                       self.getout()
                                                       break
                      except Exception as e:
                                            print('Error occured in Tracker thread \n', e )
                                            self.getout()
           def getout(self):
                      print('Exiting the program')
                      self.b.stopit = True
                      self.b.join()
                      cap.stop()


                                 
class DNNThread(threading.Thread):
           def __init__(self):
                      threading.Thread.__init__(self)
                      self.net = cv2.dnn.readNetFromCaffe( 'deploy.prototxt' , 'res10_300x300_ssd_iter_140000.caffemodel' )
                      self.stopit = False
                      self.out = False
                      self.runcode()
           def getm(self):
                      return self.m
           def run(self):
                      global cap
                      try :
                                 while not self.stopit:
                                            self.runcode()
                      except Exception as e:
                                 print('Error occured in DNN Thread\n' , e)
                                 self.out = True

           def runcode(self):
                      img = cap.read()
                      self.img = cv2.resize(img , (400 , 300))
                      blob = cv2.dnn.blobFromImage( self.img , 1.0 , ( 400 , 300 ) , (104.0 , 177.0 , 123.0 ))
                      self.net.setInput(blob)
                      detections = self.net.forward()
                      box = detections[ 0 , 0, 0, 3:7 ]*np.array( [ 400 , 300 , 400 , 300 ] )
                      (startX , startY , endX , endY ) = box.astype("int")
                      if endX>self.img.shape[1] or endY>self.img.shape[0] or startX < 0 or startY < 0:
                           return
                      bbox = []
                      bbox.append(startX)
                      bbox.append( startY)
                      bbox.append(abs(startX-endX))
                      bbox.append(abs(startY-endY))
                      bbox = np.array(bbox)
                      self.tracker1 = cv2.TrackerKCF_create()
                      ok = self.tracker1.init(self.img , tuple(bbox))
                      self.tracker = self.tracker1
                      print('hel')


a = TrackerThread()
a.start()
a.join()
print('Finished....')
                      
