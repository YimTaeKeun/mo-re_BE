from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # username: Abstract User 필드 사용, 카카오 ID 토큰의 nickname으로 부터 추출하여 저장
    sub = models.IntegerField(primary_key=True) # pk, 유저 고유 회원 번호를 의미하며, 카카오 ID 토큰으로 부터 추출합니다.
    addDate = models.DateTimeField(auto_now_add=True) # 유저 가입 날짜
