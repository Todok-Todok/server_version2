from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from book.models import Book, UserBook
from user.models import User
from typing import Dict, Optional, List

class AbstractBookSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_ing_books_by_user_id(user_id: int) -> "List[Queryset[Book]]":
        pass


class BookSelector(AbstractBookSelector):
    def get_ing_books_by_user_id(user_id: int) -> "List[Queryset[Book]]":
        responsebody = []
        user = get_object_or_404(User, id=user_id)
        book_objects = UserBook.objects.filter(user=user, status=1).values_list("book", flat=True).order_by("book_id")
        # books = Book.objects.filter(book_id__in=book_objects).order_by('book_id')
        # responsebody.append(books)
        # return responsebody