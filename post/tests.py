from datetime import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.status import HTTP_403_FORBIDDEN

from usr.models import User
from .models import (
    Post,
    BombPost,
    ReportPost,
    PostCategory
)

# Create your tests here.

ACCESS_TOKEN = 'yhANBt-R6xIqHTxs0_w19vLLFa08fHvYAAAAAQo9cxgAAAGUNIBf2eQ1KlcE_6bt'

class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 임의로 카테고리를 만듭니다.
        PostCategory.objects.create(
            categoryName='TestCategory',
        )
        # 액세스 토큰에 해당하는 유저를 임의로 생성합니다.
        User.objects.create(
            username='임태근',
            sub=3857463839
        )
    def test_post(self):
        # 게시물 관련 테스트를 진행합니다.
        # Post Test
        # given
        # 유저를 특정하기 위해 액세스 토큰 헤더가 필요합니다.
        headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
        # when
        data = {
            'title': 'test title',
            'content': 'test content',
            'category': 'TestCategory',
            'bomb': {
                'bombTime': '2025-01-05 12:32:00'
            }
        }
        # then
        response = self.client.post('/post/detail/', data, headers=headers, content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(BombPost.objects.count(), 1)
        print(BombPost.objects.get(pk=1).bombTime)

        # GET Test
        response = self.client.get('/post/detail/1/', headers=headers)
        print(response.json())
        self.assertEqual(response.status_code, 200)

        # PUT Test
        data = {
            'bomb': {
                'bombTime': '2025-01-05 14:23:43'
            }
        }
        response = self.client.put('/post/detail/1/', data, headers=headers, content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 200)


        # Anonymous User Test
        response = self.client.get('/post/detail/1/')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # No Category Test
        data = {
            'title': 'test title',
            'content': 'test content',
            'category': 'TestCategory1',
            'bomb': {
                'bombTime': '2025-01-05 12:32:00'
            }
        }
        response = self.client.post('/post/detail/', data, headers=headers)
        self.assertEqual(response.status_code, 404)

        # Anonymous POST Test
        response = self.client.post('/post/detail/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # IsAuthenticated에서 막힘

        # Anonymous PUT Test
        response = self.client.put('/post/detail/1/', data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN) # IsAuthenticated에서 막힘

        # DELETE TEst
        response = self.client.delete('/post/detail/1/', headers=headers)
        self.assertEqual(response.status_code, 204)

    def test_category(self):
        headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
        data = {
            'categoryName': 'Hello',
        }
        response = self.client.post('/post/categories/', data, headers=headers)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # 201 created 통과 -> 관리자 퍼미션 통과
        # GET Test
        response = self.client.get('/post/categories/', headers=headers)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
