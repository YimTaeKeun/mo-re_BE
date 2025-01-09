from django.contrib import admin
from .models import PostCategory, Post

# Register your models here.
admin.site.register(PostCategory) # 카테고리 생성에 슈퍼유저가 관여할 수 있도록 설정합니다.
admin.site.register(Post) # 관리자가 임의로 포스트를 삭제할 수 있도록 합니다.