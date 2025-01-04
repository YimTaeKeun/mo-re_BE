from django.contrib import admin
from .models import User

# Register your models here.

admin.site.register(User) # 유저 모델을 관리자가 관리할 수 있도록 등록합니다.