from .serializers import *
from .selectors.abstracts import BookReviewSelector
from readingNote.selectors.abstracts import ReadingNoteSelector
from readingNote.serializers import ReadingNoteContentSerializer
from typing import List, Dict
from user.models import User

from .ai.services import find_similar_keywords, generate_questions


class BookReviewService:
    def __init__(self, selector: BookReviewSelector):
        self.selector = selector

    def get_all_briefreviews(self, book_id: int) -> List:
        bookreviews = self.selector.get_BookReview_by_bookid(book_id= book_id)
        serializers = BriefReviewAllSerializer(bookreviews, many=True)
        return serializers.data

    def get_all_bookreviews_by_book(self, book_id: int) -> List:
        bookreviews = self.selector.get_BookReview_by_bookid(book_id= book_id)
        serializers = BookReviewDetailSerializer(bookreviews, many=True)
        return serializers.data

    def get_all_bookreview_by_user(self, user_id: int) -> List:
        bookreviews = self.selector.get_BookReview_by_user_id(user_id=user_id)
        serializers = UserBookReviewSerializer(bookreviews, many=True)
        return serializers.data

    def get_each_bookreview_by_review_id(self, user_id: int, review_id: int) -> "Optional[Dict]":
        bookreview = self.selector.get_BookReview_by_review_id(review_id=review_id)
        entry_user = get_object_or_404(User, id=user_id)
        if (bookreview.disclosure is False) and (bookreview.user == entry_user):
            serializer = EachReviewSerializer(bookreview)
            return serializer.data
        else:
            return None

    def get_aiquestions(self, user_id: int, book_id: int) -> List[str]:
        readingnotes_objs = ReadingNoteSelector.get_all_userreadingnote(user_id=user_id, book_id=book_id)
        readingnotes_list = ReadingNoteContentSerializer(readingnotes_objs, many=True)
        # 각 요소 사이에 '\n'을 넣어 하나의 문자열로 합치기
        combined_text = '\n'.join(readingnotes_list)
        return generate_questions(combined_text)

    def get_recommended_reviews_by_keywords(self, review_id: int) -> Dict[str:List[str], str:List]:
        my_keywords, all_keywords_list = self.selector.get_allBookReviewKeywords_by_review_id(review_id=review_id)
        recommended_keywords = find_similar_keywords(my_keywords, all_keywords_list)

        bookreviews = self.selector.get_reviews_by_keywords(keywords=recommended_keywords)
        serializer = UserBookReviewSerializer(bookreviews, many=True)
        return {"keywords": recommended_keywords, "reviews": serializer.data}
