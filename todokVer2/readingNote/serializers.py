from .models import *
from rest_framework import serializers
from datetime import date
from user.models import User
from book.models import Book
from django.shortcuts import get_object_or_404

class ReadingNoteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingNote
        fields = ('content',)

class SimpleReadingNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingNote
        fields = ('content','written_at',)

class TodaySampleQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExQuestionOngoing
        fields = ('content','exquestion_id',)

class PreReadingNoteSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    def get_nickname(self, obj):
        return obj.user.nickname
    class Meta:
        model = PreReadingNote
        fields = ('content','written_at','disclosure','nickname',)

class PreReadingNoteSaveSerializer(serializers.ModelSerializer):
    def save(self, user_id, book_id, requested_data):
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        PreReadingNote.objects.create(
            user=user,
            book=book,
            content=requested_data["content"],
            disclosure=requested_data["disclosure"],
            written_at=date.today()
        )
    class Meta:
        model = PreReadingNote
        fields = ('content', 'disclosure',)

class ReadingNotePatchSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        help_text="독서메모 내용",
        required=True,
    )
    keywords = serializers.JSONField(
        help_text="독서메모 키워드 리스트",
        allow_null=True,
        required=True,
    )
    disclosure = serializers.BooleanField(
        help_text="공개/비공개 여부",
        required=True,
    )

    def validate_keywords(self, keywords):
        if keywords is None:
            keywords = []
        return keywords

    class Meta:
        model = ReadingNote
        fields = ('content', 'keywords', 'disclosure',)

class ReadingNoteSaveSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        help_text="독서메모 내용",
        required=True,
    )
    keywords = serializers.JSONField(
        help_text="독서메모 키워드 리스트",
        allow_null=True,
        required=True,
    )
    exquestion_id = serializers.IntegerField(
        help_text="데일리 샘플 질문 id",
        allow_null=True,
        required=False,
    )
    disclosure = serializers.BooleanField(
        help_text="독서노트 공개 여부",
        required=True,
    )

    def validate_keywords(self, keywords):
        if keywords is None:
            keywords = []
        return keywords

    def validate_exquestion_id(self, exquestion_id):
        if exquestion_id is None:
            return None
        else:
            ExQuestionOngoing.objects.get(exquestion_id=exquestion_id)

    def save(self, user_id, book_id, requested_data):
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        ReadingNote.objects.create(
            user=user,
            book=book,
            disclosure=requested_data["disclosure"],
            exquestion=self.validated_data["exquestion_id"],
            keywords=self.validated_data["keywords"],
            content=requested_data["content"],
            written_at=date.today()
        )

    class Meta:
        model = ReadingNote
        fields = ('disclosure','content','keywords','exquestion_id',)


class ReadingNoteListSerializer(serializers.ModelSerializer):
    sample_question = serializers.SerializerMethodField()

    def get_sample_question(self, obj):
        if obj.exquestion is None:
            return None
        return obj.exquestion.content

    class Meta:
        model = ReadingNote
        fields = ('id', 'sample_question','content', 'keywords', 'written_at', 'disclosure',)

class ExtendedReadingNoteListSerializer(ReadingNoteListSerializer):
    nickname = serializers.SerializerMethodField()

    def get_nickname(self, obj):
        return obj.user.nickname

    class Meta(ReadingNoteListSerializer.Meta):  # 기존 Meta 클래스 상속
        fields = ReadingNoteListSerializer.Meta.fields + ('nickname',)  # 새로운 필드를 추가하여 fields 수정