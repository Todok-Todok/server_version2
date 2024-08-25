from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from book.models import Book, UserBook, BookSentence
from user.models import User, PersonalizingInfo
from typing import Dict, Optional, List
import random

class AbstractBookSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_ing_userbooks_by_user_id(user_id: int) -> "Queryset[UserBook]":
        pass
    @abstractmethod
    def get_books_by_fav_genre(user_id: int) -> "Queryset[Book]":
        pass

    @abstractmethod
    def get_booksentences(self) -> "Queryset[BookSentence]":
        pass

    @abstractmethod
    def get_book_by_bookid(self) -> Book:
        pass

class BookSelector(AbstractBookSelector):
    def get_ing_userbooks_by_user_id(user_id: int) -> "Queryset[UserBook]":
        user = get_object_or_404(User, id=user_id)
        book_objects = UserBook.objects.filter(user=user, status=1).order_by("saved_at")
        return book_objects

    def get_books_by_fav_genre(user_id: int) -> "Queryset[Book]":
        user = get_object_or_404(User, id=user_id)
        fav_genre_list = PersonalizingInfo.objects.get(user=user).fav_genre_keywords
        books = Book.objects.filter(genre__in=fav_genre_list).order_by('?')[:4]
        return books

    def get_booksentences(self) -> "Queryset[BookSentence]":
        return BookSentence.objects.all()

    def get_book_by_bookid(book_id: int) -> Book:
        return get_object_or_404(Book, book_id=book_id)