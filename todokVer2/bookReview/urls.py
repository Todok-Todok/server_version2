from django.urls import path
from . import views

urlpatterns = [
    path('brief/all/<int:book_id>/', views.BriefReviewAllAPIView.as_view()),
]