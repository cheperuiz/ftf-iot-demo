import AzureCognitiveManager as az
import json

with open("/home/pixiepro/Desktop/keys/azureKeys.txt","r") as f:
    sub = json.load(f)
    f.close() 

urlImage = "/home/pixiepro/Desktop/ftf-iot-demo/faceDetector/img.jpg"
with open( urlImage, 'rb' ) as f:
    img = f.read()

acm = az.AzureCognitiveManager(sub)
faceAttr = acm.getFaceAttr(img)
print faceAttr
emotion = acm.getEmotion(img)
print 
