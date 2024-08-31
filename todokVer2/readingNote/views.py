from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import *
from .models import *
from book.services import BookService
from book.selectors.abstracts import BookSelector
from .services import ReadingNoteService
from .selectors.abstracts import ReadingNoteSelector
from collections import ChainMap
from rest_framework import filters

# Create your views here.
class PreReadingNoteListAPIView(APIView):
    def get(self, request, book_id):
        book_detail_dict = BookService(BookSelector).get_userbook_detail(book_id=book_id)
        prereading_note_list = ReadingNoteService(ReadingNoteSelector).get_prereading_note_with_bookdetail(book_id=book_id)
        return Response({"book_detail": book_detail_dict, "pre-reading_note": prereading_note_list}, status=status.HTTP_200_OK)

class ReadingNoteCRUDAPIView(APIView):
    def get(self, request, user_id, book_id):
        sample_question = ReadingNoteService(ReadingNoteSelector).get_today_sample_question(book_id=book_id)
        book = ReadingNoteService(ReadingNoteSelector).get_simple_book_info_in_ingbook(book_id=book_id)
        reading_note = ReadingNoteService(ReadingNoteSelector).get_all_readingnote_in_ingbook(user_id=user_id, book_id=book_id)

        result = ChainMap(sample_question, book, reading_note)
        return Response(dict(result), status=status.HTTP_200_OK)

    def post(self, request, user_id, book_id):
        serializer = ReadingNoteSaveSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id, book_id, request.data)
            return Response(status=status.HTTP_200_OK)
    def patch(self, request, user_id, book_id):
        readingnote_obj = ReadingNoteService(ReadingNoteSelector).patch_readingnote(user_id=user_id,book_id=book_id)
        serializer = ReadingNotePatchSerializer(readingnote_obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_200_OK)

    def delete(self, request, user_id, book_id):
        ReadingNoteService(ReadingNoteSelector).delete_readingnote(note_id=request.data["id"])
        return Response(status=status.HTTP_204_NO_CONTENT)

class TodayReadingNoteAPIView(APIView):
    def get(self, request, user_id, book_id):
        readingnote_list = ReadingNoteService(ReadingNoteSelector).get_today_readingnote_list(user_id=user_id,book_id=book_id)
        return Response({"result":readingnote_list}, status=status.HTTP_200_OK)

class TodaySampleQuestionAPIView(APIView):
    def get(self, request, book_id):
        todayquestion_dict = ReadingNoteService(ReadingNoteSelector).get_today_sample_question(book_id=book_id)
        return Response(todayquestion_dict, status=status.HTTP_200_OK)

class PreReadingNoteAPIView(APIView):
    def get(self, request, user_id, book_id):
        prereadingnote_dict = ReadingNoteService(ReadingNoteSelector).get_prereadingnote(user_id=user_id,book_id=book_id)
        return Response(prereadingnote_dict, status=status.HTTP_200_OK)

    def post(self, request, user_id, book_id):
        serializer = PreReadingNoteSaveSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id, book_id, request.data)
            return Response(status=status.HTTP_200_OK)

class EachReadingNoteAPIView(APIView):
    def get(self, request, readingnote_id):
        readingnote_detail = ReadingNoteService(ReadingNoteSelector).get_one_readingnote_in_detail(readingnote_id=readingnote_id)
        return Response(readingnote_detail, status=status.HTTP_200_OK)

class OngoingReadingNoteAPIView(ListAPIView):
    queryset = ReadingNote.objects.all()
    serializer_class = ExtendedReadingNoteListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['keywords__icontains']
    def list(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')

        book_detail_dict = BookService(BookSelector).get_userbook_detail(book_id=book_id)

        readingnotes = ReadingNoteSelector.get_readingontes_by_book_id(book_id=book_id)
        reading_note_list = self.filter_queryset(readingnotes)  # 검색 필터 적용
        serializer = self.get_serializer(reading_note_list, many=True)
        return Response({"book_detail": book_detail_dict, "reading_note":serializer.data}, status=status.HTTP_200_OK)