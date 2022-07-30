import django.utils.timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        try:
            user = self.model(
                username=username,
            )
            extra_fields.setdefault('user_point', 10000)
            extra_fields.setdefault('is_staff', False)
            extra_fields.setdefault('is_superuser', False)
            extra_fields.setdefault('date_joined', django.utils.timezone.now)
            user.set_password(password)
            user.is_active = True
            user.save()
            return user
        except Exception as e:
            print(e)

    def create_superuser(self, username, password, **extra_fields):
        try:
            superuser = self.create_user(
                username=username,
                password=password,
            )
            superuser.is_superuser = True
            superuser.is_active = True
            # superuser.is_staff = True
            superuser.is_admin = True
            superuser.save()
            return superuser
        except Exception as e:
            print(e)


class User(AbstractBaseUser):
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username', primary_key=True)
    user_point = models.IntegerField(default=10000)
    date_joined = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')
    is_superuser = models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



