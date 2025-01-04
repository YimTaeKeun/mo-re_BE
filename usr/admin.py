from django.contrib import admin
from .models import User, BlackListUser

# Register your models here.

admin.site.register(User) # 유저 모델을 관리자가 관리할 수 있도록 등록합니다.
admin.site.register(BlackListUser) # 블랙스트 모델을 슈퍼 유저가 관리할 수 있도록 합니다.