from django.db import models
from book.models import Book
from user.models import User

# Create your models here.
class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    keywords = models.JSONField(default=list)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    written_at = models.DateField()
    release_or_not = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'BookReview'


class UserBookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        db_table = 'UserBookReview'