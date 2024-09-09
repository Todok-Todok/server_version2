from .models import User, PersonalizingInfo
from rest_framework import serializers, validators
from django.shortcuts import get_object_or_404
from .selectors.abstracts import UserSelector

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
    user_id = serializers.IntegerField(
        help_text="유저 아이디",
        required=True,
    )
    sex = serializers.CharField(
        help_text="성별",
        max_length=3,
        allow_blank=True,
        required=False,
    )
    genre = serializers.JSONField(
        help_text="관심있는 장르",
        allow_null=True,
        required=False,
    )

    def validate_genre(self, genre):
        if genre is None:
            genre = []
        return genre

    def save(self, requested_data):
        user = get_object_or_404(User, id=requested_data["user_id"])
        PersonalizingInfo.objects.create(
            user=user,
            sex=requested_data["sex"],
            fav_genre_keywords=self.validated_data["genre"]
        )

    class Meta:
        model = PersonalizingInfo
        fields = ('user_id','genre','sex',)

class UserProfileSerializer(serializers.ModelSerializer):
    sex = serializers.SerializerMethodField()

    def get_sex(self, obj):
        personalizinguser_obj = UserSelector.get_personal_info(obj.id)
        return personalizinguser_obj.sex

    def save(self, *args, **kwargs):
        # 1. 기본 저장 로직 실행
        instance = super().save(*args, **kwargs)
        instance.save()
        # 2. 추가 로직 실행 (저장 후 수행할 작업)
        personalizing = PersonalizingInfo.objects.get(user=self._args[0])
        personalizing.sex = self._kwargs['data']['sex']
        personalizing.save()

    class Meta:
        model = User
        fields = ('sex','avatar_url','nickname',"email",)