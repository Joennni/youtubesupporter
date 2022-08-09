from django.contrib import admin
from .models import movie, moviedate, reservation

# Register your models here.
admin.site.register(movie)
admin.site.register(moviedate)
admin.site.register(reservation)