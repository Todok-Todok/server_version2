from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from .models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from .selectors.abstracts import UserSelector
from .services import UserService

import secret


class RegisterAPIView(APIView):
    # 자체 회원가입
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)  # Token Create
            res = Response(
                {
                    #"user": serializer.data,
                    #"message": "register successs",
                    "user_id": user.id,
                },
                status=status.HTTP_200_OK)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 자체 로그인
# 유저 인증
class LoginAPIView(APIView):
    def post(self, request):
        user = authenticate(email=request.data["email"], password=request.data["password"])
        # 이미 회원가입 된 유저일 때
        # serializer = UserSerializer(instance=user)
        update_last_login(None, user)
        # 토큰 접근
        if user:
            try:
                # user를 통해 token get
                token = Token.objects.get(user=user)
            except:
                # [FIX]: token이 없는 경우 (token 생성 이후 기간이 지나 token이 만료되어 사라진 경우) token 재생성
                token = Token.objects.create(user=user)
            res = Response(
                {
                    #"user": serializer.data,
                    #"message": "login success",
                    "user_id": user.id
                },
                status=status.HTTP_200_OK)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserInfoAPIView(APIView):
    # 유저 정보 확인
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OnBoardingAPIView(APIView):
    def post(self, request):
        serializer = OnboardingUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(request.data)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class MyInfoAPIView(APIView):
    def get(self, request, user_id):
        user = UserSelector.get_user_userid(user_id=user_id)
        return Response({"email": user.email}, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        password_type = request.GET.get('type', None)
        if password_type == 'past':
            result = UserService(UserSelector).change_password(user_id=user_id,type=0,password=request.data["password"])
        else:
            result = UserService(UserSelector).change_password(user_id=user_id,type=1,password=request.data["password"])

        if result is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)

class RecentSearchedAPIView(APIView):
    def get(self, request, user_id):
        recent_searched = UserSelector.get_personal_info(user_id=user_id)
        return Response({"result":recent_searched.recent_search_history}, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        UserService(UserSelector).remove_one_history(user_id,request.data["content"])
        return Response(status=status.HTTP_200_OK)


# 소셜로그인
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

import requests
from allauth.socialaccount.models import SocialAccount

from rest_framework.decorators import api_view

'''
1. google_login 실행 후 로그인 성공 시, Callback 함수로 Code 값 전달받음
2. 받은 Code로 Google에 Access Token 요청
3.  Access Token으로 Email 값을 Google에게 요청
4. 전달받은 Email, Access Token, Code를 바탕으로 회원가입/로그인 진행
'''

state = getattr(secret, 'STATE')
BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'user/google/callback/'
KAKAO_CALLBACK_URI = BASE_URL + 'user/kakao/callback/'


# Create your views here.
@api_view(('POST', 'GET'))
def google_callback(request):
    data = {'access_token': request.data['access_token']}
    """
    Signup or Signin Request
    """
    try:
        print("try문 들어옴")
        user = User.objects.get(email=request.data['email'])
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return Response({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return Response({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        accept = requests.post(
            f"{BASE_URL}user/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return Response({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        # accept_json.pop('user', None)
        return Response(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        accept = requests.post(
            f"{BASE_URL}user/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return Response({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)  # 유저 정보 (pk, email) 는 response에서 빼고 싶을 때 !
        return Response(accept_json)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


# ------- 카카오 로그인 ------ #
KAKAO_REST_API_KEY = secret.KAKAO_REST_API_KEY


@api_view(('POST', 'GET'))
def kakao_callback(request):
    """
    Email Request
    """
    # profile_request = requests.get(
    #     "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    # profile_json = profile_request.json()
    # kakao_account = profile_json.get('kakao_account')
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    #print(kakao_account)
    email = request.data['email']
    data = {'access_token': request.data['access_token']}
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return Response({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return Response({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        accept = requests.post(
            f"{BASE_URL}user/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return Response({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        # accept_json.pop('user', None)
        return Response(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        accept = requests.post(
            f"{BASE_URL}user/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return Response({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        return Response(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
