from flask import Flask , Response, request
from collections import Counter
import base64
import requests
import json
import one_graph as og
import summarize
import jsonpickle
import cv2


## GET : 자료를 요청할 때 사용.
## POST : 자료를 생성을 요청할 때 사용.
## PUT : 자료의 수정을 요청할 때 사용.
## DELETE : 자료의 삭제를 요청할 때 사용.


app = Flask(__name__)


model_name = 'alaggung/bart-r3f'
# model_name = 'ainize/kobart-news'

summarizer = summarize.summarize(model_name , model_name )

def process(data):

    pe_count, doc, rec_script = summarizer.prepro(data)

    # 키워드 생성
    print(''.join(doc))
    keyword = summarizer.mmr(''.join(doc))

    # 그래프 생성
    og.one_graph(pe_count.values(), pe_count.keys())
    img = cv2.imread('1.png', cv2.IMREAD_COLOR)
    img = cv2.resize(img, (120, 120))
    _, img = cv2.imencode('.png', img)
    img = base64.encodebytes(img).decode('utf-8')

    # 요약문 생성
    summary = summarizer.get_summary(keyword, doc)
    return img, rec_script, keyword, summary    

@app.route('/summarize', methods=['POST'])
def render_file():
    global cnt, date, data
    if request.method == 'POST':
        req = request.get_json()
        data = []
        #print(f'data: {data}')
        print('리퀘스트를 받았습니다.')
        print(req)
        for i in req['conversation'][0]:
            data.append([f'{i["name"]}:{i["text"]}', i["time"]])

        img, rec_script, keyword, summary = process(data)
        print('response를 보냅니다.')
        # response 생성
        response = {"graph":img, "record":rec_script, "keyword":keyword, "summary":summary}
        response = jsonpickle.encode(response)

        return Response(response=response , status = 200 , mimetype='application/json')
    return 'Got wrong request' 



if __name__ == '__main__':
    app.run(host='0.0.0.0' , port = 9090)

