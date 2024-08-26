from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import *
from .services import BookReviewService
from .selectors.abstracts import BookReviewSelector
from book.services import BookService
from book.selectors.abstracts import BookSelector

class BookReviewAPIView(APIView):
    def post(self, request, user_id, book_id):
        serializer = BookReviewSaveSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id, book_id, request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)


class BriefReviewAllAPIView(APIView):
    def get(self, request, book_id):
        brief_reviews = BookReviewService(BookReviewSelector).get_all_briefreviews(book_id=book_id)
        return Response({"brief_review":brief_reviews}, status=status.HTTP_200_OK)


class BookReviewDetailAPIView(APIView):
    def get(self, request, book_id):
        book_detail_dict = BookService(BookSelector).get_userbook_detail(book_id=book_id)
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