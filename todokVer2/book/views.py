import secret
import asyncio

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from .serializers import BookSerializer, BookSearchSerializer, BookSentenceSerializer
from .models import Book, UserBook, BookSentence
from user.models import User, PersonalizingInfo
from django.shortcuts import get_object_or_404
from .services import BookService
from .selectors.abstracts import BookSelector
from datetime import date
from .bestseller_book_crawling.crawling import BookCrawler, EachBookCrawler
from .bestseller_book_crawling.crawling_additional import AdditionalBookCrawler
from .ai.services import extract_keywords

KAKAO_REST_API_KEY = secret.KAKAO_REST_API_KEY

# Create your views here.
class SearchAPIView(APIView):
    def get(self, request):
        book_name = request.GET['book_name']
        book_list = AdditionalBookCrawler().main(book_name)
        return Response({"result": book_list}, status=status.HTTP_200_OK)

class EachSearchAPIView(APIView):
    def get(self, request):
        book_url = request.data['book_url']
        asyncio.run(EachBookCrawler().get_each_book_info(book_url))
        return Response(status=status.HTTP_201_CREATED)

class UserBookAPIView(APIView):
    # 읽는 중인 책으로 추가
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(): # 유효성 검사
            book = serializer.save() # 저장
        else:
            book = get_object_or_404(Book,title=request.data["title"])
        userbook = UserBook.objects.create(user=user,book=book,saved_at=date.today())
        return Response({"book_id": book.book_id}, status=status.HTTP_201_CREATED)

    # 읽는 중인 책 불러오기
    def get(self, request, user_id):
        books = BookService(BookSelector).get_ing_books(user_id=user_id)
        return Response({"total_count":len(books), "books":books}, status=status.HTTP_200_OK)

class RecommendBookByGenreAPIView(APIView):
    def get(self, request, user_id):
        books_list = BookService(BookSelector).get_recommended_books(user_id=user_id)
        return Response(books_list, status=status.HTTP_200_OK)

class BookSentenceAPIView(ListAPIView):
    queryset = BookSentence.objects.all()
    serializer_class = BookSentenceSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

class BookDetailAPIView(APIView):
    def get(self, request, book_id):
        response = BookService(BookSelector).get_detail_book(book_id=book_id)
        return Response(response, status=status.HTTP_200_OK)

class ReadingPageSaveAPIView(APIView):
    def post(self, request, user_id, book_id):
        reading_percent = BookService(BookSelector).save_reading_pages(user_id=user_id, book_id=book_id, pages=request.data["reading_pages"])
        return Response({"reading_percent":reading_percent}, status=status.HTTP_200_OK)
    def get(self, request, user_id, book_id):
        entire_pages = BookService(BookSelector).get_entire_pages(user_id=user_id, book_id=book_id)
        return Response({"entire_pages":entire_pages}, status=status.HTTP_200_OK)

class UserBookRemoveAPIView(APIView):
    def delete(self, request, user_id, book_id):
        BookService(BookSelector).remove_userbook(user_id=user_id, book_id=book_id)
        return Response(status=status.HTTP_200_OK)

class UserBookAllAPIView(APIView):
    def get(self, request, user_id):
        book_list = BookService(BookSelector).get_all_books(user_id=user_id)
        return Response({"result": book_list}, status=status.HTTP_200_OK)

class BookCrawlingAPIView(APIView):
    def get(self, request):
        BookCrawler().main()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        BookService(BookSelector).delete_all_books_and_details()
        return Response(status=status.HTTP_200_OK)


class BookSearchInDBAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        personalizing = PersonalizingInfo.objects.get(user=user)

        book_name = request.GET['search']
        personalizing.recent_search_history.append(book_name)
        personalizing.save()

        response = super().list(request, *args, **kwargs)
        return response

class KeywordsExtractingAPIView(APIView):
    def post(self, request):
        keywords_list = extract_keywords(request.data["review_content"])
        return Response({"keywords": keywords_list}, status=status.HTTP_200_OK)
