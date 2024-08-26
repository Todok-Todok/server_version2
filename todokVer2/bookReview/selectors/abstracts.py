from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from bookReview.models import *
from book.models import Book
from user.models import User
from typing import Dict, Optional, List
import random

class AbstractBookReviewSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_BookReview_by_bookid(book_id: int) -> "QuerySet[BookReview]":
        pass

    @abstractmethod
    def get_BookReview_by_user_id(user_id: int) -> "QuerySet[BookReview]":
        pass

    @abstractmethod
    def get_BookReview_by_review_id(review_id: int) -> BookReview:
        pass

class BookReviewSelector(AbstractBookReviewSelector):
    def get_BookReview_by_bookid(book_id: int) -> "QuerySet[BookReview]":
        book = get_object_or_404(Book, book_id=book_id)
        return BookReview.objects.filter(book=book)

    def get_BookReview_by_user_id(user_id: int) -> "QuerySet[BookReview]":
        user = get_object_or_404(User, id=user_id)
        return BookReview.objects.filter(user=user)

    def get_BookReview_by_review_id(review_id: int) -> BookReview:
        return BookReview.objects.get(bookreview_id=review_id)