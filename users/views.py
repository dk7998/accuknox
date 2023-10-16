from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin

from utils.views import SoftDestroyModelMixin

from .models import User

from .serializers import UserSerializer
from .helpers import is_email


class UserViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, SoftDestroyModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.pk)
        else:
            return User.objects.none()


class UserSearchViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            User.objects.annotate_full_name().exclude(Q(pk=self.request.user.pk) | Q(is_active=False)).order_by("full_name")
        )

        search_keyword = self.request.query_params.get("search_keyword")
        if self.action == "list" and search_keyword:
            if is_email(search_keyword):
                queryset = queryset.filter(email__iexact=search_keyword)
            else:
                queryset = queryset.filter(full_name__icontains=search_keyword)

        return queryset
