import AzureCognitiveManager as az
import json

with open("/home/chepe/Desktop/keys/azureKeys.txt","r") as f:
#with open("/Users/cheperuiz/Desktop/keys/azureKeys.txt","r") as f:
    sub = json.load(f)
    f.close() 

urlImage = "/home/chepe/Desktop/ftf-iot-demo/faceDetector/img5.jpg"
with open( urlImage, 'rb' ) as f:
    img = f.read()

acm = az.AzureCognitiveManager(sub)
faceAttr, faceId = acm.getFaceAttr(urlImage)
print faceAttr
similar = acm.findSimilar(faceId)
print similar
#emotion = acm.getEmotion(img)
#print 


