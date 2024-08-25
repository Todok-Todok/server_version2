from .models import *
from rest_framework import serializers
from bookReview.selectors.abstracts import *
from user.serializers import UserSimpleSerializer

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
