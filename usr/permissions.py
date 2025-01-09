from rest_framework.permissions import BasePermission
from rest_framework import permissions
from usr.models import BlackListUser
import logging
logger = logging.getLogger('django')


# 블랙리스트 유저 검사 로직
def checkBlackList(sub):
    try:
        user = BlackListUser.objects.get(sub=sub)
        logger.info('차단됨. 사유: ' + user.reason)
        return True # 블랙리스트에 속함
    except BlackListUser.DoesNotExist:
        return False # 블랙리스트에 있지않아 False로 반환

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # 해당 유저가 블랙리스트에 속해 있는지 검사합니다.
        isBlack = False
        if request.user.is_authenticated: # 익명의 유저가 아니라면
            isBlack = checkBlackList(request.user.sub)

        return bool(
            request.method in permissions.SAFE_METHODS or # 읽기와 같은 안전모드에 있으면 통과
            (request.user and request.user.is_authenticated and
             (not isBlack) and  # 블랙리스트에 속하는 유저가 아니라면
             obj.author == request.user) # 쓰고, 수정하고, 삭제하는 권한은 실제 owner만 가능합니다.
            # TODO 해당 퍼미션이 정확하게 동작하는지는 실전 배포에 가야 테스트 가능
            # 현재로선 익명 유저와 인증된 유저 사이의 차이점 구분하는 데에는 성공, 인증된 유저가 게시물 등록하다는 것까지 성공
        )

# 관리자만 접근하도록 허가하는 퍼미션 클래스 입니다.
class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        isBlack = False
        if request.user.is_authenticated: isBlack = checkBlackList(request.user.sub)
        return bool(
            request.method in permissions.SAFE_METHODS or  # 읽기와 같은 안전모드에 있으면 통과
            (request.user and request.user.is_authenticated and # 인증된 사용자인가
             (not isBlack) and  # 블랙리스트에 속하는 유저가 아니라면
            request.user.is_staff) # 그 인증된 사용자가 관리자인가
        )

# 블랙리스트가 아닌 사람만 DB에 관여할 수 있으며, 모든 사람은 읽기 권한을 가집니다.
class IsNotBlackAndAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        isBlack = False
        if request.user.is_authenticated: isBlack = checkBlackList(request.user.sub)
        if isBlack:
            logger.info('회원번호 ' + str(request.user.sub) + ' 회원명 ' + str(request.user.username) + '이(가) 블랙리스트 유저로서 접근 차단되었습니다.')
        return bool(
            request.method in permissions.SAFE_METHODS or  # 읽기와 같은 안전모드에 있으면 통과
            (request.user and request.user.is_authenticated and  # 인증된 사용자인가
             (not isBlack)) # 블랙리스트에 속하는 유저가 아니라면
        )

# 블랙리스트에 등록되어 있는 사람 제외 모든 사람에게 허용되는 권한입니다.
class IsNotBlack(BasePermission):
    def has_permission(self, request, view):
        isBlack = False
        if request.user.is_authenticated: isBlack = checkBlackList(request.user.sub)
        return bool(not isBlack) # 블랙리스트 아닌 사람만 혀용이 가능합니다.