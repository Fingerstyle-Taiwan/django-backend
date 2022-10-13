'''
Database models.
'''
import uuid
import os

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.conf import settings
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


def avatar_image_file_path(instance, filename):
    ''' Generate file path for new recipe image. '''
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'avatar', filename)


def artist_image_file_path(instance, filename):
    ''' Generate file path for artist images. '''
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'artist', filename)


class UserManager(BaseUserManager):
    '''
    Manager for users.
    '''
    def create_user(self, email, password=None, **extra_fields):
        '''
        Create and Save User
        '''
        if not email:
            raise ValueError('User must have an email. ')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        ''' Create and return a new superuser. '''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''
    User Model
    '''
    email = models.EmailField(max_length=255, unique=True, verbose_name='信箱')
    name = models.CharField(max_length=255, verbose_name='暱稱')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = "用戶"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'


class Profile(models.Model):
    ''' Profile Model '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(null=True, blank=True,
                               upload_to=avatar_image_file_path,
                               verbose_name='頭貼')
    GENDER_CHOICES = (
        ('MALE', _('男生')),
        ('FEMALE', _('女生')),
        ('OTHER', _('其他'))
    )
    gender = models.CharField(max_length=6,
                              choices=GENDER_CHOICES,
                              default='OTHER',
                              verbose_name='性別')
    bio = RichTextField(null=True, blank=True, verbose_name='簡介')
    birthdate = models.DateField(null=True, blank=True, verbose_name='生日')
    country = CountryField(blank_label='(選擇國家/地區)', default='TW',
                           verbose_name='國家/地區')
    guitar_brand = models.CharField(max_length=20, null=True,
                                    blank=True, verbose_name='吉他品牌')
    guitar_model = models.CharField(max_length=20, null=True,
                                    blank=True, verbose_name='吉他型號')

    def __str__(self) -> str:
        return self.user.name

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Contest(models.Model):
    
    name = models.CharField(max_length=255, null=True,
                            blank=True, verbose_name='活動名稱')
    date = models.CharField(max_length=255, null=True,
                            blank=True, verbose_name='活動開始結束')
    origanizer = models.CharField(max_length=255, null=True,
                            blank=True, verbose_name='活動單位')
    link = models.CharField(max_length=255, null=True,
                            blank=True, verbose_name='活動連結')
    image = models.ImageField(max_length=255, null=True,
                            blank=True, verbose_name='活動圖片')
    tags = ArrayField(models.CharField(max_length=255), 
                             null=True, blank=True, verbose_name='活動tags')
    class Meta:
        verbose_name = _("活動")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name


class Artist(models.Model):
    ''' Artist Model. '''
    name = models.CharField(max_length=30, verbose_name='名字')
    avatar = models.ImageField(null=True, blank=True,
                               upload_to=artist_image_file_path,
                               verbose_name='頭貼')
    cover = models.ImageField(null=True, blank=True,
                              upload_to=artist_image_file_path,
                              verbose_name='封面照片')
    country = CountryField(blank_label='(選擇國家/地區)', default='TW',
                           verbose_name='國家/地區')
    information = RichTextField(null=True, blank=True, verbose_name='簡介')
    website = models.URLField(max_length=200, blank=True,
                              verbose_name='個人網站')
    fb_link = models.URLField(max_length=200, blank=True,
                              verbose_name='Facebook')
    ig_link = models.URLField(max_length=200, blank=True,
                              verbose_name='Instagram')
    yt_link = models.URLField(max_length=200, blank=True,
                              verbose_name='Youtube')

    def __str__(self) -> str:
        return self.name

