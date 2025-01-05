from django.urls import path
from .views import (
    PostViewSet,
    PostCategoryViewSet, CommentViewSet
)

urlpatterns = [
    path('detail/', PostViewSet.as_view({
        'post': 'create' # create만 pk 없이 진행 (메소드 매치)
    })),
    path('detail/<int:pk>/', PostViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'partial_update',
    })),
    # 카테고리 end point
    path('categories/', PostCategoryViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('categories/<int:pk>/', PostCategoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    # 댓글 저장 end point
    path('comment/save/', CommentViewSet.as_view({
        'post': 'create',
    })),
    # 댓글 삭제, 수정 end point
    path('comment/<int:pk>/', CommentViewSet.as_view({
        'delete': 'destroy',
        'put': 'partial_update',
    }))
]