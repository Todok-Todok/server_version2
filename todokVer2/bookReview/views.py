from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import *
from .services import BookReviewService
from .selectors.abstracts import BookReviewSelector
from book.services import BookService
from book.selectors.abstracts import BookSelector
from rest_framework.pagination import LimitOffsetPagination

class BookReviewAPIView(APIView):
    def post(self, request, user_id, book_id):
        response_dict = {"user_id": user_id, "book_id": book_id}

        serializer = BookReviewRequestSaveSerializer(data=request.data, context=response_dict)
        if serializer.is_valid(raise_exception=True):
            bookreview = serializer.save(user_id, book_id, request.data)
            serializer_saved = BookReviewResponseSaveSerializer(bookreview)
            return Response(serializer_saved.data, status=status.HTTP_200_OK)

class BriefReviewAllAPIView(ListAPIView):
    serializer_class = BriefReviewAllSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        book_id = self.kwargs.get('book_id')
        return BookReviewSelector.get_BookReview_by_bookid(book_id=book_id)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

class BookReviewDetailAPIView(APIView):
    def get(self, request, user_id, book_id):
        book_detail_dict = BookService(BookSelector).get_userbook_detail(user_id=user_id, book_id=book_id)
        book_reviews = BookReviewService(BookReviewSelector).get_all_bookreviews_by_book(book_id=book_id)
        return Response({"book_detail": book_detail_dict,"book_review":book_reviews}, status=status.HTTP_200_OK)

class UserBookReviewListAPIView(APIView):
    def get(self, request, user_id):
        reviews_list = BookReviewService(BookReviewSelector).get_all_bookreview_by_user(user_id=user_id)
        return Response({"result": reviews_list},status=status.HTTP_200_OK)

class EachBookReviewAPIView(APIView):
    def get(self, request, user_id, review_id):
        review = BookReviewService(BookReviewSelector).get_each_bookreview_by_review_id(user_id=user_id, review_id=review_id)
        if review is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(review, status=status.HTTP_200_OK)