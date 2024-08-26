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
    keywords = models.JSONField(default=list)
    entire_pages = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'Book'


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    status = models.IntegerField(default=1)  # 1 : 읽는 중 , 그 외 : 0 (기본값)
    reading_pages = models.IntegerField(default=0)
    reading_percent = models.IntegerField(default=0)
    reading_days = models.JSONField(default=list)
    saved_at = models.DateField()

    class Meta:
        managed = True
        db_table = 'UserBook'


class BookDetail(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, null=True)
    intro = models.TextField()
    buying_at = models.JSONField(default=dict)

    class Meta:
        managed = True
        db_table = 'BookDetail'


class BookSentence(models.Model):
    genre = models.CharField(max_length=100)
    represent_sentence = models.JSONField(default=list)     # [{"책 제목" : "문장"},...]

    class Meta:
        managed = True
        db_table = 'BookSentence'