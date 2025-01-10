from django.test import TestCase
from .models import User

# Create your tests here.

ACCESS_TOKEN = 'N_tlzdsd16mgXflb9o0O4N2VwwN4y-ObAAAAAQoqJREAAAGUT2HQHeQ1KlcE_6bt'

class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 테스트 사용자 정보를 등록해줍니다.
        User.objects.create(
            sub=3857463839,
            username='임태근'
        )

    def test_specifying_user(self): # 액세스 토큰 유저 정보 반환 api를 테스트합니다.
        headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
        print(headers)
        response = self.client.get('/user/me/', headers=headers)
        print(response.json())
        self.assertEqual(response.status_code, 200)
