from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from book.models import Book
from user.models import User
from readingNote.models import *
from typing import Dict, Optional, List
from datetime import date

class AbstractReadingNoteSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_prereadingnotes_by_bookid(book_id: int) -> "QuerySet[PreReadingNote]":
        pass

    @abstractmethod
    def get_prereadingnote_by_userbook(user_id: int, book_id: int) -> PreReadingNote:
        pass

    @abstractmethod
    def get_readingnote_by_userbook(user_id: int, book_id: int) -> ReadingNote:
        pass

    @abstractmethod
    def get_readingnote_by_id(note_id: int) -> ReadingNote:
        pass

    @abstractmethod
    def get_today_readingnote(user_id: int, book_id: int) -> "QuerySet[ReadingNote]":
        pass

    @abstractmethod
    def get_todayquestion(genre: str) -> ExQuestionOngoing:
        pass

    @abstractmethod
    def get_one_note_by_book(book: Book) -> ReadingNote:
        pass

class ReadingNoteSelector(AbstractReadingNoteSelector):
    def get_one_note_by_book(book: Book) -> ReadingNote:
        return ReadingNote.objects.filter(book=book).order_by('?').first()

    def get_prereadingnotes_by_bookid(book_id: int) -> "QuerySet[PreReadingNote]":
        book = get_object_or_404(Book, book_id=book_id)
        return PreReadingNote.objects.filter(book=book)

    def get_readingnote_by_id(note_id: int) -> ReadingNote:
        return get_object_or_404(ReadingNote, id=note_id)

    def get_readingnote_by_userbook(user_id: int, book_id: int) -> ReadingNote:
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        return ReadingNote.objects.get(user=user,book=book)

    def get_today_readingnote(user_id: int, book_id: int) -> "QuerySet[ReadingNote]":
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        return ReadingNote.objects.filter(user=user, book=book, written_at=date.today())

    def get_todayquestion(genre: str) -> ExQuestionOngoing:
        return ExQuestionOngoing.objects.filter(genre=genre).order_by('?').first()

    def get_prereadingnote_by_userbook(user_id: int, book_id: int) -> PreReadingNote:
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        return PreReadingNote.objects.get(user=user, book=book)