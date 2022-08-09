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
    Cursor.execute("SELECT 사람문장1, 감정_대분류 FROM test_db where 사람문장1 is not null and 사람문장1예측 is null ORDER BY ROWID DESC LIMIT 1")
    MM1=Cursor.fetchone()
    print(MM1)
    Cursor.execute("SELECT 사람문장2, 감정_대분류 FROM test_db where 사람문장2 is not null and 사람문장2예측 is null ORDER BY ROWID DESC LIMIT 1")
    MM2=Cursor.fetchone()
    print(MM2)
    Cursor.execute("SELECT 사람문장3, 감정_대분류 FROM test_db where 사람문장3 is not null and 사람문장3예측 is null ORDER BY ROWID DESC LIMIT 1")
    MM3=Cursor.fetchone()
    print(MM3)
    Cursor.execute("SELECT 기계문장1, 감정_대분류 FROM test_db where 기계문장1 is not null and 기계문장1예측 is null ORDER BY ROWID DESC LIMIT 1")
    MM4=Cursor.fetchone()
    print(MM4)
    Cursor.execute("SELECT 기계문장2, 감정_대분류 FROM test_db where 기계문장2 is not null and 기계문장2예측 is null ORDER BY ROWID DESC LIMIT 1")
    MM5=Cursor.fetchone()
    print(MM5)
    Cursor.execute("SELECT 기계문장3, 감정_대분류 FROM test_db where 기계문장3 is not null and 기계문장3예측 is null ORDER BY ROWID DESC LIMIT 1")
    MM6=Cursor.fetchone()
    print(MM6)
    
    
    # if MM == None:
    #     print("변환할 게시글 데이터 없음")
    #     Cursor.close()
    #     connect.close()
    #     count1 += 1

        
    # if AA == None:
    #     print('변환할 답변 데이터 없음')
    #     connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
    #     Cursor = connect.cursor()
    #     Cursor.close()
    #     connect.close()
    #     count2 += 1
        
    if MM1:
        connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
        Cursor = connect.cursor()
        MMC1=MM1[0]
        MMC2=MM1[1]
        print(MMC1, MMC2)
        result=sentiment_predict(MMC1)
        result2 = modelfitting(MMC1)
        print(result,result2)
        Cursor.execute("UPDATE test_db SET 사람문장1예측 = ? WHERE 사람문장1 = ?", (result + ' // '+result2, MMC1))
        connect.commit()
        print("업데이트 완료")

        if MMC2 == result2:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 사람문장1 = ?", ('성공', MMC1))
            connect.commit()
            print('예측 성공')
        else:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 사람문장1 = ?", ('실패', MMC1))
            connect.commit()
            print('예측 실패')
        Cursor.close()
        connect.close()
        
    if MM2:
        connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
        Cursor = connect.cursor()
        MMC1=MM2[0]
        MMC2=MM2[1]
        print(MMC1, MMC2)
        result=sentiment_predict(MMC1)
        result2 = modelfitting(MMC1)
        print(result,result2)
        Cursor.execute("UPDATE test_db SET 사람문장2예측 = ? WHERE 사람문장2 = ?", (result + ' // '+result2, MMC1))
        connect.commit()
        print("업데이트 완료")

        if MMC2 == result2:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 사람문장2 = ?", ('성공', MMC1))
            connect.commit()
            print('예측 성공')
        else:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 사람문장2 = ?", ('실패', MMC1))
            connect.commit()
            print('예측 실패')
        Cursor.close()
        connect.close()
    if MM3:
        connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
        Cursor = connect.cursor()
        MMC1=MM3[0]
        MMC2=MM3[1]
        print(MMC1, MMC2)
        result=sentiment_predict(MMC1)
        result2 = modelfitting(MMC1)
        print(result,result2)
        Cursor.execute("UPDATE test_db SET 사람문장3예측 = ? WHERE 사람문장3 = ?", (result + ' // '+result2, MMC1))
        connect.commit()
        print("업데이트 완료")


        if MMC2 == result2:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 사람문장3 = ?", ('성공', MMC1))
            connect.commit()
            print('예측 성공')
        else:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 사람문장3 = ?", ('실패', MMC1))
            connect.commit()
            print('예측 실패')
        Cursor.close()
        connect.close()
    if MM4:
        connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
        Cursor = connect.cursor()
        MMC1=MM4[0]
        MMC2=MM4[1]
        print(MMC1, MMC2)
        result=sentiment_predict(MMC1)
        result2 = modelfitting(MMC1)
        print(result,result2)
        Cursor.execute("UPDATE test_db SET 기계문장1예측 = ? WHERE 기계문장1 = ?", (result + ' // '+result2, MMC1))
        connect.commit()
        print("업데이트 완료")


        if MMC2 == result2:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 기계문장1 = ?", ('성공', MMC1))
            connect.commit()
            print('예측 성공')
        else:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 기계문장1 = ?", ('실패', MMC1))
            connect.commit()
            print('예측 실패')
        Cursor.close()
        connect.close()
    if MM5:
        connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
        Cursor = connect.cursor()
        MMC1=MM5[0]
        MMC2=MM5[1]
        print(MMC1, MMC2)
        result=sentiment_predict(MMC1)
        result2 = modelfitting(MMC1)
        print(result,result2)
        Cursor.execute("UPDATE test_db SET 기계문장2예측 = ? WHERE 기계문장2 = ?", (result + ' // '+result2, MMC1))
        connect.commit()
        print("업데이트 완료")

        if MMC2 == result2:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 기계문장2 = ?", ('성공', MMC1))
            connect.commit()
            print('예측 성공')
        else:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 기계문장2 = ?", ('실패', MMC1))
            connect.commit()
            print('예측 실패')
        Cursor.close()
        connect.close()
    if MM6:
        connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
        Cursor = connect.cursor()
        MMC1=MM6[0]
        MMC2=MM6[1]
        print(MMC1, MMC2)
        result=sentiment_predict(MMC1)
        result2 = modelfitting(MMC1)
        print(result,result2)
        Cursor.execute("UPDATE test_db SET 기계문장3예측 = ? WHERE 기계문장3 = ?", (result + ' // '+result2, MMC1))
        connect.commit()
        print("업데이트 완료")

        if MMC2 == result2:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 기계문장3 = ?", ('성공', MMC1))
            connect.commit()
            print('예측 성공')
        else:
            Cursor.execute("UPDATE test_db SET 결과 = ? WHERE 기계문장3 = ?", ('실패', MMC1))
            connect.commit()
            print('예측 실패')
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

        
        
    time.sleep(0.5)
    print('재시작')
                    