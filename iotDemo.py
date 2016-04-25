import imp, json,cv2
import sys, threading, Queue, time
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor

fd = imp.load_source('FaceDetector','faceDetector/FaceDetector.py')
am = imp.load_source('AzureCognitiveManager','azureCogServManager/AzureCognitiveManager.py')
iot = imp.load_source('iotHubManager','iotHubManager/iotHubManager.py')
ws = imp.load_source('server','WebsocketServer/server.py')

weightsPath =  "/home/pixiepro/Desktop/ftf-iot-demo/faceDetector/weights.txt"
capturePath = "/home/pixiepro/Desktop/ftf-iot-demo/faceDetector/img.jpg"
azureKeys = "/home/pixiepro/Desktop/keys/azureKeys.txt"
deviceKeys = "/home/pixiepro/Desktop/keys/deviceKeys.txt"

def initObjects():
    faceDetector = fd.FaceDetector(weightsPath,
                                                           capturePath)
    with open(azureKeys,"r") as f:
        sub = json.load(f)
        f.close() 
    azureCognitive = am.AzureCognitiveManager(sub)

    with open(deviceKeys,"r") as f:
        credentials = json.load(f)
        f.close()
    iotHub = iot.IoTHubManager(credentials)
    return faceDetector, azureCognitive, iotHub
    


def startWebsocketServer():
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory(u"ws://127.0.0.1:8001")
    factory.protocol = ws.MyServerProtocol

    q = Queue.Queue()
    ws.MyServerProtocol.setQueue(q)

    reactor.listenTCP(8001, factory)
    t = threading.Thread(target = reactor.run, kwargs = {'installSignalHandlers':0})
    t.start()
    return q

def pollMsg():
    while q.empty():
        pass
    return q.get()

def startGame(msg):
    t = threading.Thread(target=faceDetector.detectFace)
    t.start()
    

def stopGame(msg):
    print "STOP GAME!"
    faceDetector.stop()
    faceAttr = azureCognitive.getFaceAttr(capturePath)
    emotion = azureCognitive.getEmotion(capturePath)
    activity = encodeActivity(msg,faceAttr,emotion)
    iotHub.send_message(json.dumps(activity))

def encodeActivity(msg,faceAttr,emotion):
    activity = dict()
    activity['date'] = msg['date']
    activity['score'] = msg['score']
    activity['gender'] = faceAttr['gender']
    activity['age'] = faceAttr['age']
    activity['glasses'] = faceAttr['glasses']
    activity['emotion'] = emotion
    return activity

    
commands = {
        "stopGame" : stopGame,
        "startGame" : startGame
        }

def decodeMsg(msg):
    try:
        print "received %s" % msg['cmd']
        commands[msg['cmd']](msg)
    except KeyError:
        print "Oops! Unknown command!"
    except Exception as e:
        print "Oops! Unexpected error!" + str(e)
    
faceDetector = None
azureCognitive = None
iotHub = None

if __name__== "__main__":
    faceDetector, azureCognitive, iotHub = initObjects()
    q = startWebsocketServer()

    startGame(None)

    while True:
        msg = json.loads(pollMsg())
        decodeMsg(msg)
