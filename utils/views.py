from django.db.models import Model
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin



RU_METHODS = ["patch", "get"]


class DKModelViewSet(ModelViewSet):
    def perform_destroy(self, instance: Model):
        instance.is_active = False
        instance.save(update_fields=["is_active"])


class SoftDestroyModelMixin(DestroyModelMixin):
    def perform_destroy(self, instance: Model):
        instance.is_active = False
        instance.save(update_fields=["is_active"])


CRUD_MIXINS = (CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, SoftDestroyModelMixin, ListModelMixin, GenericViewSet)
CRD_MIXINS = (CreateModelMixin, RetrieveModelMixin, SoftDestroyModelMixin, ListModelMixin, GenericViewSet)
RU_MIXINS = (RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet)
R_MIXINS = (RetrieveModelMixin, ListModelMixin, GenericViewSet)
