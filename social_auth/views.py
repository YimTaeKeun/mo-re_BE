import requests
from django.http import JsonResponse
from django.shortcuts import render
from config.settings import KAKAO_REST_API_KEY, CLIENT_BASE_URL
from rest_framework import status, viewsets
from rest_framework.response import Response
from usr.models import User
import jwt
import logging
# Create your views here.
logger = logging.getLogger('django') # 로거 설정

def KakaoCallback(request):
    # code는 카카오에서 제공받은 인가코드를 말합니다.
    code = request.GET.get('code', None) # url 쿼리 파라미터로부터 code를 가져옵니다.
    # 인가 코드가 추출되지 않는 경우 예외 처리
    if code is None:
        return JsonResponse({"Error": "인가 코드 추출 실패"}, status=status.HTTP_400_BAD_REQUEST)
    # 토큰을 발급받기위한 요청 url 입니다.
    token_url = 'https://kauth.kakao.com/oauth/token'
    redirect_uri = CLIENT_BASE_URL + '/socialLogin/kakaoCallback/' # 인가 코드가 들어오는 url 즉 현 뷰의 url을 말합니다.
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
        id_token = response.json().get('id_token', None)
        # 아이디 토큰이 존재하지 않는다면 -> 예외처리
        if id_token is None:
            return JsonResponse({"Error": "id 토큰이 존재하지 않습니다.", "ErrorResponse": response.json()})
        # 유저 확인
        try:
            isNew = checkOrCreateUser(id_token)
        except Exception as e: # sub와 nickname 없는 오류 catch
            return JsonResponse({"Error": str(e)})
        data = dict()
        data['access_token'] = response.json().get('access_token', None) # 액세스 토큰 추가
        data['token_type'] = response.json().get('token_type', None) # token 타입 정보 추가
        data['refresh_token'] = response.json().get('refresh_token', None) # 리프레시 토큰 정보 추가
        data['isNew'] = isNew # 회원가입인지 로그인인지 확인하기 위한 용도
        return JsonResponse(data, status=200)
    return JsonResponse({"Error": response.text}, status=status.HTTP_400_BAD_REQUEST)

def checkOrCreateUser(id_token):
    payload = jwt.decode(id_token, options={"verify_signature": False}) # id_token payload decode

    sub = payload.get('sub', None) # 회원 고유 번호를 조회합니다.
    username = payload.get('nickname', None) # 닉네임을 조회합니다.

    if sub is None or username is None: # 회원 고유 번호 혹은 닉넴임을 조회할 수 없는 경우
        raise Exception("회원 고유 번호 혹은 닉네임을 찾을 수 없습니다.")

    try:
        user = User.objects.get(sub=sub) # 유저가 있으면 아무 행동도 취하지 않습니다.
        logger.info('회원번호 ' + str(sub) + ' ' + str(username) + '이(가) 로그인을 완료하였습니다.')
    except User.DoesNotExist: # 유저가 없으므로 새로운 유저 생성
        logger.info('회원번호 ' + str(sub) + ' ' + str(username) + '이(가) 회원가입을 완료하였습니다.')
        User.objects.create(sub=sub,
                            username=username)
        return True # 회원가입인 경우
    return False # 기존 회원 정보가 있어 단순 유저 로그인인 경우



class RefreshTokens(viewsets.ViewSet):

    # 토큰 요청 Json 요청 하나를 보냅니다.
    def create(self, request):
        # refresh_token 파싱
        refresh_token = request.data.get('refresh_token', None)
        # refresh_token이 body에 존재하지 않는다면
        if refresh_token is None:
            return Response({"Error": "Refresh token is missing"}, status=400)
        # 리프레시 토큰이 있는경우
        # 토큰을 발급받기위한 요청 url 입니다.
        token_url = 'https://kauth.kakao.com/oauth/token'
        # 요청 헤더
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        }
        data = {
            'grant_type': 'refresh_token',
            'client_id': KAKAO_REST_API_KEY,
            'refresh_token': refresh_token,
        }
        # 헤더와 정보를 조합하여 정보를 보냅니다.
        response = requests.post(token_url, data=data, headers=headers)
        # 올바른 정보가 넘어왔다면
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        # 만일 토큰 정보가 잘못되었거나, refresh_token마저 만료 된경우, 혹은 카카오 측 오류인 경우
        return Response({"Error": response.text}, status=status.HTTP_400_BAD_REQUEST)