from .models import Book, UserBook, BookSentence, BookDetail
from bookReview.models import BookReview
from rest_framework import serializers, validators
from readingNote.selectors.abstracts import ReadingNoteSelector
from bookReview.serializers import BriefReviewSerializer

class BookDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        bookreview_obj = BookReview.objects.filter(book=instance.book).order_by('?').first()
        response['book_detail'] = BookSerializer(instance.book).data
        response['brief_review'] = BriefReviewSerializer(bookreview_obj).data
        return response
    class Meta:
        model = BookDetail
        fields = ('intro','buying_at',)

class BookSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSentence
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, attrs):
        if self.instance is not None:
            return super().validate(attrs)

        if Book.objects.filter(title=attrs['title']).exists():
            raise serializers.ValidationError("Duplicated title.")

        return super().validate(attrs)

class IngBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title','author','book_image','entire_pages',)


class IngUserBookSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['book'] = IngBookSerializer(instance.book).data
        return response
    class Meta:
        model = UserBook
        fields = ('reading_pages','reading_days',)


class RecommendBookSerializer(serializers.ModelSerializer):
    book_memo = serializers.SerializerMethodField()
    def __init__(self, selector: ReadingNoteSelector):
        self.selector = selector
    def get_book_memo(self, obj):
        readingnote_obj = self.selector.get_one_note_by_book(obj)
        return readingnote_obj.content
    class Meta:
        model = Book
        fields = ('title','author','keywords','book_image','book_memo',)