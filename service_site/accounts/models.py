from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    ROLE_CHOICES = (

    ("client", "مشتری"),

    ("developer", "برنامه نویس"),

    ("designer", "طراح"),

    ("manager", "مدیر"),

    )

    role = models.CharField(

        max_length=20,

        choices=ROLE_CHOICES,

        default="client",

    )

    def __str__(self):
        return self.user.username

class Department(models.Model):

    name = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.name

class Employee(models.Model):

    user = models.OneToOneField(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

    )

    department = models.ForeignKey(

        Department,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

    )

    job_title = models.CharField(

        max_length=150,

    )

    hired_at = models.DateField()

    active = models.BooleanField(

        default=True,

    )

    def __str__(self):

        return self.user.get_full_name() or self.user.username