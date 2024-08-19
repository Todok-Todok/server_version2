from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.SearchAPIView.as_view()),
    path('mybook/<int:b_status>/<int:user_id>/', views.UserBookAPIView.as_view())
]