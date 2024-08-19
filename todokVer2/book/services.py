from book.models import Book, UserBook
# from .serializers import BookViewSerializer, BookTitleSerializer
from .selectors.abstracts import BookSelector
from django.db.models.query import QuerySet
from typing import List, Tuple, Optional, Dict


class BookService:
    def __init__(self, selector: BookSelector):
        self.selector = selector

    def get_ing_books(self, user_id: int) -> :
        mybooks = self.selector.get_ing_books_by_user_id(user_id=user_id)

    def get_all_books(self, user_id: int) -> :
        mybooks = self.selector.get_ing_books_by_user_id(user_id=user_id)