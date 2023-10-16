from typing import List
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


from utils.models import TimeStamp
from .managers import UserManager


class User(AbstractUser, TimeStamp):
    username = None
    confirm_password = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = ["first_name", "last_name"]
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.id}: {self.email}"

    @property
    def name(self):
        return (self.first_name + " " + self.last_name).strip()
