from book.models import Book, UserBook
from .serializers import *
from .selectors.abstracts import BookSelector
from django.db.models.query import QuerySet
from typing import List, Tuple, Optional, Dict


class BookService:
    def __init__(self, selector: BookSelector):
        self.selector = selector

    def get_ing_books(self, user_id: int) -> List:
        userbooks = self.selector.get_ing_userbooks_by_user_id(user_id=user_id)
        serializers = IngUserBookSerializer(userbooks)
        return serializers.data

    def get_recommended_books(self, user_id: int) -> List:
        book_queryset = self.selector.get_books_by_fav_genre(user_id=user_id)
        serializers = RecommendBookSerializer(book_queryset)
        return serializers

    def get_all_booksentences(self) -> List:
        booksentences = self.selector.get_booksentences()
        serializers = BookSentenceSerializer(booksentences)
        return serializers