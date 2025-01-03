from django.test import TestCase

# Create your tests here.

class AuthorizationTest(TestCase):
    # 로그인을 테스트합니다.
    def testLogin(self):
        # TODO 인가코드로서 매 테스트마다 바꿔줘야합니다.
        code = 'ojCllX-3oCmkfs-3rM9jqdDQ1PsntvsRc7ycBgjF2H4K_ACSJG1MjAAAAAQKPCQfAAABlCtKDKPgLMgnBn6ZSw'
        response = self.client.get('/socialLogin/kakaoCallback/?code=' + code)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/socialLogin/kakaoCallback/?cod=' + code)
        print(response.json())
        self.assertEqual(response.status_code, 400)

    # 리프레시 토큰을 테스트합니다.
    def testRefresh(self):
        # TODO 리프레시 토큰으로서 유효기간이 만료되면 바꿔줘야합니다.
        data = {
            'refresh_token': 'pbZZHeOq9TsJBPQgA-URNdOUoDlhxp__AAAAAgo9cusAAAGUKtVQgeQ1KlcE_6bt',
        }
        response = self.client.post('/socialLogin/kakaoRefresh/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print(response.json())
        # 리프레시 토큰 정보를 body에서 발견하지 못한 경우를 테스트 합니다.
        data = {
            # 일부러 틀린 정보를 넣습니다.
            'ref': '',
        }
        response = self.client.post('/socialLogin/kakaoRefresh/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print(response.json())
        # 토큰 정보 자체를 변환해서 테스트합니다.
        data = {
            'refresh_token': '1pbZZHeOq9TsJBPQgA-URNdOUoDlhxp__AAAAAgo9cusAAAGUKtVQgeQ1KlcE_6bt',
        }
        response = self.client.post('/socialLogin/kakaoRefresh/', data=data, content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 400)