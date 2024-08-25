from .serializers import *
from .selectors.abstracts import BookReviewSelector
from typing import List, Dict


class BookReviewService:
    def __init__(self, selector: BookReviewSelector):
        self.selector = selector

    def get_all_briefreviews(self, book_id: int) -> List:
        bookreviews = self.selector.get_BookReview_by_bookid(book_id= book_id)
        serializers = BriefReviewAllSerializer(bookreviews)
        return serializers.data