import random
from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from readingNote.models import ReadingNote
from book.models import Book
from typing import Dict, Optional, List

class AbstractReadingNoteSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_one_note_by_book(book: Book) -> ReadingNote:
        pass

class ReadingNoteSelector(AbstractReadingNoteSelector):
    def get_one_note_by_book(book: Book) -> ReadingNote:
        queryset_list = ReadingNote.objects.filter(book=book)
        return random.choice(queryset_list)
