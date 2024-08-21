from .models import User, PersonalizingInfo
from rest_framework import serializers, validators
from django.shortcuts import get_object_or_404

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that Email already exists"
                    )
                ]
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.nickname = validated_data['nickname']
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar_url', 'nickname',)


class UserNicknameSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if self.instance is not None:
            return super().validate(attrs)

        if User.objects.filter(title=attrs['nickname']).exists():
            raise serializers.ValidationError("Duplicated nickname.")

        return super().validate(attrs)

    class Meta:
        model = User
        fields = ('nickname',)


class OnboardingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalizingInfo
        fields = '__all__'

    def save(self, requested_data):
        user = get_object_or_404(User, id=requested_data["user_id"])
        PersonalizingInfo.objects.create(
            user=user,
            # Todo sex,genre가 null값일 때 handling
            sex=requested_data['sex'],
            fav_genre_keywords=requested_data['genre']
        )