from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
import uuid
from .validation import *


# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StudentClass(BaseModel):
    cls_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.cls_name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True, default="", validators=[validate_email])
    mobile = models.CharField(max_length=15, unique=True, validators=[validate_mobile_number])
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    cls = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name='user', blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    status = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_inactive = models.BooleanField(default=False)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email', ]
    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.email, self.mobile)
