from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import *
from .services import BookReviewService
from .selectors.abstracts import BookReviewSelector

class BriefReviewAllAPIView(APIView):
    def get(self, request, book_id):
        brief_reviews = BookReviewService(BookReviewSelector).get_all_briefreviews(book_id=book_id)
        return Response({"brief_review":brief_reviews}, status=status.HTTP_200_OK)