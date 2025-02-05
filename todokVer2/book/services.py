from .serializers import *
from .selectors.abstracts import BookSelector
from typing import List, Dict
from datetime import date
from django.db import transaction, connection

class BookService:
    def __init__(self, selector: BookSelector):
        self.selector = selector

    def get_ing_books(self, user_id: int) -> List:
        userbooks = self.selector.get_ing_userbooks_by_user_id(user_id=user_id)
        serializers = IngUserBookSerializer(userbooks, many=True)
        return serializers.data

    def get_recommended_books(self, user_id: int) -> List:
        book_queryset = self.selector.get_books_by_fav_genre(user_id=user_id)
        serializers = RecommendBookSerializer(book_queryset, many=True)
        return serializers.data

    def get_all_booksentences(self) -> List:
        booksentences = self.selector.get_booksentences(self)
        serializers = BookSentenceSerializer(booksentences, many=True)
        return serializers.data

    def get_detail_book(self, book_id: int) -> Dict:
        book_obj = self.selector.get_book_by_bookid(book_id=book_id)
        bookdetail_obj = BookDetail.objects.get(book=book_obj)
        serializers = BookDetailSerializer(bookdetail_obj)
        return serializers.data

    def get_userbook_detail(self, user_id: int, book_id: int) -> Dict:
        userbook_obj = self.selector.get_userbook_detail_by_ids(user_id=user_id, book_id=book_id)
        serializers = UserBookDetailSerializer(userbook_obj)
        return serializers.data

    def save_reading_pages(self,user_id: int, book_id: int, pages: int) -> int:
        userbook = self.selector.get_userbook_detail_by_ids(user_id=user_id, book_id=book_id)
        entire_pages = userbook.book.entire_pages
        if entire_pages == 0:
            return 0
        userbook.reading_pages = pages
        userbook.reading_percent = int((pages/entire_pages)*100)
        today_str = str(date.today())
        reading_days_list = userbook.reading_days
        if today_str not in reading_days_list:
            reading_days_list.append(today_str)
        if pages == entire_pages:
            userbook.status = 0    # 완독 상태로 바꾸기
        userbook.save()
        return userbook.reading_percent

    def get_entire_pages(self, user_id: int, book_id: int) -> int:
        userbook = self.selector.get_userbook_detail_by_ids(user_id=user_id, book_id=book_id)
        return userbook.book.entire_pages

    def remove_userbook(self, user_id: int, book_id: int) -> None:
        userbook = self.selector.get_userbook_detail_by_ids(user_id=user_id, book_id=book_id)
        userbook.delete()

    def get_all_books(self, user_id: int) -> List:
        userbooks = self.selector.get_all_userbooks_by_user_id(user_id=user_id)
        serializer = AllUserBookSerializer(userbooks, many=True)
        return serializer.data

    def delete_all_books_and_details(self):
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM `todoktodok`.`BookDetail`;")
                    cursor.execute("DELETE FROM `todoktodok`.`Book`;")
        except Exception as e:
            # 예외가 발생하면 자동으로 롤백됨.
            print(f"An error occurred: {e}")