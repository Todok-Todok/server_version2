from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from user.models import User, PersonalizingInfo
from typing import Dict, Optional, List

class AbstractUserSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_personal_info(user_id:int) -> PersonalizingInfo:
        pass

    @abstractmethod
    def get_user_userid(user_id: int) -> User:
        pass

class UserSelector(AbstractUserSelector):
    def get_personal_info(user_id: int) -> PersonalizingInfo:
        user = get_object_or_404(User, id=user_id)
        personaling_info = PersonalizingInfo.objects.get(user=user)
        return personaling_info

    def get_user_userid(user_id: int) -> User:
        return get_object_or_404(User, id=user_id)

    def whether_personal_info_exists(user: User) -> bool:
        return PersonalizingInfo.objects.filter(user=user).exists()