from django.shortcuts import render
from django.http import HttpResponse
from folium.plugins import MarkerCluster
import folium
import random
import sql.sql as sql
import requests
import json
import pandas as pd

# Create your views here.

r = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
c = r.content
seoul_geo = json.loads(c)
r2 = requests.get('https://raw.githubusercontent.com/vuski/admdongkor/master/ver20220309/HangJeongDong_ver20220309.geojson')
c2 = r2.content
songpa_geo = json.loads(c2)

# df_charge_group = pd.read_csv('./static/csv/ev_data1_group.csv', encoding='utf-8')

# df = pd.read_excel('./static/csv/seoul_data_geocode.xlsx')
# df = df.drop(0)
# df_group = df.groupby('gu', as_index = False).sum()
# df_charge = pd.read_csv('./static/csv/sfsf.csv')
# df_charge_group = df_charge.groupby(['충전소명','Latitude','Longitude'], as_index = False).count()
# df_songpa = df[df['gu'] == '송파구']
# df_charge_songpa = df_charge[df_charge['주소(구)'] == '송파구' ]
# df_charge_group_songpa = df_charge_songpa.groupby(['충전소명','Latitude','Longitude'], as_index = False).count()

def game_rock():
    game_set = ['가위', '바위', '보']
    my = random.choice(game_set)
    com = random.choice(game_set)
    if my == com:
        result = 'draw'
    elif (my == '가위' and com == '보')\
        or (my == '바위' and com == '가위')\
        or (my == '보' and com == '바위'):
        result = 'win'
    else:
        result = 'lose'
    return result, my, com

def game_question(number, answer):
    if number > answer:
        msg = '{}보다 작습니다!'.format(number)
        return False, msg
    elif number < answer:
        msg = '{}보다 큽니다!'.format(number)
        return False, msg
    else: 
        msg = '정답입니다!'
        return True, msg

#############################################################

def event(request):
    m = folium.Map(
    location=[37.559819, 126.963895],
    tiles = 'cartodbpositron',
    zoom_start = 9,  width='90%', height='90%')

    folium.Choropleth(
        geo_data = seoul_geo,
        data = df_group,
        columns = ['gu','ele_num'],
        fill_color = 'YlOrRd',
        fill_opacity = 0.6,
        line_opacity = 0.6,
        key_on = 'properties.name',
        legend_name = '지역구별 전기차 보유 수'
    ).add_to(m)

    marker_cluster = MarkerCluster().add_to(m)

    nop= -1
    for lat, long in zip(df_charge_group['Latitude'], df_charge_group['Longitude']):
        nop += 1
        folium.Marker([lat, long], icon = folium.Icon(color="green"), popup=df_charge_group['충전소명'][nop]).add_to(marker_cluster)
    maps=m._repr_html_() 
    
    m2 = folium.Map(
    name='송파구',
    location=[37.506090, 127.134003],
    tiles = 'cartodbpositron',
    zoom_start =13
    )

    folium.Choropleth(
        geo_data = songpa_geo,
        data = df_songpa,
        columns = ['dong','ele_num'],
        fill_color = 'YlOrRd',
        fill_opacity = 0.6,
        line_opacity = 0.6,
        key_on = 'properties.emd_nm',
        legend_name = '지역동별 전기차 보유 수'
    ).add_to(m2)
    
    no = -1
    
    for lat, long in zip(df_charge_group_songpa['Latitude'], df_charge_group_songpa['Longitude']):
        no += 1
        folium.Marker([lat, long], icon = folium.Icon(color="green"), popup=df_charge_group_songpa['충전소명'][no]).add_to(m2)
        
    folium.LayerControl().add_to(m2)
    maps2=m2._repr_html_()
    
    context = {'map' : maps, 'map2':maps2}
    
    return render(request, 'event/event.html',context)






def event_rock(request):
    if request.method == "POST" and request.POST['betting'] != '':
        betting = int(request.POST['betting'])
        result, my, com = game_rock()
        if result == 'win':
            bet = betting * 3 - betting 
        elif result == 'lose':
            bet = 0 - betting
        else:
            bet = 0
        current_point = sql.point_checker(request.user.username)
        if current_point < betting:
            result1 = False
            msg = "포인트가 부족합니다."
        else:
            result1 = sql.point_inserter(request.user.username, bet)
            msg = '{}! {} 포인트'.format(result, bet)
        msg2 = '{}'.format(sql.point_checker(request.user.username))
    
    elif request.method == "POST" and request.POST['betting'] == '':
        result = 'start'
        my = '가위'
        com = '바위'
        bet = 0
        betting = 0
        msg = '값을 입력해 주세요'
        msg2 = '{}'.format(sql.point_checker(request.user.username))
    else:
        result = 'start'
        my = '가위'
        com = '바위'
        bet = 0
        betting = 0
        msg = '배팅'
        msg2 = '{}'.format(sql.point_checker(request.user.username))
    
    context = {"result": result, "my": my, "com": com, 
        "betting": betting, "bet": bet, "msg":msg, "msg2":msg2}
    return render(request, 'event/event_rock.html', context)





def event_question_set(request):
    if request.method != 'POST':
        answer = random.randint(1, 20)
        count = 0
        msg = 'first'
        d2 = 0
    elif request.method == "POST" and request.POST['number'] == '': 
        answer = int(request.POST['answer'])
        count = int(request.POST['count'])
        msg = 'no value'
        d2 = 0
    elif request.method == "POST" and (int(request.POST['number']) <= 0 or int(request.POST['number']) > 20):
        answer = int(request.POST['answer'])
        count = int(request.POST['count'])
        msg = '1-20 사이의 값을 입력해 주세요'
        d2 = 0
    else:
        number = int(request.POST['number'])
        answer = int(request.POST['answer'])
        count = int(request.POST['count'])
        result, msg = game_question(number, answer)
        count += 1
        d2 = 0
        current_point = sql.point_checker(request.user.username)
        if current_point < 1000:
            result1 = False
            msg = "포인트가 부족합니다."
        else:
            if result == True and count <= 3:
                result1 = sql.point_inserter(request.user.username, 1000 * 5 - 1000)
            elif result == True and count > 3:
                result1 = sql.point_inserter(request.user.username, 0-1000)
            d2 = sql.point_checker(request.user.username)
        
    context = {'answer': answer, 'msg': msg, 'count': count, 'point': d2}
    return render(request, 'event/event_question.html', context)

# def supporter(request):
#     return render(request, 'support/support.html')

# Create your views here.
