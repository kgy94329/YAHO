import cv2
import base64
import requests
import json

cap = cv2.VideoCapture(0)

while True:
    stat, img = cap.read()

    if not stat:
        break
    
    img = cv2.resize(img, (640,640))

    cv2.imshow("get", img)

    order = cv2.waitKey(1)
    if order == ord('s'):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        _, img = cv2.imencode('.png', img)
        img_code = base64.encodebytes(img).decode('utf-8')
        data = {"text":"right", "img":img_code}
        content_type = 'application/json'
        headers = {'content-type': content_type, 'charset':'utf-8'}
        data = json.dumps(data)

        response = requests.post('http://34.64.197.102:9090/newface', data = data, headers=headers)
        print(response.text)
    if order == 27:
        break