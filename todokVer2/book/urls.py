from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.BookSearchInDBAPIView.as_view()),
    path('new/search/', views.SearchAPIView.as_view()),
    path('new/search/each/', views.EachSearchAPIView.as_view()),
    path('add/<int:user_id>/', views.UserBookAPIView.as_view()),
    path('recommend/<int:user_id>/', views.RecommendBookByGenreAPIView.as_view()),
    path('personalizing/', views.BookSentenceAPIView.as_view()),
    path('detail/<int:book_id>/', views.BookDetailAPIView.as_view()),
    path('save/<int:user_id>/<int:book_id>/', views.ReadingPageSaveAPIView.as_view()),
    path('<int:user_id>/<int:book_id>/', views.UserBookRemoveAPIView.as_view()),
    path('all/<int:user_id>/', views.UserBookAllAPIView.as_view()),
    path('crawling/', views.BookCrawlingAPIView.as_view()),
    path('keywords/', views.KeywordsExtractingAPIView.as_view())
]