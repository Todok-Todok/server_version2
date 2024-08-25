from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from .models import *
from book.models import Book
from typing import Dict, Optional, List
import random

class AbstractBookReviewSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_BookReview_by_bookid(book_id: int) -> "QuerySet[BookReview]":
        pass
class BookReviewSelector(AbstractBookReviewSelector):
    def get_BookReview_by_bookid(book_id: int) -> "QuerySet[BookReview]":
        book = get_object_or_404(Book, book_id=book_id)
        return BookReview.objects.filter(book=book)