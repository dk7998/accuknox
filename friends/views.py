from django.db.models import F, Value
from django.db.models.functions import Concat, Trim

from rest_framework.permissions import IsAuthenticated

from utils.views import SoftDestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin

from .serializers import FriendRequestSerializer, FriendRequestActionSerializer, FriendSerializer, FriendReadSerializer
from .models import Friend, FriendRequest, FriendRequestStatus
from .helpers import SendFriendRequestThrottle


class SendFriendRequestView(CreateModelMixin, RetrieveModelMixin, SoftDestroyModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method == "POST":
            return [SendFriendRequestThrottle()]
        else:
            return []

    def get_queryset(self):
        return FriendRequest.objects.filter(from_user=self.request.user, status=FriendRequestStatus.SENT, is_active=True)


class ReceiveRequestView(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = FriendRequestActionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status=FriendRequestStatus.SENT, is_active=True)


class FriendView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FriendReadSerializer
        else:
            return FriendSerializer

    def get_queryset(self):
        queryset = (
            Friend.objects.filter(user=self.request.user, is_active=True)
            .select_related("friend")
            .annotate(full_name=Trim(Concat("friend__first_name", Value(" "), "friend__last_name")))
            .order_by("full_name")
        )

        return queryset
