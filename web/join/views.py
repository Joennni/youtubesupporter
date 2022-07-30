from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
# from join.forms import UserForm
from join.forms import UserCreationForm, UserChangeForm
from .models import User
from board.models import Question
from django.http import HttpResponse
import sql.sql as sql
# Create your views here.


def signup(request):
    if request.method == "POST":
        # form = UserForm(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('home')
    else:
        # form = UserForm()
        form = UserCreationForm()
    return render(request, 'join/signup.html', {'form': form})

def myInfo(request):
    username = request.user.username
    name, date = sql.resInfo(username)
    user, point = sql.myInfo(username)
    data = list(zip(name, date))
    context = {"data": data,
                "username": user, "point": point}
    return render(request, "join/myInfo.html", context)

def userList(request):
    name = sql.getUserName()
    context = {"nameList": name}
    return render(request, "join/userList.html", context)

def userInfo(request, userName):
    userInfo = get_object_or_404(User, username=userName)
    context = {'userInfo': userInfo, 'userName':userName}
    return render(request, 'join/userInfo.html', context)

def user_delete(request, userName):
    user = get_object_or_404(User, username=userName)
    # if request.user != question.author:
    #     messages.error(request, '삭제권한이 없습니다')
    #     return redirect('pybo:detail', question_id=question.id)
    user.delete()
    return redirect('userList')
    
def admin(request):
    return render(request, 'join/admin.html')

def boardList(request):
    question_list = Question.objects.order_by('-question_date')
    admin = []
    user = []
    for i in question_list:
        if i.question_author == 'admin':
            admin.append(i)
        else:
            user.append(i)
    if admin == []:
        admin = None
    if user == []:
        user = None
    context = {'admin_list': admin, 'user_list':user}
    return render(request, 'join/boardList.html', context)

def boardInfo(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'join/boardInfo.html', context)

def board_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('boardList')