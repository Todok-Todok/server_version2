from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('base/<int:user_id>/', views.UserInfoAPIView.as_view()),
    path('base/login/', views.LoginAPIView.as_view()),
    # 소셜로그인
    # 구글
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
    # 카카오
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
]