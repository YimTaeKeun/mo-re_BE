from django.db import models

from usr.models import User


# Create your models here.

class PostCategory(models.Model):
    # id: 해당 모델의 pk로 카테고리 번호로 활용됩니다.
    categoryName = models.CharField(max_length=50) # 카테고리 이름을 의미합니다.
    addDate = models.DateTimeField(auto_now_add=True) # 카테고리 추가 날짜와 시간을 의미합니다.

class Post(models.Model):
    # id: pk로 포스트 번호로 활용됩니다.
    title = models.CharField(max_length=120) # 포스트 제목을 말합니다.
    content = models.TextField() # 포스트 내용을 말합니다. 글자 수 제한은 없습니다.
    addDate = models.DateTimeField(auto_now_add=True) # 포스트 추가 날짜와 시간을 말하며 자동으로 추가됩니다.
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 포스트 작성자를 말하며 User의 pk를 받아옵니다.
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE) # 해당 포스트가 속한 카테고리르 말하며 카테고리 모델의 pk를 받아옵니다.

class BombPost(models.Model):
    # id: pk이며, 폭파 번호를 의미합니다.
    targetPost = models.OneToOneField(Post, on_delete=models.CASCADE) # 폭파를 할 게시물을 의미하며 pk를 받아옵니다.
    bombTime = models.DateTimeField() # 폭파 예정 시간대를 의미합니다. 자동 추가가 아닌, 반드시 폭파 시간대를 받아와야 합니다. 해당 필드는 celery schedule을 통해 사용됩니다.

class ReportPost(models.Model):
    # id: pk이며, 신고 등록 번호를 의미합니다.
    reason = models.TextField() # 신고 사유가 들어갑니다.
    post = models.OneToOneField(Post, on_delete=models.CASCADE) # 신고당한 post를 의미하며 pk를 받아옵니다.
    addDate = models.DateTimeField(auto_now_add=True) # 신고 등록 날짜를 의미하며, 자동으로 시간이 등록됩니다.

