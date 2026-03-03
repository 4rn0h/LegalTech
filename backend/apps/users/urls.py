from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomTokenObtainPairView, UserRegisterView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

app_name = "users"

urlpatterns = [
    # JWT Token endpoints
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User endpoints
    path("", include(router.urls)),
    # Registration
    path("register/", UserRegisterView.as_view({"post": "register"}), name="register"),
]
