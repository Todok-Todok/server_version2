from .models import *
from rest_framework import serializers
from bookReview.selectors.abstracts import *
from user.serializers import UserSimpleSerializer
from datetime import date
from user.models import User
from book.models import Book
from django.shortcuts import get_object_or_404

class BriefReviewSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSimpleSerializer(instance.user).data
        return response
    class Meta:
        model = BookReview
        fields = ('brief_review','written_at',)


class BriefReviewAllSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.update(BriefReviewSerializer(instance).data)
        return response
    class Meta:
        model = BookReview
        fields = ('bookreview_id',)

class BookReviewDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    def get_nickname(self, obj):
        return obj.user.nickname
    class Meta:
        model = BookReview
        fields = ('brief_review','content','written_at','disclosure','nickname',)

class BookReviewSaveSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        help_text="서평 내용",
        max_length=200,
        required=True,
    )
    keywords = serializers.JSONField(
        help_text="서평 AI 요약 키워드 리스트",
        allow_null=True,
        required=False,
    )
    brief_review = serializers.CharField(
        help_text="서평 한줄소감",
        max_length=100,
        required=True,
    )
    disclosure = serializers.BooleanField(
        help_text="공개/비공개 여부",
        required=True,
    )
    aiquestion_list = serializers.JSONField(
        help_text="AI 생성 질문 리스트",
        allow_null=True,
        required=False,
    )
    def validate_keywords(self, keywords):
        if keywords is None:
            keywords = []
        return keywords

    def validate_aiquestion_list(self, aiquestion_list):
        if aiquestion_list is None:
            aiquestion_list = []
        return aiquestion_list

    def save(self, user_id, book_id, requested_data):
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        aiquestion = AIQuestion.objects.create(
            aiquestion_list=requested_data["aiquestion_list"]
        )
        BookReview.objects.create(
            user=user,
            book=book,
            aiquestion=aiquestion,
            keywords=requested_data["keywords"],
            sentence_image=requested_data["sentence_image"],
            content=requested_data["content"],
            written_at=date.today(),
            disclosure=requested_data["disclosure"]
        )

    book_image = serializers.SerializerMethodField()

    def get_book_image(self, obj):
        return obj.book.book_image
    class Meta:
        model = BookReview
        fields = ('brief_review','written_at','book_image',)

class UserBookReviewSerializer(serializers.ModelSerializer):
    book_image = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    def get_book_image(self, obj):
        return obj.book.book_image

    def get_author(self, obj):
        return obj.book.author

    class Meta:
        model = BookReview
        fields = ('bookreview_id','brief_review','written_at','book_image','author',)


class EachReviewSerializer(serializers.ModelSerializer):
    aiquestion_list = serializers.SerializerMethodField()
    def get_aiquestion_list(self, obj):
        return obj.aiquestion.aiquestion_list

    class Meta:
        model = BookReview
        fields = ('aiquestion_list','brief_review','keywords','content','disclosure',)