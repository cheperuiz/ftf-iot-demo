import FaceDetector as fd
import threading,cv2

d = fd.FaceDetector("/home/pixiepro/Desktop/ftf-iot-demo/faceDetector/weights.txt",'img.jpg')
t = threading.Thread(target=d.detectFace)
t.start()
