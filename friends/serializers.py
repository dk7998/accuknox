from typing import Dict

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.serializers import ValidationError, ALL_FIELDS

from users.models import User
from utils.serializers import DKModelSerializer
from users.serializers import UserSerializer
from .models import Friend, FriendRequest, FriendRequestStatus


class FriendSerializer(DKModelSerializer):
    class Meta:
        model = Friend
        fields = ALL_FIELDS


class FriendReadSerializer(FriendSerializer):
    friend = UserSerializer()


class FriendRequestSerializer(DKModelSerializer):
    instance: FriendRequest
    from_user = serializers.HiddenField(default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))
    status = serializers.HiddenField(default=serializers.CreateOnlyDefault(FriendRequestStatus.SENT))

    class Meta:
        model = FriendRequest
        fields = ALL_FIELDS

    def validate_to_user(self, to_user: User):
        if not to_user.is_active:
            raise ValidationError(_("This user is no longer active!"))

        already_friends_user_q = Q(user=self._request.user) & Q(friend=to_user) & Q(is_active=True)
        if Friend.objects.filter(already_friends_user_q).exists():
            raise ValidationError(_("You are already friends with this user!"))

        request_already_sent_q = (
            Q(from_user=self._request.user) & Q(to_user=to_user) & Q(status=FriendRequestStatus.SENT) & Q(is_active=True)
        )
        if FriendRequest.objects.filter(request_already_sent_q).exists():
            raise ValidationError(_("Request has already been sent to this user!"))

        request_received_q = (
            Q(to_user=self._request.user) & Q(from_user=to_user) & Q(status=FriendRequestStatus.SENT) & Q(is_active=True)
        )
        if FriendRequest.objects.filter(request_received_q).exists():
            raise ValidationError(_("This user has already sent you a request, please accept it!"))

        if self._request.user == to_user:
            raise ValidationError(_("You can't send request to yourself!"))

        return to_user


class FriendRequestActionSerializer(DKModelSerializer):
    instance: FriendRequest

    class Meta:
        model = FriendRequest
        fields = ALL_FIELDS
        read_only_fields = ["from_user", "to_user", "is_active"]

    def validate_status(self, status: int):
        if self.instance.status != FriendRequestStatus.SENT:
            raise ValidationError(_("Friend request has already been processed!"))

        if status == FriendRequestStatus.SENT:
            raise ValidationError(_("Invalid friend request action!"))

        return status

    def update(self, instance, validated_data):
        instance: FriendRequest = super().update(instance, validated_data)
        if instance.status == FriendRequestStatus.ACCEPTED:
            data = [
                {
                    "user": instance.from_user.pk,
                    "friend": instance.to_user.pk,
                },
                {
                    "user": instance.to_user.pk,
                    "friend": instance.from_user.pk,
                },
            ]

            serializer = FriendSerializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return instance
