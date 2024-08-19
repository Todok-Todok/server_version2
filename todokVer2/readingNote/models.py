from django.db import models
from book.models import Book
from user.models import User


# Create your models here.
class AIQuestionFinished(models.Model):
    aiquestion = models.AutoField(primary_key=True)
    keywords = models.JSONField()
    content = models.JSONField()

    class Meta:
        managed = True
        db_table = 'AIQuestionFinished'


class ReadingNote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    aiquestion = models.ForeignKey(AIQuestionFinished, on_delete=models.CASCADE, null=True)
    keywords = models.JSONField()
    sentence = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    written_at = models.DateTimeField()
    release_or_not = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'ReadingNote'


class UserReadingNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    aiquestion = models.ForeignKey(AIQuestionFinished, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        db_table = 'UserReadingNote'


class PreReadingNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    written_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'PreReadingNote'


class ExQuestionOngoing(models.Model):
    exquestion = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=100)
    content = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'ExQuestionOngoing'