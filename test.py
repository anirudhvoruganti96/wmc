#API endpoint
API_ENDPOINT="http://ec2-35-154-153-202.ap-south-1.compute.amazonaws.com:8083/tsiic/unauthorizeddumping/violation"


import io
from PIL import Image
import requests
import json
import base64



img = Image.open('preview.jpg', mode='r')
#roiImg = img.crop(box)

imgByteArr = io.BytesIO()
img.save(imgByteArr, format='JPEG')
imgByteArr = imgByteArr.getvalue()

encoded=base64.b64encode(imgByteArr)

#print(encoded)


#to decode
#arr=base64.b64decode(encoded)
#print(arr)

headers = {
    'Content-Type': 'application/json'
    }



payload={
    "deviceId":"1",
    "image1":list(encoded),
    "image2":list(encoded),
    "status":"0"

}

response=requests.post(url=API_ENDPOINT,data=json.dumps(payload),headers=headers)
print(response.text)
