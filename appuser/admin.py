from django.contrib import admin

# Register your models here.
from appuser.models import AppUser

admin.site.register(AppUser)
