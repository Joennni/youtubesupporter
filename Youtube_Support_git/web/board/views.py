from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm
from django.core.paginator import Paginator
from .forms import *
from .models import *
import sqlite3
from django.db.models import Q


# Create your views here.
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.POST.get('content') == '':
        return redirect('detail', question_id=question.id)       
    else:
        question.answer_set.create(answer_contents=request.POST.get('content'), answer_date=timezone.now(), answer_author=request.user.username)
    return redirect('detail', question_id=question.id)


def index(request, num=0, large_num=0):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-question_date')
    admin = []
    user = []
    for i in question_list:
        if i.question_author == 'admin':
            admin.append(i)
        else:
            user.append(i)
    paginator = Paginator(user, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'admin_list': admin, 'user_list': page_obj}
    return render(request, 'board/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.question_view += 1
    question.save()
    context = {'question': question}
    return render(request, 'board/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.question_date = timezone.now()
            question.question_author = request.user.username
            question.save()
            return redirect('index') ##불러오는게 name임 이거
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'board/question_form.html', context)


# @login_required(login_url='login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # if request.user != question.author:
    #     messages.error(request, '수정권한이 없습니다')
    #     return redirect('detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'board/question_form.html', context)


def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # if request.user != question.author:
    #     messages.error(request, '삭제권한이 없습니다')
    #     return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('index')


def SoHyun_Act(request):
    page = request.GET.get("page",'1')
    act_all = Member_time.objects.filter(mem_name = 'SoHyun')
    paginator = Paginator(act_all, 10)
    act = paginator.get_page(page)
    
    context = {"act": act}
    return render(request,"support/support_Sohyun_Act.html",context)

def SoHyun_Com(request):   
    
    # 조회테이블 
    query = request.GET.get('q')    
    template = "support/support_Sohyun_Com.html"     
    all_entries = Comment1.objects.filter(mem_name = 'SoHyun') 
    
    # 검색데이터가 있을 때
    if query:
        # 감정분석 시각화 그래프그리기
        labels = []
        labels2 = []
        data = []
        data2 = []
        labels.append('positive')
        labels.append('negative')
        labels2.append('positive_strog')
        labels2.append('positive_week')
        labels2.append('negative_strog')
        labels2.append('negative_week')
        p1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SoHyun', sense_set = 'positive')).count()
        pg1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SoHyun', sense_set = 'positive') & Comment1.objects.filter(sense_score__gt = 79)).count()
        pg2=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SoHyun', sense_set = 'positive') & Comment1.objects.filter(sense_score__lt = 79)).count()
        n1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SoHyun', sense_set = 'negative')).count()
        ng1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SoHyun', sense_set = 'negative') & Comment1.objects.filter(sense_score__gt = 79)).count()
        ng2=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SoHyun', sense_set = 'negative') & Comment1.objects.filter(sense_score__lt = 79)).count()
        data.append(p1)
        data.append(n1)
        data2.append(pg1)
        data2.append(pg2)
        data2.append(ng1)
        data2.append(ng2)
        
        query = request.GET.get('q')
        selected_entries = Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SoHyun')
        
        # Pagination        
        paginator = Paginator(selected_entries, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        selected_entries = paginator.get_page(page)
        
        return render(request, template, {'all_entries':selected_entries, 'query':query,"labels": labels, "data": data, "labels2": labels2, "data2": data2})
    # 검색을 하지 않은 기본상태
    else:
        #감정분석 시각화 그래프그리기
        labels = []
        labels2 = []
        data = []
        data2 = []
        conn = sqlite3.connect("./db.sqlite3")
        cursor = conn.cursor()
        labels.append('positive')
        labels.append('negative')
        labels2.append('positive_strog')
        labels2.append('positive_week')
        labels2.append('negative_strog')
        labels2.append('negative_week')
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SoHyun' and sense_set = 'positive' Group by mem_name")
        p1=cursor.fetchone()
        p1=p1[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SoHyun' and sense_set = 'positive' and sense_score > 79 Group by mem_name")
        pg1=cursor.fetchone()
        pg1=pg1[0]    
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SoHyun' and sense_set = 'positive' and sense_score < 79 Group by mem_name")
        pg2=cursor.fetchone()
        pg2=pg2[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SoHyun' and sense_set = 'negative' Group by mem_name")
        n1=cursor.fetchone()
        n1=n1[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SoHyun' and sense_set = 'negative' and sense_score > 79 Group by mem_name")
        ng1=cursor.fetchone()
        ng1=ng1[0]    
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SoHyun' and sense_set = 'negative' and sense_score < 79 Group by mem_name")
        ng2=cursor.fetchone()
        ng2=ng2[0]
        data.append(p1)
        data.append(n1)
        data2.append(pg1)
        data2.append(pg2)
        data2.append(ng1)
        data2.append(ng2)
        cursor.close() 
        
        # Pagination
        paginator = Paginator(all_entries, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        all_entries = paginator.get_page(page)
        
        return render(request, template, {'all_entries':all_entries, 'query':query, "labels": labels, "data": data, "labels2": labels2, "data2": data2})

def SoHyun_Cap(request):
    page = request.GET.get("page",'1')
    cap_all = Capture.objects.filter(mem_name = 'SoHyun')
    paginator = Paginator(cap_all, 10)
    cap = paginator.get_page(page)
    
    context = {"cap": cap}
    return render(request,"support/support_Sohyun_Cap.html",context)

def SoHyun_Htag(request):
    page = request.GET.get("page",'1')
    tag_all = Htag.objects.filter(mem_name = 'SoHyun')
    paginator = Paginator(tag_all, 10)
    tag = paginator.get_page(page)
    
    context = {"tag": tag}
    return render(request,"support/support_Sohyun_Tag.html",context)

def SoHyun_Script(request):
    page = request.GET.get("page",'1')
    scp_all = Script.objects.filter(mem_name = 'SoHyun')
    paginator = Paginator(scp_all, 10)
    scp = paginator.get_page(page)
    
    context = {"scp": scp}
    return render(request,"support/support_Sohyun_Script.html",context)


def SangA_Act(request):
    page = request.GET.get("page",'1')
    act_all = Member_time.objects.filter(mem_name = 'SangA')
    paginator = Paginator(act_all, 10)
    act = paginator.get_page(page)
    
    context = {"act": act}
    return render(request,"support/support_SangA_Act.html",context)

def SangA_Com(request):    
    
    # 조회테이블 
    query = request.GET.get('q')    
    template = "support/support_SangA_Com.html"     
    all_entries = Comment1.objects.filter(mem_name = 'SangA') 
    
    # 검색데이터가 있을 때
    if query:
        # 감정분석 시각화 그래프그리기
        labels = []
        labels2 = []
        data = []
        data2 = []
        labels.append('positive')
        labels.append('negative')
        labels2.append('positive_strog')
        labels2.append('positive_week')
        labels2.append('negative_strog')
        labels2.append('negative_week')
        p1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SangA', sense_set = 'positive')).count()
        pg1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SangA', sense_set = 'positive') & Comment1.objects.filter(sense_score__gt = 79)).count()
        pg2=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SangA', sense_set = 'positive') & Comment1.objects.filter(sense_score__lt = 79)).count()
        n1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SangA', sense_set = 'negative')).count()
        ng1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SangA', sense_set = 'negative') & Comment1.objects.filter(sense_score__gt = 79)).count()
        ng2=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SangA', sense_set = 'negative') & Comment1.objects.filter(sense_score__lt = 79)).count()
        data.append(p1)
        data.append(n1)
        data2.append(pg1)
        data2.append(pg2)
        data2.append(ng1)
        data2.append(ng2)
        
        query = request.GET.get('q')
        selected_entries = Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'SangA')
        
        # Pagination        
        paginator = Paginator(selected_entries, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        selected_entries = paginator.get_page(page)
        
        return render(request, template, {'all_entries':selected_entries, 'query':query,"labels": labels, "data": data, "labels2": labels2, "data2": data2})
    # 검색을 하지 않은 기본상태
    else:
        #감정분석 시각화 그래프그리기
        labels = []
        labels2 = []
        data = []
        data2 = []
        conn = sqlite3.connect("./db.sqlite3")
        cursor = conn.cursor()
        labels.append('positive')
        labels.append('negative')
        labels2.append('positive_strog')
        labels2.append('positive_week')
        labels2.append('negative_strog')
        labels2.append('negative_week')
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SangA' and sense_set = 'positive' Group by mem_name")
        p1=cursor.fetchone()
        p1=p1[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SangA' and sense_set = 'positive' and sense_score > 79 Group by mem_name")
        pg1=cursor.fetchone()
        pg1=pg1[0]    
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SangA' and sense_set = 'positive' and sense_score < 79 Group by mem_name")
        pg2=cursor.fetchone()
        pg2=pg2[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SangA' and sense_set = 'negative' Group by mem_name")
        n1=cursor.fetchone()
        n1=n1[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SangA' and sense_set = 'negative' and sense_score > 79 Group by mem_name")
        ng1=cursor.fetchone()
        ng1=ng1[0]    
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'SangA' and sense_set = 'negative' and sense_score < 79 Group by mem_name")
        ng2=cursor.fetchone()
        ng2=ng2[0]
        data.append(p1)
        data.append(n1)
        data2.append(pg1)
        data2.append(pg2)
        data2.append(ng1)
        data2.append(ng2)
        cursor.close() 
        
        # Pagination
        paginator = Paginator(all_entries, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        all_entries = paginator.get_page(page)
        
        return render(request, template, {'all_entries':all_entries, 'query':query, "labels": labels, "data": data, "labels2": labels2, "data2": data2})

def SangA_Cap(request):
    page = request.GET.get("page",'1')
    cap_all = Capture.objects.filter(mem_name = 'SangA')
    paginator = Paginator(cap_all, 10)
    cap = paginator.get_page(page)
    
    context = {"cap": cap}
    return render(request,"support/support_SangA_Cap.html",context)

def SangA_Htag(request):
    page = request.GET.get("page",'1')
    tag_all = Htag.objects.filter(mem_name = 'SangA')
    paginator = Paginator(tag_all, 10)
    tag = paginator.get_page(page)
    
    context = {"tag": tag}
    return render(request,"support/support_SangA_Tag.html",context)

def SangA_Script(request):
    page = request.GET.get("page",'1')
    scp_all = Script.objects.filter(mem_name = 'SangA')
    paginator = Paginator(scp_all, 10)
    scp = paginator.get_page(page)
    
    context = {"scp": scp}
    return render(request,"support/support_SangA_Script.html",context)


def MinHee_Act(request):
    page = request.GET.get("page",'1')
    act_all = Member_time.objects.filter(mem_name = 'MinHee')
    paginator = Paginator(act_all, 10)
    act = paginator.get_page(page)
    
    context = {"act": act}
    return render(request,"support/support_MinHee_Act.html",context)

def MinHee_Com(request):
    
    # 조회테이블 
    query = request.GET.get('q')    
    template = "support/support_MinHee_Com.html"     
    all_entries = Comment1.objects.filter(mem_name = 'MinHee') 
    
    # 검색데이터가 있을 때
    if query:
        # 감정분석 시각화 그래프그리기
        labels = []
        labels2 = []
        data = []
        data2 = []
        labels.append('positive')
        labels.append('negative')
        labels2.append('positive_strog')
        labels2.append('positive_week')
        labels2.append('negative_strog')
        labels2.append('negative_week')
        p1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'MinHee', sense_set = 'positive')).count()
        pg1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'MinHee', sense_set = 'positive') & Comment1.objects.filter(sense_score__gt = 79)).count()
        pg2=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'MinHee', sense_set = 'positive') & Comment1.objects.filter(sense_score__lt = 79)).count()
        n1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'MinHee', sense_set = 'negative')).count()
        ng1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'MinHee', sense_set = 'negative') & Comment1.objects.filter(sense_score__gt = 79)).count()
        ng2=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'MinHee', sense_set = 'negative') & Comment1.objects.filter(sense_score__lt = 79)).count()
        data.append(p1)
        data.append(n1)
        data2.append(pg1)
        data2.append(pg2)
        data2.append(ng1)
        data2.append(ng2)
        
        query = request.GET.get('q')
        selected_entries = Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'MinHee')
        
        # Pagination        
        paginator = Paginator(selected_entries, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        selected_entries = paginator.get_page(page)
        
        return render(request, template, {'all_entries':selected_entries, 'query':query,"labels": labels, "data": data, "labels2": labels2, "data2": data2})
    # 검색을 하지 않은 기본상태
    else:
        #감정분석 시각화 그래프그리기
        labels = []
        labels2 = []
        data = []
        data2 = []
        conn = sqlite3.connect("./db.sqlite3")
        cursor = conn.cursor()
        labels.append('positive')
        labels.append('negative')
        labels2.append('positive_strog')
        labels2.append('positive_week')
        labels2.append('negative_strog')
        labels2.append('negative_week')
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'MinHee' and sense_set = 'positive' Group by mem_name")
        p1=cursor.fetchone()
        p1=p1[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'MinHee' and sense_set = 'positive' and sense_score > 79 Group by mem_name")
        pg1=cursor.fetchone()
        pg1=pg1[0]    
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'MinHee' and sense_set = 'positive' and sense_score < 79 Group by mem_name")
        pg2=cursor.fetchone()
        pg2=pg2[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'MinHee' and sense_set = 'negative' Group by mem_name")
        n1=cursor.fetchone()
        n1=n1[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'MinHee' and sense_set = 'negative' and sense_score > 79 Group by mem_name")
        ng1=cursor.fetchone()
        ng1=ng1[0]    
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'MinHee' and sense_set = 'negative' and sense_score < 79 Group by mem_name")
        ng2=cursor.fetchone()
        ng2=ng2[0]
        data.append(p1)
        data.append(n1)
        data2.append(pg1)
        data2.append(pg2)
        data2.append(ng1)
        data2.append(ng2)
        cursor.close() 
        
        # Pagination
        paginator = Paginator(all_entries, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        all_entries = paginator.get_page(page)
        
        return render(request, template, {'all_entries':all_entries, 'query':query, "labels": labels, "data": data, "labels2": labels2, "data2": data2})

def MinHee_Cap(request):
    page = request.GET.get("page",'1')
    cap_all = Capture.objects.filter(mem_name = 'MinHee')
    paginator = Paginator(cap_all, 10)
    cap = paginator.get_page(page)
    
    context = {"cap": cap}
    return render(request,"support/support_MinHee_Cap.html",context)

def MinHee_Htag(request):
    page = request.GET.get("page",'1')
    tag_all = Htag.objects.filter(mem_name = 'MinHee')
    paginator = Paginator(tag_all, 10)
    tag = paginator.get_page(page)
    
    context = {"tag": tag}
    return render(request,"support/support_MinHee_Tag.html",context)

def MinHee_Script(request):
    page = request.GET.get("page",'1')
    scp_all = Script.objects.filter(mem_name = 'MinHee')
    paginator = Paginator(scp_all, 10)
    scp = paginator.get_page(page)
    
    context = {"scp": scp}
    return render(request,"support/support_MinHee_Script.html",context)


def JiHyun_Act(request):
    page = request.GET.get("page",'1')
    act_all = Member_time.objects.filter(mem_name = 'JiHyun')
    paginator = Paginator(act_all, 10)
    act = paginator.get_page(page)
    
    context = {"act": act}
    return render(request,"support/support_JiHyun_Act.html",context)

def JiHyun_Com(request):
    
    # 조회테이블 
    query = request.GET.get('q')    
    template = "support/support_JiHyun_Com.html"     
    all_entries = Comment1.objects.filter(mem_name = 'JiHyun') 
    
    # 검색데이터가 있을 때
    if query:
        # 감정분석 시각화 그래프그리기
        labels = []
        labels2 = []
        data = []
        data2 = []
        labels.append('positive')
        labels.append('negative')
        labels2.append('positive_strog')
        labels2.append('positive_week')
        labels2.append('negative_strog')
        labels2.append('negative_week')
        p1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'JiHyun', sense_set = 'positive')).count()
        pg1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'JiHyun', sense_set = 'positive') & Comment1.objects.filter(sense_score__gt = 79)).count()
        pg2=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'JiHyun', sense_set = 'positive') & Comment1.objects.filter(sense_score__lt = 79)).count()
        n1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'JiHyun', sense_set = 'negative')).count()
        ng1=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'JiHyun', sense_set = 'negative') & Comment1.objects.filter(sense_score__gt = 79)).count()
        ng2=(Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'JiHyun', sense_set = 'negative') & Comment1.objects.filter(sense_score__lt = 79)).count()
        data.append(p1)
        data.append(n1)
        data2.append(pg1)
        data2.append(pg2)
        data2.append(ng1)
        data2.append(ng2)
        
        query = request.GET.get('q')
        selected_entries = Comment1.objects.filter(Q(video_name__icontains=query)|Q(com_id__icontains=query)|Q(comment__icontains=query)|Q(sense__icontains=query)) & Comment1.objects.filter(mem_name = 'JiHyun')
        
        # Pagination        
        paginator = Paginator(selected_entries, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        selected_entries = paginator.get_page(page)
        
        return render(request, template, {'all_entries':selected_entries, 'query':query,"labels": labels, "data": data, "labels2": labels2, "data2": data2})
    # 검색을 하지 않은 기본상태
    else:
        #감정분석 시각화 그래프그리기
        labels = []
        labels2 = []
        data = []
        data2 = []
        conn = sqlite3.connect("./db.sqlite3")
        cursor = conn.cursor()
        labels.append('positive')
        labels.append('negative')
        labels2.append('positive_strog')
        labels2.append('positive_week')
        labels2.append('negative_strog')
        labels2.append('negative_week')
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'JiHyun' and sense_set = 'positive' Group by mem_name")
        p1=cursor.fetchone()
        p1=p1[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'JiHyun' and sense_set = 'positive' and sense_score > 79 Group by mem_name")
        pg1=cursor.fetchone()
        pg1=pg1[0]    
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'JiHyun' and sense_set = 'positive' and sense_score < 79 Group by mem_name")
        pg2=cursor.fetchone()
        pg2=pg2[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'JiHyun' and sense_set = 'negative' Group by mem_name")
        n1=cursor.fetchone()
        n1=n1[0]
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'JiHyun' and sense_set = 'negative' and sense_score > 79 Group by mem_name")
        ng1=cursor.fetchone()
        ng1=ng1[0]    
        cursor.execute("select count(mem_name) from board_comment1 where mem_name = 'JiHyun' and sense_set = 'negative' and sense_score < 79 Group by mem_name")
        ng2=cursor.fetchone()
        ng2=ng2[0]
        data.append(p1)
        data.append(n1)
        data2.append(pg1)
        data2.append(pg2)
        data2.append(ng1)
        data2.append(ng2)
        cursor.close() 
        
        # Pagination
        paginator = Paginator(all_entries, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        all_entries = paginator.get_page(page)
        
        return render(request, template, {'all_entries':all_entries, 'query':query, "labels": labels, "data": data, "labels2": labels2, "data2": data2})

def JiHyun_Cap(request):
    page = request.GET.get("page",'1')
    cap_all = Capture.objects.filter(mem_name = 'JiHyun')
    paginator = Paginator(cap_all, 10)
    cap = paginator.get_page(page)
    
    context = {"cap": cap}
    return render(request,"support/support_JiHyun_Cap.html",context)

def JiHyun_Htag(request):
    page = request.GET.get("page",'1')
    tag_all = Htag.objects.filter(mem_name = 'JiHyun')
    paginator = Paginator(tag_all, 10)
    tag = paginator.get_page(page)
    
    context = {"tag": tag}
    return render(request,"support/support_JiHyun_Tag.html",context)

def JiHyun_Script(request):
    page = request.GET.get("page",'1')
    scp_all = Script.objects.filter(mem_name = 'JiHyun')
    paginator = Paginator(scp_all, 10)
    scp = paginator.get_page(page)
    
    context = {"scp": scp}
    return render(request,"support/support_JiHyun_Script.html",context)


def comment_chart(request):
    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()
    
    cursor.execute("select mem_name, count(mem_name) from board_comment1 group by mem_name")
    row = cursor.fetchall()
    colname = cursor.description
    
    cursor.close()
    conn.close()
    
    values= []
    names = []
    for i in row:
        names.append(i[0])
        values.append(i[1])
    
    # print(names)
    # print(values)
    
    
    context = {'names':names, 'values':values }
    return render(request, "support/comment_chart.html", context)

def hash_chart(request):
    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()
    
    cursor.execute("select mem_name, count(mem_name) from board_htag group by mem_name")
    row = cursor.fetchall()
    colname = cursor.description
    
    cursor.close()
    conn.close()
    
    values= []
    names = []
    for i in row:
        names.append(i[0])
        values.append(i[1])
    
    # print(names)
    # print(values)
    
    
    context = {'names':names, 'values':values }
    return render(request, "support/hash_chart.html", context)

def login_chart(request):
    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()
    
    cursor.execute("select distinct(mem_name), count(mem_name) from board_member_list group by mem_name")
    row = cursor.fetchall()
    # colname = cursor.description
    
    cursor.close()
    conn.close()
    
    values= []
    names = []
    for i in row:
        names.append(i[0])
        values.append(i[1])
    
    # print(names)
    # print(values)
    
    
    context = {'names':names, 'values':values }
    return render(request, "support/login_chart.html", context)

def capture_chart(request):
    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()
    
    cursor.execute("select mem_name, count(mem_name) from board_capture group by mem_name")
    row = cursor.fetchall()
    colname = cursor.description
    
    cursor.close()
    conn.close()
    
    values= []
    names = []
    for i in row:
        names.append(i[0])
        values.append(i[1])
    
    # print(names)
    # print(values)
    
    
    context = {'names':names, 'values':values }
    return render(request, "support/capture_chart.html", context)


