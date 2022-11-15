import model_ as md
from flask import Flask , Response
from flask import request
from flask import render_template
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
cnt = 0
date = ""
member = 0
data = []

# 보낼 값들
pe_count = None
rec_script = None
keyword = None
img = None

def process():
    global data, summary, rec_script, keyword, img, pe_count

    pe_count, doc, rec_script = summarizer.prepro(data)

    # 키워드 생성
    keyword = summarizer.mmr(''.join(doc))

    # 그래프 생성
    og.one_graph(pe_count.values(), pe_count.keys())
    img = cv2.imread('1.png', cv2.IMREAD_COLOR)
    img = cv2.resize(img, (120, 120))
    _, img = cv2.imencode('.png', img)
    img = base64.encodebytes(img).decode('utf-8')

    # 요약문 생성
    summary = summarizer.get_summary(keyword, doc)

@app.route('/send', methods=['GET'])
def send_result():
    global summary, rec_script, keyword, img, date, pe_count
    
    print('response를 보냅니다.')
    # response 생성
    req = {"date":date, "graph":img, "text":rec_script, "keyword":keyword, "summary":summary, "members":list(pe_count.keys())}
    req = jsonpickle.encode(req)

    return Response(response=req, status = 200 , mimetype='application/json')
    

@app.route('/summarize', methods=['POST'])
def render_file():
    global cnt, date, data
    if request.method == 'POST':
        req = request.get_json()
        cnt += 1

        #print(f'data: {data}')
        print('리퀘스트를 받았습니다.')
        
        for i in req['scripts']:
            data.append([f'{i["name"]}:{i["text"]}', i["time"]])
        
        if cnt < member:
            return "Got data"
        elif cnt == member:
            data.sort(key=lambda x:x[1])
            process()
        
            #print('response를 보냅니다.')
            # response 생성
            #response = {"date":date, "graph":img, "text":rec_script, "keyword":keyword, "summary":summary}
            #response = jsonpickle.encode(response)

            #return Response(response=response , status = 200 , mimetype='application/json')
            # return "Done"
        return "Done"
    return 'Got wrong request' 

@app.route('/info', methods=['POST'])
def counter():
    global member, date
    if request.method == 'POST':
        date, member = "", 0
        req = request.get_json()
        
        member = req['count']
        date = req['date']
        
        return "Got information of meeting"


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port = 9090)

