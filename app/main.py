'''
    File: main.py
    Author: Guyong Kwon, Hangyul Lee
    Date: 2022-11-21
    Note:
        서버로부터 데이터를 받아 AI처리를 수행하는 모듈
        AI기능
        1. 회의 대화 내용 데이터로부터 키워드 추출
        2. 추출된 키워드를 활용하여 추출요약 진행
        3. 입력받은 유저 사진 이미지가 정면인지 측면인지 체크
        4. 1분마다 한 장의 사진을 입력받고 유저가 있는지 없는지 체크

        그 외 기능
        1. 회의 대화 참여율 그래프 작성
'''
from flask import Flask , Response, request
import base64
import numpy as np
import graph_drawer as gd
import face_detector
import summarize
import jsonpickle
import cv2

## GET : 자료를 요청할 때 사용.
## POST : 자료를 생성을 요청할 때 사용.
## PUT : 자료의 수정을 요청할 때 사용.
## DELETE : 자료의 삭제를 요청할 때 사용.

app = Flask(__name__)

model_name = 'alaggung/bart-r3f'
summarizer = summarize.summarize(model_name , model_name )

def meeting_process(data):
    pe_count, doc, rec_script = summarizer.prepro(data)
    
    # 키워드 생성
    keyword = summarizer.mmr(''.join(doc))
    
    # 그래프 생성
    gd.draw(pe_count.values(), pe_count.keys())
    img = get_graph()

    # 요약문 생성
    summary = summarizer.get_summary(keyword, doc)
    return img, rec_script, keyword, summary

def get_graph(status="normal"):
    # 정상적인 그래프가 출력되지 않으면 no_graph이미지를 생성
    # 생성된 이미지를 base64로 인코딩하여 전송
    if status == "normal":
        img = cv2.imread('1.png', cv2.IMREAD_COLOR)
    else:
        img = cv2.imread('no_graph.png', cv2.IMREAD_COLOR)
        
    _, img = cv2.imencode('.png', img)
    img = base64.encodebytes(img).decode('utf-8')
    return img

def daily_process(do,undo, labels=['Do', 'Undo']):
    gd.draw([do, undo], labels, wedgeprops=None)
    img = get_graph()
    return img

def decode_img(data):
    # 전송받은 이미지를 디코딩
    img = base64.b64decode(data)
    nparr = np.fromstring(img, dtype=np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

@app.route('/meeting', methods=['POST'])
def meeting_data():
    if request.method == 'POST':
        req = request.get_json()
        data = []
        print('리퀘스트를 받았습니다.')
        for i in req['conversation'][0]:
            data.append([f'{i["name"]}:{i["text"]}', i["time"]])

        img, rec_script, keyword, summary = meeting_process(data)
        
        # response 생성
        response = {"graph":img, "record":rec_script, "keyword":keyword, "summary":summary}
        response = jsonpickle.encode(response)
        print('response를 보냅니다.')
        return Response(response=response , status = 200 , mimetype='application/json')
    return 'Got wrong request' 

@app.route('/daily', methods=['POST'])
def daily_data():
    if request.method == 'POST':
        req = request.get_json()

        print('리퀘스트를 받았습니다.')
        checkCount = req['checkCount'][0]
        totalCount = req['totalCount'][0]
        if totalCount == checkCount and chechCount == 0:
            img = get_graph('no_graph')
        else:
            img = daily_process(checkCount, (totalCount - checkCount))
        
        # response 생성
        response = {"graph":img}
        response = jsonpickle.encode(response)
        print('response를 보냅니다.')
        return Response(response=response , status = 200 , mimetype='application/json')
    return 'Got wrong request' 

@app.route('/facedetect', methods=['POST'])
def detect():
    if request.method == 'POST':
        req = request.get_json()

        print('리퀘스트를 받았습니다.')
        target = req['img'][0]
        img = decode_img(target)
        embedding = req['embd'][0]

        result = face_detector.check_image(img, embedding)
        return result

@app.route('/newface', methods=['POST'])
def face_data():
    if request.method == 'POST':
        req = request.get_json()

        print('리퀘스트를 받았습니다.')
        check = req['text'][0]
        img_code = req['img'][0]
        img = decode_img(img_code)
        
        result, embedding_list = face_detector.make_base_image(check, img)
        if embedding_list != None:
            response = {'result':result, 'embd':embedding_list}
            response = jsonpickle.encode(response)
            return Response(response=response , status = 200 , mimetype='application/json')
        else:
            return result

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port = 9090)

