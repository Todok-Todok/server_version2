from django.db import models
from book.models import Book
from user.models import User

# Create your models here.
class AIQuestion(models.Model):
    aiquestion_id = models.AutoField(primary_key=True)
    aiquestion_list = models.JSONField(default=list)

    class Meta:
        managed = True
        db_table = 'AIQuestion'

class BookReview(models.Model):
    bookreview_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    aiquestion = models.OneToOneField(AIQuestion, on_delete=models.CASCADE, null=True)
    keywords = models.JSONField(default=list)
    brief_review = models.CharField(max_length=100)
    content = models.TextField()
    written_at = models.DateField()
    disclosure = models.BooleanField(default=False) # False : 비공개, True : 공개

    class Meta:
        managed = True
        db_table = 'BookReview'

# class UserBookReview(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
#     bookreview = models.ForeignKey(BookReview, on_delete=models.CASCADE, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'UserBookReview'