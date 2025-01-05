from django.urls import path
from .views import (
    PostViewSet
)

urlpatterns = [
    path('detail/', PostViewSet.as_view({
        'post': 'create' # create만 pk 없이 진행 (메소드 매치)
    })),
    path('detail/<int:pk>/', PostViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'partial_update',
    }))
]