from django.db import models
from book.models import Book
from user.models import User

class ExQuestionOngoing(models.Model):
    exquestion_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=100)
    content = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'ExQuestionOngoing'


# Create your models here.
class ReadingNote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    exquestion = models.ForeignKey(ExQuestionOngoing, on_delete=models.CASCADE, null=True)
    keywords = models.JSONField(default=list)
    content = models.TextField()
    written_at = models.DateField()
    disclosure = models.BooleanField(default=False)  # False : 비공개, True : 공개

    class Meta:
        managed = True
        db_table = 'ReadingNote'


# class UserReadingNote(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
#     aiquestion = models.ForeignKey(AIQuestionFinished, on_delete=models.CASCADE, null=True)
#     exquestion = models.ForeignKey(ExQuestionOngoing, on_delete=models.CASCADE, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'UserReadingNote'


class PreReadingNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=200)
    written_at = models.DateField()
    disclosure = models.BooleanField(default=False)  # False : 비공개, True : 공개

    class Meta:
        managed = True
        db_table = 'PreReadingNote'