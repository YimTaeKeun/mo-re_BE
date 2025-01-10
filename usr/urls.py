from django.urls import path
from .views import SpecifyingUserViewSet

urlpatterns = [
    # 회원 식별 뷰 매핑
    path('me/', SpecifyingUserViewSet.as_view({
        'get': 'retrieve'
    }), name='who'),
]