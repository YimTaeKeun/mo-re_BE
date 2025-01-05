from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or # 읽기와 같은 안전모드에 있으면 통과
            (request.user and request.user.is_authenticated and
             obj.author == request.user) # 쓰고, 수정하고, 삭제하는 권한은 실제 owner만 가능합니다.
            # TODO 해당 퍼미션이 정확하게 동작하는지는 실전 배포에 가야 테스트 가능
            # 현재로선 익명 유저와 인증된 유저 사이의 차이점 구분하는 데에는 성공, 인증된 유저가 게시물 등록하다는 것까지 성공
        )