from transformers import AutoTokenizer, BartForConditionalGeneration
import numpy as np
import itertools

from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from flask import Flask
from flask import request
from flask import render_template
import requests
import json
# import MeCab


## GET : 자료를 요청할 때 사용.
## POST : 자료를 생성을 요청할 때 사용.
## PUT : 자료의 수정을 요청할 때 사용.
## DELETE : 자료의 삭제를 요청할 때 사용.


app = Flask(__name__)


# 모델 설정값
model_name = "./model-155epoch-102180steps-0.4105loss-0.9423acc"
tokenizer_name = "alaggung/bart-r3f"
max_length = 200
num_beams = 5
length_penalty = 1.2
mc = Okt()


# 요약 추론 모델
def inference(dialogue):
    tokenizer = AutoTokenizer.from_pretrained("resources/tokenizers/unigram_4K")
    model = BartForConditionalGeneration.from_pretrained(model_name)
    model.eval()
    print(model.eval())
    inputs = tokenizer("[BOS]" + "[SEP]".join(dialogue) + "[EOS]", return_tensors="pt")
    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        num_beams=num_beams,
        length_penalty=length_penalty,
        max_length=max_length,
        use_cache=True,
    )
    summarization = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summarization

def mmr(doc_embedding, candidate_embeddings, words, top_n, diversity):

    # 문서와 각 키워드들 간의 유사도가 적혀있는 리스트
    word_doc_similarity = cosine_similarity(candidate_embeddings, doc_embedding)

    # 각 키워드들 간의 유사도
    word_similarity = cosine_similarity(candidate_embeddings)

    # 문서와 가장 높은 유사도를 가진 키워드의 인덱스를 추출.
    # 만약, 2번 문서가 가장 유사도가 높았다면
    # keywords_idx = [2]
    keywords_idx = [np.argmax(word_doc_similarity)]

    # 가장 높은 유사도를 가진 키워드의 인덱스를 제외한 문서의 인덱스들
    # 만약, 2번 문서가 가장 유사도가 높았다면
    # ==> candidates_idx = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10 ... 중략 ...]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    # 최고의 키워드는 이미 추출했으므로 top_n-1번만큼 아래를 반복.
    # ex) top_n = 5라면, 아래의 loop는 4번 반복됨.
    for _ in range(top_n - 1):
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

        # MMR을 계산
        mmr = (1-diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        # keywords & candidates를 업데이트
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [words[idx] for idx in keywords_idx]

# 자카드 유사도
def jaccard_similarity(keyword, text):
    key = set(keyword)
    txt = set(text)
    return float(len(key.intersection(txt)) / len(key.union(txt)))  

# 문장 형태소 분리
def get_pos(sentence):
    tokenized_doc = mc.pos(sentence)
    # print(tokenized_doc)
    return [word[0] for word in tokenized_doc if word[1] == 'Noun']

# 키워드 분석repo_name
def keyword_analyze(doc):
    
    tokenized_doc = mc.pos(doc)
    tokenized_nouns = ' '.join([word[0] for word in tokenized_doc if word[1] == 'Noun' and word[0] != '안드레아']) 

    n_gram_range = (2, 3)

    count = CountVectorizer(ngram_range=n_gram_range).fit([tokenized_nouns])
    candidates = count.get_feature_names_out()
    model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
    doc_embedding = model.encode([doc])
    candidate_embeddings = model.encode(candidates)
    keyword = mmr(doc_embedding, candidate_embeddings, candidates, top_n=5, diversity=0.7)
    return keyword


@app.route('/', methods=['POST'])
def render_file():
    if request.method == 'POST': 
        # print(request.form)
        datas = request.get_json()
        doc = []
        for i in datas:
            # print(i['name'] + ' : ' + i['text'])
            # print(i['text'])
            # pos = get_pos(i['text'])
            # sim = jaccard_similarity(key.split(), pos)
            

            doc.append(f'{i["name"]} : {i["text"]}')
            # # print(txt)
            # print('--원본 스크립트--')
            # print(f'{i["name"]} : {i["text"]}')
            # print('---요약본---')
        print('\n'.join(doc))
        result = keyword_analyze('\n'.join(doc))
        print(result)
    


            
        return result
    return 'haha'

#ver2,,insert queue
@app.route('/uploader')
def uploader():        
    response = requests.post()
    return 'connected!!'
    
if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0' , port = 9090)




# @app.route('/upload', methods=['POST'])
# def render_file():
#     if request.method == 'POST':
#         datas = request.get_json()['data']
#         print(datas)
        
#         return '받았습니다!!!'
#     return 'haha'
    # return render_template('upload.html')

