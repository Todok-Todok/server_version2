from django.urls import path
from . import views

urlpatterns = [
    path('brief/all/<int:book_id>/', views.BriefReviewAllAPIView.as_view()),
    path('ongoing/<int:user_id>/<int:opponent_user_id>/<int:book_id>/', views.BookReviewDetailAPIView.as_view()),
    path('<int:user_id>/<int:book_id>/', views.BookReviewAPIView.as_view()),
    path('all/<int:user_id>/', views.UserBookReviewListAPIView.as_view()),
    path('each/<int:user_id>/<int:review_id>/', views.EachBookReviewAPIView.as_view()),
    path('recommend/<int:review_id>/', views.RecommendReviewsAPIView.as_view()),
    path('aiquestions/<int:user_id>/<int:book_id>/', views.GenerateAIQuestionsAPIView.as_view())
]