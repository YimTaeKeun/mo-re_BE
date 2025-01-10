from rest_framework import viewsets, status
from .models import User
from rest_framework.response import Response

# Create your views here.

# 로그인한 사용자가 누구인지 반환합니다.
class SpecifyingUserViewSet(viewsets.ViewSet):
    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated: # 로그인된 사용자라면
            return Response({
                "sub": request.user.sub, # 사용자 고유 id를 반환합니다.
                "username": request.user.username, # 사용자 닉네임 정보를 반환합니다.
            }, status=status.HTTP_200_OK)
        return Response({"Error": "로그인 해주세요."}, status=status.HTTP_403_FORBIDDEN)
