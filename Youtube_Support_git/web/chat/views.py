from django.contrib.auth.decorators import login_required
import json
from django.utils.safestring import mark_safe

from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })