from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm

from .models import User


# Register your models here.
# admin.site.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username','user_point',)}),
        # ('Personal info', {'fields': ('password',)}),
        # ('Permissions', {'fields': ('is_admin',)}),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('password1', 'password2')
    #         }
    #     ),
    # )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)