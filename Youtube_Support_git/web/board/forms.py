from django import forms
from django.forms import ModelForm
from board.models import Question
from .models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['question_title', 'question_contents']  # QuestionForm에서 사용할 Question 모델의 속성
        widgets = {
            'question_title': forms.TextInput(attrs={'class': 'form-control'}),
            'question_contents': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')