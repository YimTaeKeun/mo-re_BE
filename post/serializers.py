from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (
    Post,
    PostCategory,
    BombPost,
    ReportPost,
    Comment
)

class BombPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BombPost
        fields = ['bombTime']

# 댓글 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    bomb = BombPostSerializer(required=False) # bomb time이 설정되지 않는 경우를 위해 required는 false로 지정
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'category', 'bomb'] # bomb는 relation name으로 포스트와 연결된 폭탄 스케쥴을 말합니다.

    def create(self, validated_data):
        """
        DB에 저장할 때, 호출되는 함수로, bomb 스케쥴과 함께 저장됩니다.
        """
        bomb_data = validated_data.pop('bomb', None) # bomb 스케쥴을 꺼내옵니다.

        # 폭탄 스케쥴과 관련없는 게시물 데이터는 저장합니다.
        post = Post.objects.create(**validated_data)

        # 폭탄 스케쥴링 데이터를 저장합니다.
        if bomb_data:
            BombPost.objects.create(targetPost=post, **bomb_data)

        return post

    def update(self, instance, validated_data):
        """
        put 요청이 들어올 경우에 호출되는 함수입니다.
        """
        # 여기서 instance는 게시물을 말하는 것입니다.
        # instance에는 기존 데이터가 들어오고, validated_data에는 새로들어온 요청이 들어옵니다.
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        # 만약에 폭탄 스케줄 수정이 일어난다면, 데이터를 추출합니다.
        bomb = validated_data.get('bomb', None)
        # bomb 리스트에 해당 게시물이 있었는지 없었는지 파악을 합니다.
        if bomb is not None: # bomb 데이터가 있는 경우
            try:
                bomb_instance = BombPost.objects.get(targetPost=instance)
                # 폭탄 리스트에 등록되어 있었던 경우
                # 폭탄 시리얼라이저를 통해서 저장합니다. 일부 저장은 true
                serializer = BombPostSerializer(bomb_instance, data=bomb, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Post.DoesNotExist: # 폭탄 리스트에 등록되어 있지 않는 경우
                BombPost.objects.create(targetPost=instance, **bomb) # 폭탄 리스트에 등록합니다.

        return instance

    def to_representation(self, instance):
        # 댓글을 제외한 나머지 필드들은 상위 클래스의 to_representation을 통해서 시리얼라이징된 데이터를 얻습니다.
        data = super().to_representation(instance)
        data['comments'] = CommentSerializer(instance.comments.all(), many=True).data # relatedName을 통해 댓글 들을 얻습니다.
        return data

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = '__all__'
