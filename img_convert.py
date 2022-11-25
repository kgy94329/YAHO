'''
File: img_convert.py
Author: Guyoung Kwon
Date: 2022-11-21
Note:
    face_detector.py 모듈의 기능을 테스트하기 위한 모듈
    face_detector는 다른 서버에서 구동되어야 하며 본 모듈은 로컬에서 실행되어야 한다.

'''

import cv2
import base64
import requests
import json
import re

cap = cv2.VideoCapture(0)
content_type = 'multipart/form-data'
headers = {'content-type': content_type, 'charset':'utf-8'}

embeddings = []
tar = ['front', 'right', 'left']
cnt = 0

while True:
    stat, img = cap.read()

    if not stat:
        break
    
    img = cv2.resize(img, (640,640))

    cv2.imshow("get", img)
    
    if cnt == 3:
        print('Ready!')

    order = cv2.waitKey(1)
    if order == ord('f'):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite('front.png', img)
    if order == ord('r'):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite('right.png', img)
    if order == ord('l'):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite('left.png', img)
        # _, img = cv2.imencode('.png', img)
        # img_code = base64.encodebytes(img).decode('utf-8')
        # img_code = re.sub("\n", "", img_code)
        # text = tar[cnt]
        # data = {"faceType":text, "image":img_code}
        
        # print('send')
        # data = json.dumps(data)
        # cnt += 1
        # response = requests.post('http://34.64.121.28:9090/newface', data = data, headers=headers)
        # print(response)
        # if response["result"] == "ok":
            
        #     embeddings.append(response["embd"])
    
    if order == ord('t'):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        _, img = cv2.imencode('.png', img)
        img_code = base64.encodebytes(img).decode('utf-8')
        img_code = re.sub("\n", "", img_code)
        data = {"embd":embeddings, "image":img_code}

        data = json.dumps(data)

        response = requests.post('http://34.64.121.28:9090/newface', data = data, headers=headers)
        print(response["result"])

    if order == 27:
        break