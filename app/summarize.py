from transformers import AutoTokenizer, BartForConditionalGeneration, PreTrainedTokenizerFast
from konlpy.tag import Mecab
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from collections import Counter
import numpy as np

class summarize:
    def __init__(self, model_name, tokenizer_name):
        self.max_length = 1000
        self.num_beams = 5
        self.length_penalty = 1.2
        if model_name == 'ainize/kobart-news':
            self.tokenizer = PreTrainedTokenizerFast(tokenizer_name)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)
        self.sent_model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
        self.mc = Mecab()
        self.doc_embedding = None
        self.candidate_embeddings = None
        self.candidates = None

    '''
    전달받은 회의 녹취록을 전처리하는 모듈
    예시:
        입력 값: 
        [
            '한나: 안드레아. 미팅에 관한 정보 받았어요?',
            '안드레아: 네, 받았어요. 고객서비스 책임자 핸슨씨가 미팅을 소집하고 날짜를 잡았어요.',
            '안드레아: 안 계신 동안 미팅 안건을 전달하셨어요.',
            '한나: 미팅이 언제죠?',
        ]

        처리 결과:
            names = {'한나': 2, '안드레아':2}
            Scripts = 
            [
                '안드레아. 미팅에 관한 정보 받았어요?',
                '네, 받았어요. 고객서비스 책임자 핸슨씨가 미팅을 소집하고 날짜를 잡았어요.',
                '안 계신 동안 미팅 안건을 전달하셨어요.',
                '미팅이 언제죠?'
            ]
    '''
    
    def prepro(self, doc):
        names = []
        scripts = []
        rec_script = []

        for temp, time in doc:
            name, script = temp.split(':')
            names.append(name)
            scripts.append(script)
            rec_script.append(f'[{name} - {time}]\n{script}')
        
        names = dict(Counter(names))
        rec_script = '\n'.join(rec_script)

        return names, scripts, rec_script

    def get_keywords(self, doc):
        tokenized_doc = self.mc.pos(doc)
        tokenized_nouns = ' '.join([word[0] for word in tokenized_doc if word[1] == 'NNG'])

        # n-gram 추출
        n_gram_range = (2, 3)
        count = CountVectorizer(ngram_range=n_gram_range).fit([tokenized_nouns])
        self.candidates = count.get_feature_names_out()
        self.doc_embedding = self.sent_model.encode([doc])
        self.candidate_embeddings = self.sent_model.encode(self.candidates)

    def mmr(self, doc ,top_n=5, diversity=0.7):
        self.get_keywords(doc)
        
        # 문서와 각 키워드들 간의 유사도가 적혀있는 리스트
        word_doc_similarity = cosine_similarity(self.candidate_embeddings, self.doc_embedding)

        # 각 키워드들 간의 유사도
        word_similarity = cosine_similarity(self.candidate_embeddings)

        # 문서와 가장 높은 유사도를 가진 키워드의 인덱스를 추출.
        # 만약, 2번 문서가 가장 유사도가 높았다면
        # keywords_idx = [2]
        keywords_idx = [np.argmax(word_doc_similarity)]

        # 가장 높은 유사도를 가진 키워드의 인덱스를 제외한 문서의 인덱스들
        # 만약, 2번 문서가 가장 유사도가 높았다면
        # ==> candidates_idx = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10 ... 중략 ...]
        candidates_idx = [i for i in range(len(self.candidates)) if i != keywords_idx[0]]

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

        return [self.candidates[idx] for idx in keywords_idx]

    # 자카드 유사도
    def jaccard_similarity(self, keyword, text):
        key = set(keyword)
        txt = set(text)
        return float(len(key.intersection(txt)) / len(key.union(txt)))

    # 문장 형태소 분리
    def get_pos(self, tokenized_doc):

        return [word[0] for word in tokenized_doc if word[1] == 'NNG']

    def inference(self, dialogue, model_name='alaggung/bart-r3f'):
        self.model.eval()

        if model_name == 'alaggung/bart-r3f':
            inputs = self.tokenizer("[BOS]" + "[SEP]".join(dialogue) + "[EOS]", return_tensors="pt")
            outputs = self.model.generate(
                inputs.input_ids,
                attention_mask=inputs.attention_mask,
                num_beams=self.num_beams,
                length_penalty=self.length_penalty,
                max_length=self.max_length,
                use_cache=True,
            )
            summarization = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return summarization
        elif model_name == '':
            input_ids = self.tokenizer.encode(dialogue, return_tensors="pt")
            # Generate Summary Text Ids
            summary_text_ids = self.model.generate(
                input_ids=input_ids,
                bos_token_id=self.model.config.bos_token_id,
                eos_token_id=self.model.config.eos_token_id,
                length_penalty=2.0,
                max_length=self.max_length,
                min_length=56,
                num_beams=4,
            )
            # Decoding Text
            return self.tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)
    
    def get_summary(self, keyword, text, n_top=5):
        similarity = []
        summary = []
        for key in keyword:
            for txt in text:
                pos = self.get_pos(self.mc.pos(txt))
                similarity.append([txt, self.jaccard_similarity(key.split(), pos)])
        
        similarity.sort(reverse=True, key=lambda x: x[1])
        for text, _ in similarity[:n_top]:
            summary.append(text)
        
        return summary

