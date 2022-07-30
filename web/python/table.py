import sqlite3 as sql
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
conn = sql.connect(BASE_DIR / "db.sqlite3", check_same_thread=False)
cursor = conn.cursor()


def reservation_table():
    temp = "create table reservation\
            (\
                res_user varchar(150) not null,\
                res_movie text not null,\
                res_date text not null, \
                foreign key(res_user) references join_user(username),\
                foreign key(res_movie) references movie(movie_name)\
            )\
        "
    cursor.execute(temp)
    conn.commit()

def movie_table():
    temp = "create table movie\
            (\
                movie_name text primary key not null,\
                movie_name_en text not null,\
                movie_year text not null,\
                movie_rel_date text not null,\
                movie_country text not null,\
                movie_cate text not null,\
                movie_rating text not null,\
                movie_director text not null,\
                movie_img text not null,\
                movie_total_viewer integer not null,\
                movie_reserve text not null,\
                movie_star text not null,\
                movie_price integer not null\
            )\
        "
    cursor.execute(temp)
    conn.commit()

def moviedate_table():
    temp = "create table moviedate\
            (\
                moviedate_movie text not null,\
                moviedate_date text not null,\
                moviedate_total_seat integer not null,\
                moviedate_reserve_seat integer not null,\
                moviedate_remain_seat integer not null,\
                foreign key(moviedate_movie) references movie(movie_name)\
            )\
        "
    cursor.execute(temp)
    conn.commit()


def movie_insert():
    temp = []
    with open("D:/Workspace/My/HRD/Project/mini_project1/table/movie.csv", 'r', encoding='UTF-8') as f:
        for line in f:
            line = line.strip()
            if line == '':
                break
            line = line.split(',')
            if line[0] == '\ufeffmovie_name':
                continue
            else:
                temp = 'insert into movies_movie\
                        (\
                            movie_name, movie_name_en, movie_year, movie_rel_date, movie_country, movie_cate, movie_rating,\
                            movie_director, movie_img, movie_total_viewer, movie_reserve, movie_star, movie_price\
                        )\
                        values\
                        (\
                            "{}", "{}", {}, "{}", "{}", "{}", "{}", "{}", "{}", {}, "{}", {}, {}\
                        )\
                        '.format(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9]
                                , line[10], line[11], line[12])
                cursor.execute(temp)
        conn.commit()



def moviedate_insert():
    temp = []
    with open("D:/Workspace/My/HRD/Project/mini_project1/table/moviedate.csv", 'r', encoding='UTF-8') as f:
        for line in f:
            line = line.strip()
            if line == '':
                break
            line = line.split(',')
            if line[0] == '\ufeffmoviedate_movie':
                continue
            else:
                temp = 'insert into movies_moviedate\
                        (\
                            moviedate_movie, moviedate_date, moviedate_total_seat, moviedate_reserve_seat, moviedate_remain_seat\
                        )\
                        values\
                        (\
                            "{}", "{}", {}, {}, {}\
                        )\
                        '.format(line[0], line[1], line[2], line[3], line[4])
                cursor.execute(temp)
        conn.commit()

















if __name__ == '__main__':
    # movie_table()
    # moviedate_table()
    # reservation_table()
    movie_insert()    
    moviedate_insert()
    


    