from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from bookReview.models import *
from book.models import Book
from user.models import User
from typing import List, Tuple
from django.db.models import Q
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

    @abstractmethod
    def get_allBookReviewKeywords_by_review_id(review_id: int) -> Tuple[BookReview, List[List[str]]]:
        pass

    @abstractmethod
    def get_reviews_by_keywords(keywords: List[str]) -> "QuerySet[BookReview]":
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

    def get_allBookReviewKeywords_by_review_id(review_id: int) -> Tuple[BookReview, List[List[str]]]:
        bookreview = BookReview.objects.get(bookreview_id=review_id)
        return bookreview, BookReview.objects.filter(book=bookreview.book).exclude(bookreview_id=review_id).values_list("keywords", flat=True)

    def get_reviews_by_keywords(keywords: List[str]) -> "QuerySet[BookReview]":
        if not keywords:
            return BookReview.objects.none()  # 빈 리스트가 들어오면 빈 QuerySet 반환

        # Q 객체를 사용하여 OR 조건으로 필터링
        query = Q()
        for keyword in keywords:
            query |= Q(keywords__icontains=keyword)

        # 필터링을 적용하고 중복 제거
        reviews = BookReview.objects.filter(query).distinct()

        return reviews
