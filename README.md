# YAHO (You Are in Home Office)
## 프로젝트 개요
기존의 협업툴을 고도화한 가상 오피스
#### __기획의도__  
팀 프로젝트 진행 시 미팅은 필수적이며, 재택 근무라는 새로운 업무 환경에서는  
개인의 생산성과 더불어 팀이 같은 목표를 공유하는 것이 중요하다고 생각함.  
그래서 미팅을 진행하며 공통의 목표를 설정하고 서로가 어떤 업무를 맡았는지  
공유 및 진척도를 팔로우하며 업무 분담의 투명성을 높여주고, AI 기술을 접목하여  
개인의 업무 효율 또한 높일 수 있는 환경을 제공하는 가상 오피스 구현  
#### __기대효과__  
 1. 사용자 얼굴 인식을 통한 집중 업무 시간 계산으로 개인의 업무 집중도 향상 기대
 2. 미팅 시 팀 프로젝트 보드 작성으로 팀 내 업무 커뮤니케이션의 명확성과 투명성 확보 가능
 3. 프로젝트 단위 별 미팅 히스토리 저장으로 follow-up 미팅의 경우 업무 시간 단축
 4. 팀 미팅 시 배정받은 업무를 토대로 개인 to-do 리스트를 세분화하고 개인의  
일별/주별/월별 리포트를 통해 사용자의 성취감과 업무 능률 향상 기대  
## 팀원 소개  
|AI|AI|AI|NET|XR|XR|
| :---: | :---: | :---: | :---: | :---: | :---: |
|👑[권구영](https://github.com/kgy94329)|[김규영](https://github.com/qyeongkim)|[이한결](https://github.com/AIHanGyeol)|[노재원](https://github.com/NJWonE)|[나병한](https://github.com/svcbn)|[이예담](https://github.com/yelee12)|
## 사용 기술(AI)
(이탤릭 볼드체는 제가 구현한 기능입니다.)

### Speech to Text
담당: [권구영](https://github.com/kgy94329), [이한결](https://github.com/AIHanGyeol)  
- ************문제점************
    - Kospeech라는 STT모델을 이용하기 위해 사전 학습된 모델을 활용하였으나 정확도가 너무 낮음
    - 추가 학습을 위해 데이터를 수집하고 학습을 시도하였으나 학습에 필요한 리소스가 부족하여 다른 모델을 찾기로 함
    - __*구글 클라우드의 Streaming STT 모델을 활용하기 위해 API key를 얻어서 Unity에 내장하였으나 한국어 모델은 화자가 말을 끊는 시점을 정확히 파악하지 못해 원활한 회의록을 얻기에 어려움이 있었음*__
    - __*문제 해결을 위해 코드를 확인하고 구글의 도큐멘트를 확인하였으나 구글 모델 자체의 문제인것으로 확인되어 Naver STT API를 활용하기로 함*__
- *__Naver가 제공하는 C#코드를 Unity에 내장시킴*__
- 회의중 발화자는 마이크 on/off 버튼으로 자신의 발언을 녹음하고 녹음이 종료되면 Naver STT API로 전송되어 text 데이터를 받아온다.
- 회의가 종료되면 수집된 text 데이터들을 시간순에 따라 재배열하여 회의록으로 저장한다.

### 추출요약 기능
담당: [권구영](https://github.com/kgy94329)  
[참고문서]: [딥러닝과 Maximal Marginal Relevance를 이용한 2단계 문서 요약](http://koreascience.or.kr/article/CFKO201930060772845.pdf)  
- __*작성된 회의록을 Konlpy의 Mecab을 활용하여 형태소 단위로 분리*__
- __*MMR(Maximal Marginal Relevance) 알고리즘을 활용하여 회의 주제와 관련성이 높으면서도 중복되지 않는 단어들을 추출*__
- __*추출된 단어들과 자카드 유사도를 활용하여 회의록으로부터 중요 문장을 추출*__

### 사용자 인식 기능
담당: [이한결](https://github.com/AIHanGyeol), [김규영](https://github.com/qyeongkim)  
- **문제점**
    - __*유저가 현재 근무중인지 파악하기 위해 Object Detection모델인 YOLOv7을 학습시킴*__
    - __*사람들 사진 약 900장의 데이터를 인터넷에서 크롤링하여 Roboflow에서 사람들의 얼굴을 디텍시키기 위한 전처리를 진행*__
    - __*모델을 학습시키고 웹캠을 통해 얼굴을 탐지하는 테스트를 진행했을 때 얼굴을 잘 탐지하였으나, 유저 이외의 다른 사람들의 얼굴도 함께 탐지하여 유저가 아닌 다른 사람이 자리에 앉아 있어도 부재중 표시가 뜨지 않는 문제를 확인*__
    - InsightFace 모델을 onnx로 만들어 Unity에 내장시키고자 하였으나, 추론 코드를 C#으로 옮기는 과정에서 실패
- 얼굴 인식에 가장 높은 성능을 가지고 있고 별도의 학습 필요 없이 사전 학습된 모델을 활용한 InsightFace를 활용하기로 함
- 유저의 정면 사진 1장을 가지고 테스트 하였을 때 좌, 우 사진을 입력해도 **0.5 이상의 유사도**를 도출하였고 다른 사람의 사진을 입력하면 **0.3 이하의 유사도**를 도출하는 것을 확인함
- 웹캠을 활용하여 **실시간 인식**을 시도하였을 때 프레임은 **약 평균 25프레임**의 우수한 성능을 보여주었으나 Unity에서 실시간 웹캠을 켜두는 것은 클라이언트 부분에서 많은 리소스가 소모될것으로 생각되어 10초에 1장의 사진을 촬영하는것으로 AI결정함

### AI 서버 운용
- __*AWS EC2 인스턴스에 AI서버를 구축*__
    - 요금 문제로 서버 종료
- __*GCP(Google Cloud Platform)의 Compute Engine 인스턴스에 AI 서버 구축*__


## 프로젝트 주요 기능

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/534a92cf-c1fc-4957-8fd6-6001f107c1ad/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/db2da2a4-4918-4581-8bd3-126e537c18fc/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/4061c77c-28b9-4c4b-99c7-c438c459755c/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/27869508-f91b-4640-8a46-2dc8b63b5647/Untitled.png)

## 시스템 구상도
![image](https://user-images.githubusercontent.com/58832219/205869539-147768c2-52e8-4c46-aa4f-e0c5852d8da0.png)
## 스토리보드
![image](https://user-images.githubusercontent.com/58832219/205870123-1e98cd2c-83d4-4ffa-92b2-7f0167593cbe.png)
![image](https://user-images.githubusercontent.com/58832219/205870287-84893f54-c897-49ce-aac2-6a2575ac28d0.png)
![image](https://user-images.githubusercontent.com/58832219/205870415-3c318784-b8b9-481a-98d7-45c82f88a4c5.png)
