
# &#128104;&#127995;&#8205;&#128187; YOUTUBE SUPPORTER <a href = "http://gmrain.synology.me:8080/"><img src="https://img.shields.io/badge/www.u_tube_spt.com-0000CC?style=flat-square&logo=logo&logoColor=white"/></a>

## 1. 프로젝트 소개
### 개요:   
유튜브는 남녀노소 전세계 사람들이 정보를 공유하고 일상의 한부분이 될 정도로 인기가 많은 동영상 사이트이다. 특히 최근 유튜버 마케팅이 고전적인 광고보다 소비자들에게 많이 사랑받고 있기 때문에 유튜브를 기업에서도 무시할 수 없다. 하지만 많은 사람들이 이용하는 만큼 다양한 댓글이 달리고 사용자들의 반응을 파악하기가 쉽지 않다.   
"youtube supporter"는 유튜브를 통해 산업을 파악해야하는 사용자들에게 쉽게 트렌드를 파악할 수 있도록 돕기 위해 기획하게 됐다.   

- 객체 인식을 통해 사용자가 크롤링한 정보를 사용자별로 저장
- 손제스처를 통해 쉽게 유튜브의 정보를 수집
- 유튜브 댓글의 감성을 분석해 긍/부정을 쉽게 파악
- DB로 데이터 자동 저장
- 조회가 편리한 웹사이트

### 예상 효용:   
- 직원들의 피로도 감소
- 데이터 필터링을 통한 원하는 정보만 추출
- 트렌드 파악 용이



## 2. 팀원 소개 &#128104;&#8205;&#128105;&#8205;&#128103;&#8205;&#128103;
### &#127940;&#127995; 정소현  (gmrain@naver.com)
역할: 객체인식, 동작인식, DB구축  

### &#129318;&#127995; 오상아 (allesgute89@naver.com)
역할: DB구축, 웹페이지 제작

### &#129464;&#127995; 장민희 (lool_0803@naver.com)
역할: 감성분석, 보고서 작성

### &#128037; 문지현 (gomdori1027@naver.com)
역할: 유튜브 크롤링, 감성분석, 보고서 작성

## 3. 프로그램  
### 프로그램 설명:  
"youtube supporter"는 크게 객체인식과 동작인식으로 진행된다.   
객체인식을 통해 사용자를 파악하여 해당 사용자의 정보를 가져와 DB에 연결하고 유저의 동작을 인식해 동작에 맞는 기능을 수행 후 데이터를 저장한다.  
이는 웹페이지에 실시간으로 연동되어 조회를 통해 열람 가능하다.  

### 프로그램 사용기술  
#### 1) 객체 인식:  
유저의 얼굴을 학습하여 객체를 분류한다. 유저가 직접 로그인을 하지 않아도 프로그램이 유저의 정보를 스스로 저장한다.  

- 진행 방법:  
사용모델:  YOLO v5  
모델 선택 이유:   
첫 번째로 객체 탐지 모델 중 이미지를 한 번만 보는 특징으로 맥락적 이해도가 높다. 두 번째는 기존의 R-CNN보다 6배 빠른 성능을 보여주며 이를 통해 실시간으로 객체 탐지를 가능하게 했다. 또한 통합된 모델을 사용하여 간단하다. 마지막으로 YOLO의 버전 중 v4보다 환경 구성과 구현이 쉽기 때문에 버전을 선택했다. 

- 한계점:  
데이터를 학습시키는 과정이 필요하여 직원들의 얼굴을 인식시키기 위해서는 많은 데이터가 라벨링이 된 상태로 필요하다. 

#### 2) 동작 인식:  

<img src="/image_git/MediaPipe.gif" width="300" height="400">

유저의  손동작에 따른 기능을 수행한다. 데이터 수집을 위한 다양한 처리를 대신 해준다.   

|동작|구현 기능|
|--|--|
|<img src="/image_git/g_capture.jpg" width="100" height="100">|유튜브 화면캡쳐|
|<img src="/image_git/g_stop.jpg" width="100" height="100">|유튜브 일시정지/재생|
|<img src="/image_git/g_comment.jpg" width="100" height="100">|유튜브 댓글 크롤링 & 감성분석|
|<img src="/image_git/g_htag.jpg" width="100" height="100">|유튜브 해시태그 크롤링|
|<img src="/image_git/g_script.jpg" width="100" height="100">|유튜브 자막 & 타임스탬프 크롤링|
|shift+A <img src="/image_git/g_volume.jpg" width="200" height="100">|볼륨 조절|



-  진행 방법:  
사용모델: Mediapipe  
모델 선택 이유:   
Google에서 공개한 MediaPipe는 비디오 형식 데이터를 이용한 다양한 비전 AI기능을 파이프라인 형태로 제공하는 AI 프레임워크이다. 모델 용량이 작고 속도가 빠르다는 장점이 있어 선택했다. 또 전용카메라없이 일반카메라를 이용해 사용할 수 있다. MediaPipe에는 여러가지 모델이 있는데 이번 프로젝트에서는 손가락과 손의 위치를 알려주는 모델을 이용하였다.
제스처를 감지하기 위해서 손가락 별 노드 길이에 따른 손가락 접힘 감지 논리코드를 구현하였다.

-  한계점:
손이 카메라에 계속해서 노출되어 감지되고 있으므로 원하는 때에 적절하게 명령어를 수행하기 위해서는 활성화 키(Shift + C )가 필요했는데 차후에 손동작만으로 가능하면 더욱 편의성이 개선되어 질 것으로 기대한다.

#### 3) 댓글 감성 분석:  
<img src="/image_git/example_sentiment.png" >

감성분석 시각화 모습 (약한긍정/긍정/약한부정/부정)  
<img src="/image_git/piegraph2.png" width="400" height="430">  
감성분석은 텍스트 문서의 감성을 분류하는 문서 분류로 텍스트 문서에서 감성을 긍정 혹은 부정으로 분류하는 분석으로 자연어 처리 중 한 분야이다. 딥러닝을 이용한 감성 분석 방법론은 문서를 토큰화 후 임베딩을 통해 문장벡터를 얻는 과정과 벡터화된 문서를 분류하는 과정으로 나눌 수 있다.  
감성 분석은 감성을 분류하고, 더 나아가 감성 분석의 결과를 이용해 여론을 분석하는 오피니언 마이닝 분야에서 응용된다. 
 (오영택, 김민태, 김우주. (2019). Parallel Stacked Bidirectional LSTM 모델을 이용한 한국어 영화리뷰 감성 분석. 정보과학회논문지, 46(1)) 

유튜브 댓글의 여론을 분석해 여론을 분석하고 피드백을 받을 수 있다. 

-  진행 방법:  
최종 사용 모델: Keras의 LSTM 사용

모델 선택 이유: 
LSTM모델은 Long Short Term Memory의 줄임말로 주로 시계열 처리나 자연어 처리때 사용한다. 
여러 모델을 사용해 비교해 본 결과 다른 기술과도 호환이 쉬웠다. 특히 파이썬의 버전과 넘파이 버전에서 충돌을 일으키지 않고 모델을 불러 올 수 있었다. 
또한 문맥을 파악해야 하고 긴 문장이 많은 유튜브 댓글 특성상 긴 문장 댓글을 문맥의 정보를 저장하고 긴 문장 처리에 용이해 모델을 선택하게 되었다. 

#### 사용한 모델 비교:
|사용 모델|장점|단점|정확도 (test)|
|--|--|--|--|
Logistic Regression|1. 구현이 용이 2. 속도와 예측이 빠름|선형관계를 전제로 한 모델이라 예측력이 떨어짐|0.8619|
KoBert|1. 높은 정확도2. 문맥에 대한 정보 저장|호환성의 문제로 사용 불가|0.8902|
LSTM|1. 다른 기술과 높은 호환성 2. 긴 문장 처리에 용이 3. 문맥에 대한 정보 저장|정확도가 모델 중 낮음|0.8602|

- 한계점:  
직접 데이터 라벨링 하는 건 비효율적이라 기존에 존재하던 ‘네이버 영화 리뷰’데이터를 사용하였고 유튜브 댓글과는 성격이 다르다는 특징이 있었다.  
자유롭게 댓글을 쓸 수 있다는 유튜브의 특성상 광고 댓글이나 맥락이 없는 무의미한 댓글(예: 1빠!)이 존재했고 맞춤법이나 비문이 많아 분석의 정확도 부분에서 한계점이 존재했다.  

#### 4) 게시판 감성분석  
다중분류 감성분석을 진행했다.  댓글 감성분석에서 두 가지 감정이 아닌 더 세분화된 감정 6개를 내놓는다. 
-  진행 방법:  
최종 사용 모델: Keras의 양방향 LSTM 사용

모델 선택 이유: 
LSTM모델은 Long Short Term Memory의 줄임말로 주로 시계열 처리나 자연어 처리때 사용한다. 
양방향 모델을 사용한 이유는 다중분류로 정확도가 이전의 LSTM보다 낮았고 과적합이 쉽게 일어났다. 

감성분석 시각화 모습 (기쁨/당황/분노/불안/상처/슬픔)
<img src="/image_git/Board_sentiment.png" > 

#### 5) 웹페이지 제작:  
객체, 동작인식을 통해 DB에 저장되어 있는 정보를 실시간으로 집계하여 조회할 수 있으며, 집계된 데이터별 시각화 자료를 볼 수 있다.
- 사용자 전체 크롤링 수집 카운트 집계 조회 화면 구현
- 집계 항목별 시각화 그래프 조회
- 사용자별 상세 크롤링 컨텐츠 조회
- 댓글 별 감성분석 결과 조회
- 검색창을 통한 항목별 결과 조회 및 조회결과에 대한 감정분석 시각화 그래프 화면 구현


### 프로그램 기능 설명
##### 1) 데이터 수집 :   
크롤링(제목, 댓글, 해시태그, 자막)
화면 캡쳐

#### 2) 데이터 저장 :  
SQLite

#### 3) 데이터 처리 :   
감성분석, 시각화


### 프로그램 활용 계획:  
홈페이지를 통한 서비스 제공  
#### 홈페이지 주소: http://gmrain.synology.me:8080


## 4. 프로젝트 수행 결과 분석
결과물 설명(관련 이미지 첨부)
문제점
개선 방안 및 고찰

