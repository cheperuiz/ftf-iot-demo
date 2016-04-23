import FaceDetector as fd
import threading

d = fd.FaceDetector("weights.txt",'img.jpg')
t = threading.Thread(target=d.detectFace)
t.start()
