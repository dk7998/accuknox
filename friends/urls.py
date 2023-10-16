from rest_framework.routers import DefaultRouter

from .views import SendFriendRequestView, ReceiveRequestView, FriendView

router = DefaultRouter(trailing_slash=False)
router.register(r"send_requests", SendFriendRequestView, basename="")
router.register(r"receive_requests", ReceiveRequestView, basename="")
router.register(r"friends", FriendView, basename="")

urlpatterns = router.urls
