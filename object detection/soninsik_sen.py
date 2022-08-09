import sqlite3
import argparse
import os
import sys
from pathlib import Path
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from openpyxl import Workbook
import pandas as pd
import time
import glob
from PIL import Image
from PIL import ImageFilter
import shutil
from datetime import datetime
from bs4 import BeautifulSoup
import warnings 
warnings.filterwarnings('ignore')
import re
from youtube_transcript_api import YouTubeTranscriptApi
import re
import urllib.request
import numpy as np
import pandas as pd
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
okt = Okt()
count22 = 0

import tensorflow as tf
from  tensorflow.keras.models import load_model
model = tf.keras.models.load_model('C:/Users/HAEDONG/yolov5/lstm_sentiment.h5')

import cv2
import mediapipe as mp
import math
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import pickle

driver = webdriver.Chrome('c:/ChromeDriver.exe')
url= 'https://www.youtube.com'
driver.get(url)

with open('./tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


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

# def comment_sentiment_predict(df):
#     import pandas as pd
#     df['comment'] = df['comment'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
#     df = df.dropna()
#     df = df.reset_index(drop = True)
#     comment_df = pd.DataFrame(columns = ['video_name', 'com_id', 'comment', 'sentiment'])

#     for i in range(len(df)):
#         comment_df.loc[i, 'video_name'] = df.loc[i, 'video_name']
#         comment_df.loc[i, 'com_id'] = df.loc[i, 'com_id']
#         comment_df.loc[i, 'comment'] = df.loc[i, 'comment']
#         comment_df.loc[i, 'sentiment'] = sentiment_predict(comment_df.loc[i, 'comment'])
#         print(comment_df.loc[i, 'comment'])
#         print(comment_df.loc[i, 'sentiment'])

#     return comment_df

com_count = 0

# 현재 활성화된 창의 정보
fw = pyautogui.getActiveWindow()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume =   cast(interface, POINTER(IAudioEndpointVolume))

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

mpDraw = mp.solutions.drawing_utils
mpDraw_styles = mp.solutions.drawing_styles
mpHands = mp.solutions.hands
my_hands= mpHands.Hands()
mp_objectron = mp.solutions.objectron

def dist(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1 - x2,2)) + math.sqrt(math.pow(y1 - y2,2))

compareIndex = [[18,4],[6,8],[10,12],[14,16],[18,20]]
openfinger = [False,False,False,False,False]
gesture = [[True,True,True,True,True, "Hi~!"],
            [False,True,True,False,False,"H_tag"],
            [True,True,False,False,True,"SpiderMan!"],
            [True,False,False,False,False, "Capture"],
            [False,True,False,False,False, "Comment"],
            [False,False,True,False,False, "******"],
            [False,False,False,False,False, "Stop/replay"],
            [True,True,False,False,False, "Script"],
            [False,False,False,False,True, "Promise!"]]


    
while True:
    success, img = cap.read()
    h,w,c = img.shape
    imgRGB =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=my_hands.process(imgRGB)
    if results.multi_hand_landmarks:
    #sqlite3 DB 연결
        connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
        Cursor = connect.cursor()
        # 시간대 설정
        now = datetime.now()
        today = now.date()
        current_time = now.strftime("%H:%M:%S")
        current_time2 = now.strftime("%H_%M_%S")

        # 사진 담을 폴더 만들기
        dest_folder = 'Z:/homes/gmrain/djangoproject/Youtube_Supporter/static/screenshot/{}'.format(today)

        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        for handLms in results.multi_hand_landmarks:
            if keyboard.is_pressed('shift'):
                if keyboard.is_pressed('t'):
                    
                    Cursor.execute("SELECT * FROM board_Member_list ORDER BY ROWID DESC LIMIT 1")
                    print(Cursor.fetchone())
            if keyboard.is_pressed('shift'):
                if keyboard.is_pressed('a'):
                    global curdist
                    curdist = -dist(handLms.landmark[4].x,handLms.landmark[4].y,handLms.landmark[8].x,handLms.landmark[8].y) / (dist(handLms.landmark[2].x,handLms.landmark[2].y,handLms.landmark[5].x,handLms.landmark[5].y)*2)
                    curdist = curdist * 100
                    curdist = -96 - curdist
                    curdist = min(0,curdist)
                    curdist = max(-64,curdist)
                    # print(curdist)
                    volume.SetMasterVolumeLevel(curdist, None)
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            
            
            for i in range(0,5):
                openfinger[i] = dist(handLms.landmark[0].x,handLms.landmark[0].y,handLms.landmark[compareIndex[i][0]].x,handLms.landmark[compareIndex[i][0]].y) < dist(handLms.landmark[0].x,handLms.landmark[0].y,handLms.landmark[compareIndex[i][1]].x,handLms.landmark[compareIndex[i][1]].y)
                
                # print(open)
                text_x=(handLms.landmark[0].x * w)
                text_y=(handLms.landmark[0].y * h)
                for i in range(0,len(gesture)):
                    flag = True
                    for j in range(0,5):
                        if(gesture[i][j] != openfinger[j]):
                            flag=False
                    if(flag == True):
                        action2=gesture[i][5]
                        cv2.putText(img,gesture[i][5],(round(text_x) -50,round(text_y)- 250),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),4)
                mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS, mpDraw_styles.get_default_hand_landmarks_style(),
            mpDraw_styles.get_default_hand_connections_style())

                    
                
                if keyboard.is_pressed('shift'):
                    if keyboard.is_pressed('x'):
                        if str(action2)== "Capture" :
                            Cursor.execute("SELECT * FROM board_Member_list ORDER BY ROWID DESC LIMIT 1")
                            NN=Cursor.fetchone()
                            print(NN[0])
                            driver.current_url
                                        
                            driver.implicitly_wait(1.5)
                            
                            html_source = driver.page_source
                            soup = BeautifulSoup(html_source, 'html.parser')

                            id_list = soup.select("div#header-author > h3 > #author-text > span")
                            comment_list = soup.select("yt-formatted-string#content-text")
                            video_name = soup.select("title")
                            #type(video_name)
                            video_name = video_name[0].text

                            pyautogui.screenshot('{}/{}_{}_{}.jpg'.format(dest_folder,NN[0],today,current_time2), region=(fw.left,fw.top,fw.size[0],fw.size[1]))
                            Cursor.execute("INSERT INTO board_Capture VALUES (?,?,?,?,?,?,?)", ('{}_{}_{}.jpg'.format(NN[0],today,current_time2),NN[0],video_name,'{}/{}_{}_{}.jpg'.format(dest_folder,NN[0],today,current_time2),"{} {}".format(today,current_time),today,current_time))
                            connect.commit()
                            print(NN[0], ' 유저가 화면을 캡처하였습니다.', '{}/{}_{}_{}.jpg'.format(dest_folder,NN[0],today,current_time2))
                        if str(action2)== "Stop/replay" :
                            Cursor.execute("SELECT * FROM board_Member_list ORDER BY ROWID DESC LIMIT 1")
                            NN=Cursor.fetchone()
                            print(NN[0], '멈추거나 재생합니다')
                            pyautogui.press(['space'])
                                        
                                    
                        if str(action2) == 'Comment': #댓글 크롤링    
                                        Cursor.execute("SELECT * FROM board_Member_list ORDER BY ROWID DESC LIMIT 1")
                                        NN=Cursor.fetchone()
                                        print(NN[0])
                                        id_final = []
                                        comment_final = []
                                        com_count += 1

                                    #크롤링 시작
                                        driver.current_url

                                        driver.implicitly_wait(1.5)

                                        #팝업
                                        try:
                                            driver.find_element_by_css_selector("#dismiss-button > a").click()
                                        except:
                                            pass

                                        driver.execute_script("window.scrollTo(0, 500)")
                                        time.sleep(1)
                                        driver.execute_script("window.scrollTo(0, 1000)")
                                        time.sleep(0.5)
                                        driver.execute_script("window.scrollTo(0, 1500)")
                                        time.sleep(0.5)
                                        driver.execute_script("window.scrollTo(0, 2000)")
                                        time.sleep(0.5)
                                        driver.execute_script("window.scrollTo(0, 2500)")
                                        time.sleep(0.5)
                                        driver.execute_script("window.scrollTo(0, 3000)")
                                        time.sleep(0.5)
                                        driver.execute_script("window.scrollTo(0, 3500)")
                                        time.sleep(0.5)
                                        driver.execute_script("window.scrollTo(0, 4000)")
                                        time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 4500)") 
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 5000)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 5500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 6000)") 
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 6500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 7000)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 7500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 8000)") 
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 8500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 9000)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 9500)") 
                                        # time.sleep(0.5)                    
                                        # driver.execute_script("window.scrollTo(0, 10000)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 10500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 11000)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 11500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 12000)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 12500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 13000)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 13500)") 
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 14000)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 14500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 15000)") 
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 15500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 16000)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 16500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 17000)") 
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 17500)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 18000)")
                                        # time.sleep(0.5)
                                        # driver.execute_script("window.scrollTo(0, 18500)") 
                                        time.sleep(1)

                                        
                                        
                                        html_source = driver.page_source
                                        soup = BeautifulSoup(html_source, 'html.parser')

                                        id_list = soup.select("div#header-author > h3 > #author-text > span")
                                        comment_list = soup.select("yt-formatted-string#content-text")
                                        video_name = soup.select("title")
                                        #type(video_name)
                                        video_name = video_name[0].text
                                        
                                        predict_final = []
                                        for y in range(len(comment_list)):
                                            temp_id = id_list[y].text
                                            temp_id = temp_id.replace('\n', '')
                                            temp_id = temp_id.replace('\t', '')
                                            temp_id = temp_id.replace('    ', '')
                                            id_final.append(temp_id) # 댓글 작성자

                                            temp_comment = comment_list[y].text
                                            temp_comment = temp_comment.replace('\n', '')
                                            temp_comment = temp_comment.replace('\t', '')
                                            temp_comment = temp_comment.replace('    ', '')
                                            comment_final.append(temp_comment) # 댓글 내용
                                            predict1=sentiment_predict(temp_comment)
                                            sen1=predict1[0:8]
                                            score=predict1[9:14]
                                            predict_final.append(predict1)
                                            

                                            Cursor.execute("INSERT INTO board_comment1 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (y,y,com_count,NN[0],video_name, temp_id, temp_comment,"{} {}".format(today,current_time),today,current_time,predict1,sen1,score))
                                            connect.commit()
                                            print(y,'DB에 댓글을 저장중입니다.')
                                        print("댓글 저장을 완료하였습니다")

                                        
                                        pd_data = {"video_name": video_name, "com_id" : id_final , "comment" : comment_final, "pridict2": predict_final }
                                        youtube_pd = pd.DataFrame(pd_data)
                                        # youtube_pd = comment_sentiment_predict(youtube_pd)


                                        #저장
                                        youtube_pd.to_excel('{}/{}_comment_{}_{}.xlsx'.format(dest_folder,NN[0],today,current_time2))
                                        connect.close()
                            
                        
                        if str(action2) == 'H_tag': #해쉬태그 크롤링
                            id_final = []
                            comment_final = []
                            com_count += 1
                            Cursor.execute("SELECT * FROM board_Member_list ORDER BY ROWID DESC LIMIT 1")
                            NN=Cursor.fetchone()
                            print(NN[0], '해시태그를 읽고있습니다.')
                        #크롤링 시작
                            driver.current_url
                            
                            driver.implicitly_wait(3)
                            time.sleep(1.5)
                            # driver.execute_script("window.scrollTo(0, 3000)")
                            # time.sleep(5)

                            #팝업
                            try:
                                driver.find_element_by_css_selector("#dismiss-button > a").click()
                            except:
                                pass
                            
                            html_source = driver.page_source
                            soup = BeautifulSoup(html_source, 'html.parser')

                            id_list = soup.select("div#header-author > h3 > #author-text > span")
                            comment_list = soup.select("yt-formatted-string#content-text")
                            video_name = soup.select("title")
                            #type(video_name)
                            video_name = video_name[0].text
                            tag = soup.select('#scriptTag')
                            if '#' in tag[0].text:
                                
                                re_pattern = re.compile(r'\#\w+')
                                tag_results = re.findall(re_pattern, tag[0].text)
                                h_tag = pd.DataFrame(tag_results)
                                h_tag.columns = [video_name]
                                h_tag.to_csv('{}/{}_h_tag_{}_{}.txt'.format(dest_folder,NN[0],today,current_time2), index=False)
                                for w in range(len(tag_results)):

                                    Cursor.execute("INSERT INTO board_Htag VALUES (?,?,?,?,?,?,?,?,?)", (w,w,com_count,NN[0],video_name, tag_results[w],"{} {}".format(today,current_time),today,current_time))
                                    connect.commit()
                                    print(w,'DB에 해쉬태그를 저장하고있습니다')
                                print('DB에 해쉬태그 저장을 완료하였습니다.')
                                time.sleep(0.5)
                            connect.close()

                        
                        if str(action2) == 'Script': #자막
                            
                            id_final = []
                            comment_final = []
                            com_count += 1

                        #크롤링 시작
                            driver.current_url
                            cur_url = driver.current_url
                            driver.implicitly_wait(3)
                            time.sleep(1.5)
                            # driver.execute_script("window.scrollTo(0, 3000)")
                            # time.sleep(5)
                            Cursor.execute("SELECT * FROM board_Member_list ORDER BY ROWID DESC LIMIT 1")
                            NN=Cursor.fetchone()
                            print(NN[0],'스크립트를 저장중입니다.. 잠시만 기다려주십시오.')

                            #팝업
                            try:
                                driver.find_element_by_css_selector("#dismiss-button > a").click()
                            except:
                                pass
                            
                            html_source = driver.page_source
                            soup = BeautifulSoup(html_source, 'html.parser')

                            id_list = soup.select("div#header-author > h3 > #author-text > span")
                            comment_list = soup.select("yt-formatted-string#content-text")
                            video_name = soup.select("title")
                            #type(video_name)
                            video_name = video_name[0].text
                            srt = YouTubeTranscriptApi.get_transcript(cur_url[32:], languages=['ko'])
                            script = []
                            stime= []

                            with open('subtitles.txt', 'w', encoding='utf-8') as f:
                                for z,s in enumerate(srt):
                                    f.write("{}\n".format(s))
                                    script.append(s['text'][:])
                                    stime.append(s.get('start'))

                                    Cursor.execute("INSERT INTO board_script VALUES (?,?,?,?,?,?,?,?,?,?)", (z,z,com_count,NN[0],video_name,stime[z], script[z],"{} {}".format(today,current_time),today,current_time))
                                    
                                    connect.commit()
                                print(NN[0],'스크립트 저장을 완료하였습니다.')
                                    # f.close()
                            
                            script = pd.DataFrame(script)
                            script.columns = [video_name]
                            script.to_csv('{}/{}_script_{}_{}.txt'.format(dest_folder,NN[0],today,current_time2), index=False)
                            connect.close()

                cv2.namedWindow('MediaPipe Hands', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
                if count22 < 300:
                    cv2.resizeWindow('MediaPipe Hands', 1400, 1000)
                
                elif count22 > 300:
                    cv2.resizeWindow('MediaPipe Hands', 500, 400)
                    
                cv2.imshow('MediaPipe Hands', img)
                
                count22= count22+1
                
                
                
                
                
                # cv2.waitkey(1)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
# cap.release()