import requests

_url = 'https://api.projectoxford.ai/face/v1.0/detect'
_key = ''
urlImage = '/home/chepe/Desktop/chepe.jpg'

# Face detection parameters
params = { 
	'returnFaceAttributes': 'age,gender,glasses',
	'returnFaceId': 'false',
	'returnFaceLandmarks': 'false'	} 

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream' 

json = None 
with open( urlImage, 'rb' ) as f:
    data = f.read()

response = requests.request( 
			'post', _url, 
			json = json, 
			data = data, 
			headers = headers, 
			params = params )

print response.status_code, response.reason
print response.text
