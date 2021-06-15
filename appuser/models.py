from django.contrib.admin.views import main
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AppUser(models.Model):
    name = models.CharField(
        max_length=100
    )
    token = models.CharField(
        max_length=100
    )
    secret_key = models.CharField(
        max_length=100
    )
    is_enable = models.BooleanField(
        default=False
    )


class AppUserLog(models.Model):
    app_user = models.ForeignKey(
        AppUser, on_delete=models.PROTECT
    )
    create_at = models.DateTimeField(
        auto_now_add=True
    )
    path = models.CharField(
        max_length=20
    )
