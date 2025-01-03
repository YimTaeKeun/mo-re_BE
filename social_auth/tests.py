from django.test import TestCase

# Create your tests here.

class AuthorizationTest(TestCase):
    # 로그인을 테스트합니다.
    def testLogin(self):
        # TODO 인가코드로서 매 테스트마다 바꿔줘야합니다.
        code = 'fi2K_UU-vI9oZRwoq4ydjy4z9ucXkcke_LjHh7drkJ6IcX4KNOwZvQAAAAQKKcjZAAABlCrRuUi2W8wW6V7rJg'
        response = self.client.get('/socialLogin/kakaoCallback/?code=' + code)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    # 리프레시 토큰을 테스트합니다.
    def testRefresh(self):
        # TODO 리프레시 토큰으로서 유효기간이 만료되면 바꿔줘야합니다.
        data = {
            'refresh_token': 'pbZZHeOq9TsJBPQgA-URNdOUoDlhxp__AAAAAgo9cusAAAGUKtVQgeQ1KlcE_6bt',
        }
        response = self.client.post('/socialLogin/kakaoRefresh/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print(response.json())