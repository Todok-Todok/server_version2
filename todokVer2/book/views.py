import secret
import requests
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import BookSerializer,UserBookSerializer
from .models import Book, UserBook
from user.models import User
from django.shortcuts import get_object_or_404
from .services import BookService
from .selectors.abstracts import BookSelector

KAKAO_REST_API_KEY = secret.KAKAO_REST_API_KEY

# Create your views here.
class SearchAPIView(APIView):
    def get(self, request):
        book_name = request.GET['book_name']
        headers = {"Authorization": "KakaoAK "+KAKAO_REST_API_KEY}
        doc = requests.get(
            f"https://dapi.kakao.com/v3/search/book?query={book_name}", headers=headers)
        doc = doc.json()
        # title #doc['documents'][0]['title']
        # author #', '.join(doc['documents'][0]['authors'])
        # book_image #doc['documents'][0]['thumbnail']
        # publisher #doc['documents'][0]['publisher']
        return Response(doc, status=status.HTTP_200_OK)

class UserBookAPIView(APIView):
    # 읽는 중인 책으로 추가
    def post(self, request, b_status, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(): # 유효성 검사
            book = serializer.save() # 저장
        else:
            book = get_object_or_404(Book,title=request.data["title"])
        userbook = UserBook.objects.create(user=user,book=book,status=b_status)
        return Response(status=status.HTTP_201_CREATED)

    # 파라미터 값이 1일 때 : 읽는 중인 책 불러오기
    # 파라미터 값이 0일 때 : 전체 책 불러오기
    def get(self, request, b_status, user_id):
        user = get_object_or_404(User, id=user_id)
        books = BookService(BookSelector).get_mybooks(user_id=user_id,b_status=b_status)
        return Response(books, status=status.HTTP_200_OK)