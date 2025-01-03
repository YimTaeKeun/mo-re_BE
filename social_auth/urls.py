from django.urls import path
from .views import KakaoCallback, RefreshTokens

# url 패턴을 지정합니다. BaseUrl/socialLogin/
urlpatterns = [
    # 카카오 콜백 함수로 리다이렉트
    path('kakaoCallback/', KakaoCallback, name='kakao_callback'),
    path('kakaoRefresh/', RefreshTokens.as_view({
        'post': 'create'
    }), name='kakao_refresh'),
]