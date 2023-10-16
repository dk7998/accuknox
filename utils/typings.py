from typing import Union, Optional, TYPE_CHECKING
from django.http import HttpRequest
from rest_framework.request import Request

if TYPE_CHECKING:
    from users.models import User

class DummyRequest:
    user: Optional["User"]


REQUEST = Union[HttpRequest, Request, DummyRequest]