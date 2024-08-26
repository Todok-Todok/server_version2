from .models import *
from rest_framework import serializers
from datetime import date
from user.models import User
from book.models import Book
from django.shortcuts import get_object_or_404

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
        book = get_object_or_404(Book, id=book_id)
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
        max_length=200,
        required=True,
    )
    keywords = serializers.JSONField(
        help_text="독서메모 키워드 리스트",
        allow_null=True,
        required=True,
    )
    sentence_image = serializers.CharField(
        help_text="성별",
        max_length=256,
        allow_blank=True,
        required=False,
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

class ReadingNoteSaveSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        help_text="독서메모 내용",
        max_length=200,
        required=True,
    )
    keywords = serializers.JSONField(
        help_text="독서메모 키워드 리스트",
        allow_null=True,
        required=True,
    )
    sentence_image = serializers.CharField(
        help_text="성별",
        max_length=256,
        allow_blank=True,
        required=False,
    )
    exquestion_id = serializers.IntegerField(
        help_text="데일리 샘플 질문 id",
        allow_null=True,
        required=False,
    )

    def validate_keywords(self, keywords):
        if keywords is None:
            keywords = []
        return keywords

    def save(self, user_id, book_id, requested_data):
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, id=book_id)
        ReadingNote.objects.create(
            user=user,
            book=book,
            exquestion=requested_data["exquestion_id"],
            keywords=requested_data["keywords"],
            sentence_image=requested_data["sentence_image"],
            content=requested_data["content"],
            written_at=date.today()
        )

    class Meta:
        model = ReadingNote