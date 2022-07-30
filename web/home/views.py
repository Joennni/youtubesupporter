from ctypes import alignment
# from msilib.schema import Class
from types import GetSetDescriptorType
from django.shortcuts import render
from django.http import HttpResponse
import sql.sql as sql
import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc #영어는 font설정을 안해도 되지만 해당 데이터 안에 한글이 있을때 깨지는걸 방지,한글되는폰트적용.
import platform
import json
from django.core.paginator import Paginator

#그래프에서 한글 표기를 위한 글자체 변경
#(윈도우, 맥os) 각각의 경우에 대해서 처리
if platform.system() =='Windows':
    path='c:/Windows/Fonts/malgun.ttf'
    font_name=font_manager.FontProperties(fname=path).get_name()
    rc('font',family=font_name)
    
elif platform.system()=='Darwin':
    rc('font',family='AppleGothic')
    
else:
    print('Check your OS system')


BASE_DIR = Path(__file__).resolve().parent.parent

plt.rcParams['font.family'] = 'NanumGothic'


#df = pd.read_csv('읽어올 데이터')
#df.head()
# Create your views here.




def home(request):
    name, img, star = sql.movie_list(order='movie_total_viewer', asc='desc')
    data = list(zip(name, img, star))[:4]
    temp1 = []
    temp2 = []
    for i in range(len(data)):
        temp1.append((data[i][0], data[i][1], data[i][2]))
    temp2.append(temp1)
    msg = 'ok'
    
    context = {"data": temp2, 'msg':msg}
    return render(request, 'home/home.html', context)


def home_01(request):
    return render(request, "home/home_01.html", {})   

def support(request):
    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()
    
    # 접속횟수
    cursor.execute("select count(mem_name) from board_Member_time where mem_name = 'SoHyun' Group by mem_name")
    s1=cursor.fetchone()
    s1=s1[0]
    cursor.execute("select count(mem_name) from board_Member_time where mem_name = 'SangA' Group by mem_name")
    s2=cursor.fetchone()
    s2=s2[0]
    cursor.execute("select count(mem_name) from board_Member_time where mem_name = 'MinHee' Group by mem_name")
    s3=cursor.fetchone()
    s3=s3[0]
    cursor.execute("select count(mem_name) from board_Member_time where mem_name = 'JiHyun' Group by mem_name")
    s4=cursor.fetchone()
    s4=s4[0]
    
    
    # 댓글 수집 갯수
    cursor.execute("select count(mem_name) from board_comment1 Group by mem_name order by mem_name desc")
    com = cursor.fetchall()
    
    com0 = com[0][0]
    com1 = com[1][0]
    com2 = com[2][0]
    com3 = com[3][0]
    
    
    # 캡처 이미지 갯수
    cursor.execute("select count(mem_name) from board_capture Group by mem_name order by mem_name desc")
    cap = cursor.fetchall()
    print(cap)
    cap0 = cap[0][0]
    cap1 = cap[1][0]
    cap2 = cap[2][0]
    cap3 = cap[3][0]
    print(cap0)
    # 해시태그 수집 갯수
    cursor.execute("select count(mem_name) from board_htag Group by mem_name order by mem_name desc")
    tag = cursor.fetchall()
    
    tag0 = tag[0][0]
    tag1 = tag[1][0]
    tag2 = tag[2][0]
    tag3 = tag[3][0]
    
    # 자막 수집 갯수
    cursor.execute("select count(mem_name) from board_script Group by mem_name order by mem_name desc")
    scp= cursor.fetchall()
    
    scp0 = scp[0][0]
    scp1 = scp[1][0]
    scp2 = scp[2][0]
    scp3 = scp[3][0]
    
    # 합계
    s_total = s1+s2+s3+s4
    com_total = com0 + com1 + com2 + com3
    cap_total = cap0 + cap1 + cap2 + cap3
    tag_total = tag0 + tag1 + tag2 + tag3
    scp_total = scp0 + scp1 + scp2 + scp3
    
    # 평균
    s_avg = (s1+s2+s3+s4)/4
    com_avg = (com0 + com1 + com2 + com3)/4
    cap_avg = (cap0 + cap1 + cap2 + cap3)/4
    tag_avg = (tag0 + tag1 + tag2 + tag3)/4
    scp_avg = (scp0 + scp1 + scp2 + scp3)/4
    
    # 접속횟수 최소값
    cursor.execute("select count(mem_name) from board_Member_time Group by mem_name order by count(mem_name) asc limit 1")
    con_min= cursor.fetchone()
    con_min = con_min[0]
    
    # 접속횟수 최대값
    cursor.execute("select count(mem_name) from board_Member_time Group by mem_name order by count(mem_name) desc limit 1")
    con_max= cursor.fetchone()
    con_max = con_max[0]
    
    # 댓글 수집 갯수 최소값
    cursor.execute("select count(mem_name) from board_comment1 Group by mem_name order by count(mem_name) asc limit 1")
    com_min= cursor.fetchone()
    com_min = com_min[0]
    
    # 댓글 수집 갯수 최대값
    cursor.execute("select count(mem_name) from board_comment1 Group by mem_name order by count(mem_name) desc limit 1")
    com_max= cursor.fetchone()
    com_max = com_max[0]
    
    # 캡처 이미지 갯수 최소값
    cursor.execute("select count(mem_name) from board_capture Group by mem_name order by count(mem_name) asc limit 1")
    cap_min= cursor.fetchone()
    cap_min = cap_min[0]
    
    # 캡처 이미지 갯수 최대값
    cursor.execute("select count(mem_name) from board_capture Group by mem_name order by count(mem_name) desc limit 1")
    cap_max= cursor.fetchone()
    cap_max = cap_max[0]
    
    # 해시태그 갯수 최소값
    cursor.execute("select count(mem_name) from board_htag Group by mem_name order by count(mem_name) asc limit 1")
    tag_min= cursor.fetchone()
    tag_min = tag_min[0]
    
    # 해시태그 갯수 최대값
    cursor.execute("select count(mem_name) from board_htag Group by mem_name order by count(mem_name) desc limit 1")
    tag_max= cursor.fetchone()
    tag_max = tag_max[0]
    
    # 자막 수집 갯수 최소값
    cursor.execute("select count(mem_name) from board_script Group by mem_name order by count(mem_name) asc limit 1")
    scp_min= cursor.fetchone()
    scp_min = scp_min[0]
    
    # 자막 수집 갯수 최대값
    cursor.execute("select count(mem_name) from board_script Group by mem_name order by count(mem_name) desc limit 1")
    scp_max= cursor.fetchone()
    scp_max = scp_max[0]
    
    # 유저별 접속횟수 그래프
    cursor.execute("select mem_name, count(mem_name) from board_Member_time group by mem_name order by mem_name DESC")
    activation_member=cursor.fetchall()
    df_activation=pd.DataFrame(activation_member)
    
    plt.figure(figsize=(6, 6))
    sns.barplot(data = df_activation , x = 0 , y= 1 , palette = "Blues_d")
    plt.yticks(fontsize=12)
    plt.xlabel(' ', fontsize=12)
    plt.ylabel('접속횟수', fontsize=12)
    plt.title('유저별 접속횟수', fontsize=20)
    plt.savefig('{}/static/img/유저별_접속횟수.png'.format(BASE_DIR))
    
    # 유저별 댓글 수집갯수
    cursor.execute("select mem_name, count(mem_name) from board_comment1 group by mem_name order by mem_name DESC")
    comment_counts=cursor.fetchall()
    df_comment_counts=pd.DataFrame(comment_counts)

    plt.figure(figsize=(6, 6))
    sns.barplot(data = df_comment_counts , x = 0 , y= 1 , palette = "Blues_d")
    plt.yticks(fontsize=12)
    plt.xlabel(' ', fontsize=12)
    plt.ylabel('댓글 수집갯수', fontsize=12)
    plt.title('유저별 댓글 수집 갯수', fontsize=20)
    plt.savefig('{}/static/img/유저별_댓글수집횟수.png'.format(BASE_DIR))
    
    # 유저별 이미지 캡쳐갯수
    cursor.execute("select mem_name, count(mem_name) from board_capture group by mem_name order by mem_name DESC")
    capture_counts=cursor.fetchall()
    df_capture_counts=pd.DataFrame(capture_counts)

    plt.figure(figsize=(6, 6))
    sns.barplot(data = df_capture_counts , x = 0 , y= 1 , palette = "Blues_d")
    plt.yticks(fontsize=12)
    plt.xlabel(' ', fontsize=12)
    plt.ylabel('캡처갯수', fontsize=12)
    plt.title('유저별 캡처갯수', fontsize=20)
    plt.savefig('{}/static/img/유저별_캡쳐횟수.png'.format(BASE_DIR))
    
    # 유저별 해시태그 수집 갯수
    cursor.execute("select mem_name, count(mem_name) from board_htag group by mem_name order by mem_name DESC")
    H_tag_counts=cursor.fetchall()
    df_H_tag_counts=pd.DataFrame(H_tag_counts)

    plt.figure(figsize=(6, 6))
    sns.barplot(data = df_H_tag_counts , x = 0 , y= 1 , palette = "Blues_d")
    plt.yticks(fontsize=12)
    plt.xlabel(' ', fontsize=12)
    plt.ylabel('해시태그 수집 갯수', fontsize=12)
    plt.title('유저별 해시태그 수집 갯수', fontsize=20)
    plt.savefig('{}/static/img/유저별_해시태그_수집_횟수.png'.format(BASE_DIR))
    
    # 유저별 스크립트 수집 갯수
    cursor.execute("select mem_name, count(mem_name) from board_script group by mem_name order by mem_name DESC")
    script_counts=cursor.fetchall()
    df_script_counts=pd.DataFrame(script_counts)

    plt.figure(figsize=(6, 6))
    sns.barplot(data = df_script_counts , x = 0 , y= 1 , palette = "Blues_d")
    plt.yticks(fontsize=12)
    plt.xlabel(' ', fontsize=12)
    plt.ylabel('스크립트 수집갯수', fontsize=12)
    plt.title('유저별 스크립트 수집갯수', fontsize=20)
    plt.savefig('{}/static/img/유저별_스크립트_수집_횟수.png'.format(BASE_DIR))

    
    
    context = {"con1": s1, "con2": s2, "con3": s3, "con4": s4, "com":com0, "com1":com1, "com2":com2, "com3":com3, "cap":cap0, "cap1":cap1, "cap2":cap2, "cap3":cap3, 
            "tag":tag0, "tag1":tag1, "tag2":tag2, "tag3":tag3, "scp":scp0, "scp1":scp1, "scp2":scp2, "scp3":scp3, 
            "s_total": s_total, "com_total": com_total, "cap_total": cap_total, "tag_total": tag_total, "scp_total": scp_total, 
            "s_avg": s_avg, "com_avg": com_avg, "cap_avg": cap_avg, "tag_avg": tag_avg, "scp_avg": scp_avg, "con_min": con_min, "con_max": con_max, "com_min": com_min, "com_max": com_max,
            "cap_min": cap_min, "cap_max": cap_max, "tag_min": tag_min, "tag_max": tag_max, "scp_min": scp_min, "scp_max": scp_max}
    cursor.close()
    conn.close()    
    
    
    
    return render(request, 'support/support.html', context)


def search(request):
    search = request.POST['search']
    # name, img, star = sql.search(search)
    name, img, star = sql.movie_list(order='movie_name', search=search, asc='asc')
    data = list(zip(name, img, star))
    temp1 = []
    temp2 = []
    for i in range(len(data)):
        if i % 3 == 0 and i != 0:
            temp2.append(temp1[-3:])
        temp1.append((data[i][0], data[i][1], data[i][2]))
        if i == len(data)-1:
            tmp = len(temp1) % 3
            temp2.append(temp1[-tmp:])
    if len(temp2) == 0 and len(temp1) == 0:
        msg = '검색 결과가 존재하지 않습니다.'
    else:
        msg = 'ok'
    total_count = len(temp1)
    context = {"data": temp2, 'msg':msg, "total": total_count}
    return render(request, 'home/search_list.html', context)


