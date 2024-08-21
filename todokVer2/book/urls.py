from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.SearchAPIView.as_view()),
    path('add/<int:user_id>/', views.UserBookAPIView.as_view()),
    path('recommend/<int:user_id>/', views.RecommendBookByGenreAPIView.as_view()),
    path('personalizing/', views.BookSentenceAPIView.as_view())
]