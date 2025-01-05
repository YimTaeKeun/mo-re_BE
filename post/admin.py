from django.contrib import admin
from .models import PostCategory

# Register your models here.
admin.site.register(PostCategory) # 카테고리 생성에 슈퍼유저가 관여할 수 있도록 설정합니다.