from pyexpat import model
from django.db import models
from django.urls import reverse
# from django.core import models as core_models
# from users import models as user_models
from django.contrib.auth.models import User as user_models

# Create your models here.
class Question(models.Model):
    question_title = models.CharField(max_length=200)
    question_author = models.CharField(max_length=200)
    question_contents = models.TextField()
    question_date = models.DateTimeField()
    question_view = models.IntegerField(default=0)
    
    def __str__(self):
        return self.question_title

class Answer(models.Model):
    answer_question_id = models.ForeignKey(Question, on_delete=models.CASCADE, db_column='answer_question_id')
    answer_author = models.CharField(max_length=200)
    answer_contents = models.TextField()
    answer_date = models.DateTimeField()
    
class Comment1(models.Model):
    index_no = models.IntegerField()
    com_count = models.IntegerField()
    mem_name = models.TextField()
    video_name = models.TextField()
    com_id = models.TextField()
    comment = models.TextField()
    comment_get = models.TextField()
    commemt_get_day = models.TextField()
    commemt_get_time = models.TextField()
    sense = models.TextField()
    sense_set = models.TextField()
    sense_score = models.FloatField()
    
    def __str__(self):
        return self.comment
    
class Member_time(models.Model):
    mem_name = models.TextField()
    activation = models.TextField()
    activation_day = models.TextField()
    activation_time = models.TextField()
    
class Capture(models.Model):
    mem_name = models.TextField()
    video_name = models.TextField()
    img_path = models.TextField()
    capture_get = models.TextField()
    capture_get_day = models.TextField()
    capture_get_time = models.TextField()
    
class Script(models.Model):
    index_no = models.IntegerField()
    script_count = models.IntegerField()
    mem_name = models.TextField()
    video_name = models.TextField()
    time = models.TextField()
    script = models.TextField()
    script_get = models.TextField()
    script_get_day = models.TextField()
    script_get_time = models.TextField()

class Htag(models.Model):
    index_no = models.IntegerField()
    h_count = models.IntegerField()
    mem_name = models.TextField()
    video_name = models.TextField()
    h_tag = models.TextField()
    h_tag_get = models.TextField()
    h_tag_get_day = models.TextField()
    h_tag_get_time = models.TextField()
    
class Member_list(models.Model):
    mem_name = models.TextField()
