from .models import *
from .serializers import *
from .selectors.abstracts import UserSelector
from django.db.models.query import QuerySet
from typing import List, Tuple, Optional, Dict


class UserService:
    def __init__(self, selector: UserSelector):
        self.selector = selector

    def remove_one_history(self, user_id: int, content: str) -> None:
        personaling_info = self.selector.get_personal_info(user_id=user_id)
        info_list = personaling_info.recent_search_history
        if content in info_list:
            info_list.remove(content)
        personaling_info.save()

    def change_password(self, user_id: int, type: int, password: str) -> "Optional[str]":
        user = get_object_or_404(User, id=user_id)
        # type == 0 : 기존 비밀번호 일치 확인
        # type == 1 : 새로운 비밀번호로 변경
        if type == 0:
            if user.password != password:
                return None
        else:
            user.password = password
            user.save()

        return password
