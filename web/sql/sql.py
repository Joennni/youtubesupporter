import sqlite3 as sql
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
conn = sql.connect(BASE_DIR / "db.sqlite3", check_same_thread=False)
cursor = conn.cursor()

##유저포인트 조회
def point_checker(name):
    temp = "select user_point\
            from join_user\
            where username = '{}'".format(name)
    cursor.execute(temp)
    current_point = cursor.fetchall()[0][0]
    return current_point

##유저포인트 업데이트
def point_inserter(name, bet):
    try:
        temp = "update join_user\
                set user_point = user_point + {}\
                where username = '{}'".format(bet, name)
        cursor.execute(temp)
        conn.commit()
        return True
    except:
        return False

##예매정보
def resInfo(name):
    temp = 'select res_movie, res_date\
            from movies_reservation \
            where res_user = "{}"\
            order by res_date desc'.format(name)
    cursor.execute(temp)
    row = cursor.fetchall()
    res_name = []
    res_date = []
    for i in row:
        res_name.append(i[0])
        res_date.append(i[1])
    return res_name, res_date

##내정보
def myInfo(name):
    temp = 'select username, user_point\
            from join_user \
            where username = "{}"'.format(name)
    cursor.execute(temp)
    row = cursor.fetchall()
    name = row[0][0]
    point = format(row[0][1], ',d')
    return name, point

##영화리스트
def movie_list(order, search = '', asc='asc'):
    temp = 'select movie_name, movie_img, movie_star\
            from movies_movie\
            where movie_name like "%{}%"\
            order by "{}" {}'.format(search, order, asc)
    cursor.execute(temp)
    row = cursor.fetchall()
    name = []
    img = []
    star = []
    for i in row:
        name.append(i[0])
        img.append(i[1])
        star.append(i[2])
    return name, img, star

##영화상세
def movie_detail(name):
    temp = 'select * \
            from movies_movie \
            where movie_name = "{}"'.format(name)
    cursor.execute(temp)
    row = cursor.fetchall()
    col = [i[0][6:] for i in cursor.description]
    tmp = []
    count = 0
    for i in row[0]:
        if col[count] == 'total_viewer' or col[count] == 'price':
            tmp.append(format(i, ',d'))    
        else:
            tmp.append(i)
        count += 1
    return col, tmp

##예매페이지
def movie_reserve(name, date):
    temp = 'select moviedate_movie, moviedate_total_seat, moviedate_reserve_seat, moviedate_remain_seat, movie_img, movie_price\
            from movies_moviedate inner join movies_movie on (moviedate_movie = movie_name) \
            where moviedate_movie = "{}"\
                and moviedate_date = "{}"'.format(name, date)
    cursor.execute(temp)
    row = cursor.fetchall()
    col = [i[0] for i in cursor.description]
    m_name = row[0][0]
    total_seat = row[0][1]
    reserve_seat = row[0][2]
    remain_seat = row[0][3]
    img = row[0][4]
    price = row[0][5]
    return col, m_name, total_seat, reserve_seat, remain_seat, img, price

##예매insert
def reserve_inserter(name, user, date):
    try:
        temp = "INSERT INTO movies_reservation(res_movie,res_user,res_date) \
                VALUES('{}','{}','{}')".format(name, user, date)
        cursor.execute(temp)
        conn.commit()
    except:
        return False
    return True

##좌석업데이트
def movie_res_updater(name, date):
    try:
        temp = "update movies_moviedate\
                set moviedate_remain_seat = moviedate_remain_seat - 1,\
                    moviedate_reserve_seat = moviedate_reserve_seat + 1\
                where movies_moviedate_movie = '{}'\
                    and moviedate_date = '{}'".format(name, date)
        cursor.execute(temp)
        conn.commit()
    except:
        return False
    return True

##유저리스트
def getUserName():
    temp = 'select username\
            from join_user'
    cursor.execute(temp)
    row = cursor.fetchall()
    temp = []
    for i in row:
        temp.append(i[0])
    return temp


#################################################################################
##사용안함

##댓글작성
def answerInsert(answer_contents, answer_date, answer_author, answer_question_id):
    try:
        temp = "insert into board_answer(answer_contents, answer_date, answer_author, answer_question_id)\
                values('{}', '{}', '{}', {})".format(answer_contents, answer_date, answer_author, answer_question_id)
        cursor.execute(temp)
        return True
    except:
        return False
