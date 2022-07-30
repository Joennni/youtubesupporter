from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import date, timedelta
import sql.sql as sql
import datetime
import random
# Create your views here.

def lottery_game():
    game_set = list(range(1,11))
    my = random.choice(game_set)
    com = random.choice(game_set)
    if my == com:
        result = 'win'
    else:
        result = 'lose'
    return result

############################################################

def movie_list(request):
    name, img, star = sql.movie_list('movie_star', asc='desc')
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
    total_count = len(temp1)
    context = {"data": temp2, "total": total_count}
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request, name):
    col, row = sql.movie_detail(name)
    context = {'data': list(zip(col, row))}
    return render(request, 'movies/movie_detail.html', context)

def reserve(request, name, date=date.today()):
    if type(date) == str:
        today = datetime.date.today()
    else:
        today = date
        date = date.isoformat()
    col, d1, d2, d3, d4, d5, d6 = sql.movie_reserve(name, date)
    one_day = timedelta(days=1)
    # dat = []
    # for _ in range(10):
    #     # dat.append(today.isoformat()[5:])
    #     dat.append(today.isoformat())
    #     today = today + one_day
    dat = [
        '2022-05-03', '2022-05-04', '2022-05-05', '2022-05-06', '2022-05-07', 
        '2022-05-08', '2022-05-09', '2022-05-10', '2022-05-11', '2022-05-12', 
    ]
    context = {'col': col, "date": dat, "name":name
                ,"m_name": d1,"total_seat": d2,"reserve_seat": d3
                ,"remain_seat": d4,"img": d5,"res_day": date
                ,"price": d6}
    return render(request, 'movies/reserve.html', context)

def reserve_result(request, name, user, date, price):
    if request.method != 'POST':
        current_point = sql.point_checker(user)
        if current_point < price:
            result3 = False
            ap = '포인트가 부족합니다.'
        else:
            result3 = sql.point_inserter(user, 1000-price)
            ap = sql.point_checker(user)
            result1 = sql.reserve_inserter(name,user,date)
            result2 = sql.movie_res_updater(name, date)
        msg = 'not click'
        lottery = ' '
    else:
        result3, ap = True, sql.point_checker(user)
        msg = 'click'
        if lottery_game() == 'win':
            lottery = '당첨! 50000 포인트 증정!'
            tmp = sql.point_inserter(user, 50000)
        else:
            lottery = '낙첨..'

    context = {'result': result3, "price": price,
                'after_point': ap, "name":name,
                'lottery': lottery, 'msg':msg}
    return render(request, 'movies/reserve_result.html', context)
