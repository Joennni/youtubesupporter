from django.shortcuts import render
from folium import plugins
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster


# Create your views here.
import sql.sql as sql
import folium
import geocoder
import pandas as pd
import requests
import json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

r = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
c = r.content
seoul_geo = json.loads(c)

seoul = pd.read_csv('소상공인시장진흥공단_상가(상권)정보_서울_202203.csv')
seoul = seoul[['시군구명', '상권업종대분류명', '상권업종중분류명', '위도', '경도']]

import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'

seoul_coffee = seoul.loc[seoul['상권업종중분류명'] == '커피점/카페']

seoul_group_data = seoul.loc[seoul['상권업종중분류명'] == '커피점/카페'].groupby('시군구명')['상권업종중분류명'].count()


def ptpt():
    plt.figure(figsize=(12, 30))
    sns.countplot(y=seoul['상권업종중분류명'], order=seoul['상권업종중분류명'].value_counts().index)
    plt.yticks(fontsize=12)
    plt.title('서울시 업종별 개수')
    plt.savefig('{}/static/img/상권분류명.png'.format(BASE_DIR))


def ptpt2():    
    plt.figure(figsize=(12, 10))
    seoul.loc[seoul['상권업종중분류명'] == '커피점/카페'].groupby('시군구명')['상권업종대분류명'].count()\
                                                .sort_values().plot(kind='barh', color='royalblue')
    plt.yticks(fontsize=12)
    plt.title('서울시 자치구별 커피점/카페 업종수')
    plt.savefig('{}/static/img/커피점카페.png'.format(BASE_DIR))
    
g = geocoder.ip('me')

def mapping(request):
    map = folium.Map(location=g.latlng,zoom_start=15, width='70%', height='95%', align = 'center') 
    plugins.LocateControl().add_to(map) 
    maps=map._repr_html_() 
    
    m = folium.Map(
    location = [36.5053542, 127.7043419],
    zoom_start = 8,
    width='70%', 
    height='100%',
    tiles = 'Stamen Toner'
    )
    
    latlon = [[37.31355679999999, 127.08034150000003],
            [37.35959300000016, 127.105316],
            [37.388204699999996, 126.66208460000007],
            [37.19821445962207, 127.07333060688757],
            [37.3862876275833, 126.96253325015414],
            [37.31864776315991, 127.08885641049494],
            [37.56661020000001, 126.97838810000007]]
    
    latitude = 37.394946
    longitude = 127.111104
    
    folium.Marker([latitude, longitude],tooltip="우리집 입구", icon=folium.Icon('red', icon='star'), popup='<iframe width="560" height="315" src="https://www.youtube.com/embed/dpwTOQri42s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>').add_to(m)
    
    HeatMap(latlon).add_to(m)
    maps2=m._repr_html_()  
    
    mk = folium.Map(location=[37.559819, 126.963895],zoom_start=12,tiles='cartodbpositron')

    folium.GeoJson(seoul_geo,name='지역구').add_to(mk)

    marker_cluster = MarkerCluster().add_to(mk)

    for lat, long in zip(seoul_coffee['위도'], seoul_coffee['경도']):
        folium.Marker([lat, long], icon = folium.Icon(color="green")).add_to(marker_cluster)
    
    maps3=mk._repr_html_()  
    
    mk2 = folium.Map(location=[37.559819, 126.963895],zoom_start=11, tiles='cartodbpositron') 
    folium.GeoJson(seoul_geo,name='지역구').add_to(mk2)

    mk2.choropleth(geo_data=seoul_geo,data=seoul_group_data,fill_color='YlOrRd', fill_opacity=0.5,line_opacity=0.2,key_on='properties.name',legend_name="지역구별 커피 업종 수")
    
    maps4=mk2._repr_html_()
    ptpt()
    ptpt2()
    
    context = {'map' : maps, 'm' : maps2, 'mk' : maps3, 'mk2' : maps4}
    return render(request, 'home/home.html', context)