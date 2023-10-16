from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import UserViewSet, UserSearchViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="")
router.register(r"search_users", UserSearchViewSet, basename="")


urlpatterns = [
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
] + router.urls
