from rest_framework import viewsets, status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# permission class import
from usr.permissions import IsOwnerOrReadOnly

# model import
from .models import (
    BombPost,
    Post,
    PostCategory,
    ReportPost
)
# 시리얼라이저 import
from .serializers import (
    PostSerializer
)

# Create your views here.

# post 관련 뷰를 제작합니다.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly) # 사용자 인증된 사람만 create 할 수 있도록 합니다.
    # 사용자 인증이 안된 사람은 읽기 권한만 가집니다. 이 권한은 추후 변경이 가능할 수 있습니다.
    # POST 요청의 경우 IsAuthenticatedOrReadOnly의 has_permission만 따름
    # 반면, PUT, DELETE 요청의 경우 has_permission 메소드와 함께, 오브젝트를 특정하기 때문에 has_object_permission 메소드도 함께 실행됩니다.

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated: # 글쓴이가 없다면
            return Response({"Error": "작성자가 존재하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy() # request 데이터를 변환할 수는 없으므로 복제를 하여 변환을 시도합니다.

        try:
            # 이름으로 들어온 카테고리를 그 이름에 대응되는 pk값으로 변환하여 저장합니다.
            data['category'] = PostCategory.objects.get(categoryName=data['category']).pk
        except PostCategory.DoesNotExist: # 카테고리가 존재하지 않는다면
            return Response({"ERROR": "해당 카테고리가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)


        data['author'] = request.user.pk # user의 pk 속성을 author 속성을 저장합니다.
        serializer = self.get_serializer(data=data) # 시리얼라이저를 통해서 요청 객체를 시리얼라이저에 할당합니다.
        try:
            serializer.is_valid(raise_exception=True) # 시리얼라이저 형식에 맞는 데이터들이 들어왔는지 검증합니다.
        except ValidationError as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED) # 201 코드 반환




# TODO 시리얼라이저 재 매칭 필요
class PostSimpleViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        # list 메소드는 여러 인스턴스를 반환하는 메소드이므로 simple viewset에 적합합니다.
        return self.list(request, *args, **kwargs) # get 요청이 들어오는 즉시, list 메소드로 전환됩니다.