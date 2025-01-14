from .models import (
    Post, # 게시물 삭제를 위해
    BombPost # 삭제 타겟 조회 위해
)

from celery import shared_task # shared_task는 장고와 연관이 있는 작업일 때 사용하는 어노테이션 입니다.

from django.utils import timezone


@shared_task
def check_and_bomb_post(): # 매 분마다 task 실행 후, 게시물을 폭파시킵니다.
    print('폭파 스케쥴이 실행됩니다.')
    objects = BombPost.objects.filter(bombTime__lte=timezone.now())
    if objects.count() != 0: # 삭제 대상이 하나라도 존재한다면
        try:
            for obj in objects:
                print('제목: ' + obj.targetPost.title + ' 아이디: ' + obj.targetPost.id + '을(를) 삭제 시도합니다.')
                obj.targetPost.delete() # 대상 오브젝트 삭제를 시도합니다.
                print('제거가 완료되었습니다.')
        except Exception as e:
            print(e)
        print('모든 대상 게시물 제거가 완료되었습니다.')