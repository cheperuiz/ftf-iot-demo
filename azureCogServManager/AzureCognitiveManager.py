import requests, json

class AzureCognitiveManager:

    def __init__(self,s):
        self._faceEndpoint = s['faceEndpoint']
        self._faceKey = s['faceKey']
        self._emotionEndpoint = s['emotionEndpoint']
        self._emotionKey = s['emotionKey']
    
    def _configFaceAttrReq(self, data):
        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = self._faceKey
        headers['Content-Type'] = 'application/octet-stream'

        params = dict()
        params['returnFaceAttributes'] = 'age,gender,glasses'
        params['returnFaceId'] = 'false'
        params['returnFaceLandmarks'] = 'false'

        r = dict()
        r['endpoint'] = self._faceEndpoint 
        r['headers'] = headers
        r[' params'] = params
        r['json'] = None
        r['data'] = data
        return r

    def _configEmotionReq(self, data):
        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = self._emotionKey
        headers['Content-Type'] = 'application/octet-stream'

        r = dict()
        r['endpoint'] = self._emotionEndpoint
        r['headers'] = headers
        r[' params'] = None
        r['json'] = None
        r['data'] = data
        return r

    def _makeRequest(self, r):
        response = requests.request( 
			'post', r['endpoint'], 
			json = r['json'], 
			data = r['data'], 
			headers = r['headers'], 
			params = r[' params'])
        return response

    def _getDataFromPath(self,path):
        with open(path, 'rb' ) as f:
            data = f.read()
            return data
    
    def getFaceAttr(self,path):
        data = self._getDataFromPath(path)
        req = self._configFaceAttrReq(data)
        response = self._makeRequest(req)
        print response.status_code, response.reason
        faces = json.loads(response.text)
        face = max(faces,key=lambda item:item['faceRectangle']['width'])
        return face['faceAttributes']

    def getEmotion(self,path):
        data = self._getDataFromPath(path)
        req = self._configEmotionReq(data)
        response = self._makeRequest(req)
        print response.status_code, response.reason
        faces = json.loads(response.text)
        face = max(faces,key=lambda item:item['faceRectangle']['width'])
        emotion = max(face['scores'],key=face['scores'].get)
        return emotion
        
