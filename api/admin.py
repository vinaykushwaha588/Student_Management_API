from django.contrib import admin
from .models import *


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile', 'email', 'is_inactive', 'is_superuser', 'is_active',)


admin.site.register(User, UserAdmin)


class StudentClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'cls_name',)


admin.site.register(StudentClass, StudentClassAdmin)
