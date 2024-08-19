from django.db import models
from user.models import User


# Create your models here.

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    book_image = models.CharField(max_length=256, blank=True, default="")
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    keywords = models.JSONField()
    entire_pages = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'Book'


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    status = models.IntegerField(default=0)  # 1 : 읽는 중 , 그 외 : 0 (기본값)
    reading_time = models.JSONField()
    reading_pages = models.IntegerField()
    reading_percent = models.IntegerField()
    reading_days = models.JSONField()


    class Meta:
        managed = True
        db_table = 'UserBook'


class BriefReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    brief_review = models.TextField()
    written_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'BriefReview'


class BookDetail(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    intro = models.TextField()
    buying_at = models.JSONField()

    class Meta:
        managed = True
        db_table = 'BookDetail'


class BookSentence(models.Model):
    genre = models.CharField(max_length=100, primary_key=True)
    represent_sentence = models.JSONField()

    class Meta:
        managed = True
        db_table = 'BookSentence'