from .serializers import *
from .selectors.abstracts import BookSelector
from typing import List, Dict


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
        return serializers.data

    def get_all_booksentences(self) -> List:
        booksentences = self.selector.get_booksentences()
        serializers = BookSentenceSerializer(booksentences)
        return serializers.data

    def get_detail_book(self, book_id: int) -> Dict:
        book_obj = self.selector.get_book_by_bookid(book_id=book_id)
        bookdetail_obj = BookDetail.objects.get(book=book_obj)
        serializers = BookDetailSerializer(bookdetail_obj)
        return serializers.data