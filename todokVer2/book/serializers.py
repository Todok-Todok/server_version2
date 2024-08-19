from .models import Book, UserBook
from rest_framework import serializers, validators

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


class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields = '__all__'