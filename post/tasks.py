from .models import (
    Post, # 게시물 삭제를 위해
    BombPost # 삭제 타겟 조회 위해
)

from celery import shared_task # shared_task는 장고와 연관이 있는 작업일 때 사용하는 어노테이션 입니다.
from celery.utils.log import get_task_logger # 로거 임포트

from django.utils import timezone

logger = get_task_logger(__name__) # 현재 모듈명을 기반으로 로거 생성


@shared_task
def check_and_bomb_post(): # 매 분마다 task 실행 후, 게시물을 폭파시킵니다.
    logger.info('폭파 스케쥴이 실행됩니다.')
    objects = BombPost.objects.filter(bombTime__lte=timezone.now())
    if objects.count() != 0: # 삭제 대상이 하나라도 존재한다면
        try:
            for obj in objects:
                logger.info(f'제목: {obj.targetPost.title} 아이디: {obj.targetPost.id} 을(를) 삭제 시도합니다.')
                obj.targetPost.delete() # 대상 오브젝트 삭제를 시도합니다.
                logger.info('제거가 완료되었습니다.')
            logger.info('모든 대상 게시물 제거가 완료되었습니다.')
        except Exception as e:
            logger.error(f'삭제 중 오류 발생: {e}', exc_info=True)
