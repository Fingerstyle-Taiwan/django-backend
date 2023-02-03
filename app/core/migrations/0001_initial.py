# Generated by Django 4.0.8 on 2022-10-13 17:37

import ckeditor.fields
import django.contrib.postgres.fields
import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models

import core.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=255, unique=True, verbose_name="信箱"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="暱稱")),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "用戶",
                "verbose_name_plural": "用戶",
                "ordering": ["-id"],
                "get_latest_by": "id",
            },
        ),
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="名字")),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=core.models.artist_image_file_path,
                        verbose_name="頭貼",
                    ),
                ),
                (
                    "cover",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=core.models.artist_image_file_path,
                        verbose_name="封面照片",
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="TW", max_length=2, verbose_name="國家/地區"
                    ),
                ),
                (
                    "information",
                    ckeditor.fields.RichTextField(
                        blank=True, null=True, verbose_name="簡介"
                    ),
                ),
                ("website", models.URLField(blank=True, verbose_name="個人網站")),
                ("fb_link", models.URLField(blank=True, verbose_name="Facebook")),
                ("ig_link", models.URLField(blank=True, verbose_name="Instagram")),
                ("yt_link", models.URLField(blank=True, verbose_name="Youtube")),
            ],
        ),
        migrations.CreateModel(
            name="Contest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, null=True, verbose_name="活動名稱"),
                ),
                (
                    "date",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="活動開始結束"
                    ),
                ),
                (
                    "organizer",
                    models.CharField(max_length=255, null=True, verbose_name="活動單位"),
                ),
                (
                    "link",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="活動連結"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        max_length=255,
                        null=True,
                        upload_to="",
                        verbose_name="活動圖片",
                    ),
                ),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        blank=True,
                        null=True,
                        size=None,
                        verbose_name="活動tags",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=core.models.avatar_image_file_path,
                        verbose_name="頭貼",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("MALE", "男生"), ("FEMALE", "女生"), ("OTHER", "其他")],
                        default="OTHER",
                        max_length=6,
                        verbose_name="性別",
                    ),
                ),
                (
                    "bio",
                    ckeditor.fields.RichTextField(
                        blank=True, null=True, verbose_name="簡介"
                    ),
                ),
                (
                    "birthdate",
                    models.DateField(blank=True, null=True, verbose_name="生日"),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="TW", max_length=2, verbose_name="國家/地區"
                    ),
                ),
                (
                    "guitar_brand",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="吉他品牌"
                    ),
                ),
                (
                    "guitar_model",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="吉他型號"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
