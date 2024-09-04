from .serializers import *
from .selectors.abstracts import BookReviewSelector
from typing import List, Dict
from user.models import User


class BookReviewService:
    def __init__(self, selector: BookReviewSelector):
        self.selector = selector

    def get_all_briefreviews(self, book_id: int) -> List:
        bookreviews = self.selector.get_BookReview_by_bookid(book_id= book_id)
        serializers = BriefReviewAllSerializer(bookreviews, many=True)
        return serializers.data

    def get_all_bookreviews_by_book(self, book_id: int) -> List:
        bookreviews = self.selector.get_BookReview_by_bookid(book_id= book_id)
        serializers = BookReviewDetailSerializer(bookreviews, many=True)
        return serializers.data

    def get_all_bookreview_by_user(self, user_id: int) -> List:
        bookreviews = self.selector.get_BookReview_by_user_id(user_id=user_id)
        serializers = UserBookReviewSerializer(bookreviews, many=True)
        return serializers.data

    def get_each_bookreview_by_review_id(self, user_id: int, review_id: int) -> "Optional[Dict]":
        bookreview = self.selector.get_BookReview_by_review_id(review_id=review_id)
        entry_user = get_object_or_404(User, id=user_id)
        if (bookreview.disclosure is False) and (bookreview.user == entry_user):
            serializer = EachReviewSerializer(bookreview)
            return serializer.data
        else:
            return None