from .serializers import *
from .selectors.abstracts import ReadingNoteSelector
from book.selectors.abstracts import BookSelector
from typing import List, Dict


class ReadingNoteService:
    def __init__(self, selector: ReadingNoteSelector):
        self.selector = selector

    def get_prereading_note_with_bookdetail(self, user_id: int, book_id: int) -> List:
        prereading_objs = self.selector.get_prereadingnotes_by_bookid(book_id=book_id)
        serializer = PreReadingNoteSerializer(prereading_objs)
        return serializer.data

    def patch_readingnote(self, user_id: int, book_id: int) -> ReadingNote:
        readingnote_obj = self.selector.get_readingnote_by_userbook(user_id=user_id,book_id=book_id)
        return readingnote_obj

    def delete_readingnote(self, note_id: int) -> None:
        readingnote_obj = self.selector.get_readingnote_by_id(note_id=note_id)
        readingnote_obj.delete()

    def get_today_readingnote_list(self, user_id: int, book_id: int) -> List:
        readingnote_objs = self.selector.get_today_readingnote(user_id=user_id,book_id=book_id)
        serializer = SimpleReadingNoteSerializer(readingnote_objs)
        return serializer.data

    def get_today_sample_question(self, book_id: int) -> Dict:
        book_obj = BookSelector.get_book_by_bookid(book_id=book_id)
        exquestion_obj = self.selector.get_todayquestion(genre=book_obj.genre)
        serializer = TodaySampleQuestionSerializer(exquestion_obj)
        return serializer.data

    def get_prereadingnote(self, user_id: int, book_id: int) -> Dict:
        prereadingnote_obj = self.selector.get_prereadingnote_by_userbook(user_id=user_id,book_id=book_id)
        serializer = PreReadingNoteSaveSerializer(prereadingnote_obj)
        return serializer.data