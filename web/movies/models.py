from django.db import models

# # Create your models here.
class movie(models.Model):
    movie_name = models.TextField(primary_key=True, unique=True)
    movie_name_en = models.TextField()
    movie_year = models.TextField()
    movie_rel_date = models.TextField()
    movie_country = models.TextField()
    movie_cate = models.TextField()
    movie_rating = models.TextField()
    movie_director = models.TextField()
    movie_img = models.TextField()
    movie_total_viewer = models.IntegerField()
    movie_reserve = models.TextField()
    movie_star = models.TextField()
    movie_price = models.IntegerField()
    
    def __str__(self):
        return self.movie_name


class moviedate(models.Model):
    moviedate_movie = models.ForeignKey('movie', on_delete=models.PROTECT, db_column='moviedate_movie')
    moviedate_date = models.TextField()
    moviedate_total_seat = models.IntegerField()
    moviedate_reserve_seat = models.IntegerField()
    moviedate_remain_seat = models.IntegerField()
    
    def __str__(self):
        return self.moviedate_movie


class reservation(models.Model):
    res_movie = models.ForeignKey('movie', on_delete=models.PROTECT, db_column='res_movie')
    res_user = models.ForeignKey('join.user', on_delete=models.PROTECT, db_column='res_user')
    res_date = models.TextField()

    def __str__(self):
        return self.res_user