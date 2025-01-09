from django.contrib import admin
from .models import PostCategory, Post, Comment, ReportPost, BombPost

# Register your models here.
admin.site.register(PostCategory) # 카테고리 생성에 슈퍼유저가 관여할 수 있도록 설정합니다.
admin.site.register(Post) # 관리자가 임의로 포스트를 관리할 수 있도록 합니다.
admin.site.register(Comment) # 관리자가 임의로 댓글을 관리할 수 있도록 합니다.
admin.site.register(ReportPost) # 관리자가 임의로 신고 게시물을 관리할 수 있도록 합니다.
admin.site.register(BombPost) # 관리자가 임의로 폭발 게시물을 관리할 수 있도록 합니다.