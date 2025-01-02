import requests
from django.http import JsonResponse
from django.shortcuts import render
from config.settings import KAKAO_REST_API_KEY, BASE_URL
# Create your views here.

def KakaoCallback(request):
    # code는 카카오에서 제공받은 인가코드를 말합니다.
    code = request.GET.get('code') # url 쿼리 파라미터로부터 code를 가져옵니다.
    # 토큰을 발급받기위한 요청 url 입니다.
    token_url = 'https://kauth.kakao.com/oauth/token'
    redirect_uri = BASE_URL + '/socialLogin/kakaoCallback/' # 인가 코드가 들어오는 url 즉 현 뷰의 url을 말합니다.
    # 요청 body
    data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_REST_API_KEY,
        'redirect_uri': redirect_uri,
        'code': code,
    }
    # 요청 헤더
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    }
    # 토큰 발급을 요청합니다.
    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code == 200:
        # TODO: 카카오 유저 정보를 처리합니다.
        return JsonResponse(response.json(), status=200)
    return JsonResponse({"Error": response.text}, status=400)