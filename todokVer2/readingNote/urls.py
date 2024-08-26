from django.urls import path
from . import views

urlpatterns = [
    path('prereading/<int:book_id>/', views.PreReadingNoteAPIView.as_view()),
    #path('ongoing/<int:user_id>/<int:book_id>/', views.OngoingReadingNoteAPIView.as_view()),
    path('base/<int:user_id>/<int:book_id>/', views.ReadingNoteCRUDAPIView.as_view()),
    path('today/<int:user_id>/<int:book_id>/', views.TodayReadingNoteAPIView.as_view()),
    path('todayquestion/<int:book_id>/', views.TodaySampleQuestionAPIView.as_view()),
    path('before/<int:user_id>/<int:book_id>/', views.PreReadingNoteAPIView.as_view())
]