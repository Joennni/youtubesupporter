import sqlite3
import os
import pandas as pd
import time
from datetime import datetime
import keyboard
import pyautogui
import pickle

from konlpy.tag import Okt
# from soninsik_sen import sentiment_predict
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
okt = Okt()

import tensorflow as tf
from  tensorflow.keras.models import load_model
model = tf.keras.models.load_model('C:/Users/HAEDONG/yolov5/lstm_sentiment.h5')
loaded_model = load_model('C:/Users/HAEDONG/Youtube_Support_core/lstm_model.h5')


# 시간대 설정
now = datetime.now()
today = now.date()
current_time = now.strftime("%H:%M:%S")
current_time2 = now.strftime("%H_%M_%S")
count1 = 0
count2 = 0

        

        
with open('./tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
    
with open('./tokenizer2.pickle', 'rb') as handle2:
    tokenizer2 = pickle.load(handle2)
        
        
def sentiment_predict(new_sentence):
        new_token = [word for word in okt.morphs(new_sentence) if not word in stopwords] 
        new_sequences = tokenizer.texts_to_sequences([new_token])
        new_pad = pad_sequences(new_sequences, maxlen = 80)
        score = float(model.predict(new_pad))

        if score > 0.5:
            result = (f'positive({score*100 :.2f})')
            print(result)
        else : 
            result = (f'negative({(1-score)*100 :.2f})')
            print(result)


        return result
    
def modelfitting(a):
    import pandas as pd
    b = pd.DataFrame()
    b['document'] = [a]
    b = b['document']
    import numpy as np
    # 한글과 공백을 제외하고 모두 제거
    b = b.str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 A-Z a-z]","")
    # 빈 문장 제거
    b.replace('', np.nan, inplace=True)
    b = b.dropna(how='any')
    # 토큰화
    from konlpy.tag import Okt
    okt = Okt()
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '을','에서','에게','로',
                '으로', '자' ,'에' , '와' , '한', '하다']
    X_train2 = []
    for sentence in b:
        tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
        stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
        X_train2.append(stopwords_removed_sentence)
    X_train = tokenizer2.texts_to_sequences(X_train2)

    from tensorflow.keras.preprocessing.sequence import pad_sequences
    X_train = pad_sequences(X_train, maxlen = 25)
    dftt = X_train.copy()
    y_test = loaded_model.predict(dftt)
    test_eval = []
    if np.argmax(y_test) == 0:
        test_eval.append("기쁨")
    elif np.argmax(y_test) == 1:
        test_eval.append("당황")
    elif np.argmax(y_test) == 2:
        test_eval.append("분노")
    elif np.argmax(y_test) == 3:
        test_eval.append("불안")
    elif np.argmax(y_test) == 4:
        test_eval.append("상처")
    elif np.argmax(y_test) == 5:
        test_eval.append("슬픔")
    
    return test_eval[0]

# def loop11(keyboard_input):
#     if keyboard.is_pressed('shift'):
#         if keyboard.is_pressed('w'):
        
while True:
    
    connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
    Cursor = connect.cursor()
    Cursor.execute("SELECT question_contents FROM board_question where predict is null ORDER BY ROWID DESC LIMIT 1")
    MM=Cursor.fetchone()
    print(MM)
    Cursor.execute("SELECT answer_contents FROM board_answer where predict is null ORDER BY ROWID DESC LIMIT 1")
    AA=Cursor.fetchone()
    print(AA)
    
    
    if MM == None:
        print("변환할 게시글 데이터 없음")
        Cursor.close()
        connect.close()
        count1 += 1

        
    if AA == None:
        print('변환할 답변 데이터 없음')
        connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
        Cursor = connect.cursor()
        Cursor.close()
        connect.close()
        count2 += 1
        
    if MM:
        connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
        Cursor = connect.cursor()
        MM=MM[0]
        print(MM)
        result=sentiment_predict(MM)
        result2 = modelfitting(MM)
        print(result,result2)
        Cursor.execute("UPDATE board_question SET predict = ? WHERE question_contents = ?", (result + ' // '+result2, MM))
        connect.commit()
        print("업데이트 완료")

        Cursor.execute("UPDATE board_question SET question_contents = ? WHERE question_contents = ?", (MM+' 감성분석 결과 : '+result + ' // '+ result2, MM))

        connect.commit()
        print("업데이트 완료2")
        Cursor.close()
        connect.close()

    if AA:
        connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
        Cursor = connect.cursor()
        AA=AA[0]
        print(AA)
        result=sentiment_predict(AA)
        result2=modelfitting(AA)
        print(result,result2)
        Cursor.execute("UPDATE board_answer SET predict = ? WHERE answer_contents = ?", (result + ' // '+result2, AA))
        connect.commit()
        print("업데이트 완료")

        Cursor.execute("UPDATE board_answer SET answer_contents = ? WHERE answer_contents = ?", (AA+'// 감성분석 결과 : '+result + ' // '+result2, AA))

        connect.commit()
        print("업데이트 완료2")
        Cursor.close()
        connect.close()
    # count1 = max(3, count1)
    # count2 = max(3, count2)
    
    print(count1, count2)
                    
    # if MM == None and AA == None and count1 >= 3 and count2 >= 3:
    #     print("더이상 변환할 데이터가 없어 데이터 베이스를 최신화 시킵니다")
    #     count1 = 0
    #     count2 = 0
        
    #     pyautogui.click(-2742, 2295, clicks=2 , interval=0.5) # x 100, y 200 위치로 바로 이동
    #     time.sleep(0.5)

        
        
    time.sleep(1)
    print('재시작')
                    