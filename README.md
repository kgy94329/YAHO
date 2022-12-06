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
### 1. Face recognition
담당: [이한결](https://github.com/AIHanGyeol), [김규영](https://github.com/qyeongkim)  

* [InsightFace](https://github.com/deepinsight/insightface)모델을 활용한 얼굴 인식 적용  
- 유저의 정면, 좌측면, 우측면 얼굴사진으로부터 특징벡터를 추출하고 데이터베이스에 저장
    - 미간 좌표값과 코 끝의 좌표값을 이용하여 사진이 정면인지 측면인지 판별
    - 정면 사진에서 추출한 특징벡터 하나만으로도 꽤 정확한 결과를 보여주지만 좀 더 확실한 결과를 얻기 위해 측면 사진을 추가로 등록
- 1분에 한 번씩 유저의 사진을 촬영하고 얼굴 특징벡터를 추출하여 데이터베이스에 저장된 특징벡터와 코사인 유사도를 계산
- 코사인 유사도가 0.4이상이면 본인이라고 볼 수 있다.
### 2. Text Summarization
담당: [권구영](https://github.com/kgy94329)  
[참고문서]: [딥러닝과 Maximal Marginal Relevance를 이용한 2단계 문서 요약](http://koreascience.or.kr/article/CFKO201930060772845.pdf)
* Konlpy의 Mecab을 활용하여 문서의 형태소를 분리하고 명사만을 추출
* 추출된 명사를 Sci-kit learn의 CountVectorizer를 활용하여 핵심 키워드를 추출
  * 중요 단어라고 판단되는 단어들이 중복되어 추출됨
* MMR(Maximal Marginal Relevance)를 활용하여 문서와 유사하면서도 중복되지 않는 단어 후보들을 추출
  * 문서 주제와 관련성이 높은 문장을 선택하면서도 이전에 선택된 문장들에 대한 유사도가 낮은  
  문장을 선택하여 선택된 문장들간의 정보 중복 문제를 해결할 수 있는 기법
* 문서의 문장마다 형태소를 분리하고 자카드 유사도를 활용하여 핵심 키워드가 많이 포함된 문장들을 추출
## 시스템 구상도
![image](https://user-images.githubusercontent.com/58832219/205869539-147768c2-52e8-4c46-aa4f-e0c5852d8da0.png)
## 스토리보드
![image](https://user-images.githubusercontent.com/58832219/205870123-1e98cd2c-83d4-4ffa-92b2-7f0167593cbe.png)
![image](https://user-images.githubusercontent.com/58832219/205870287-84893f54-c897-49ce-aac2-6a2575ac28d0.png)
![image](https://user-images.githubusercontent.com/58832219/205870415-3c318784-b8b9-481a-98d7-45c82f88a4c5.png)
