import base64
from io import BytesIO

import qrcode
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import (
    CustomTokenObtainPairSerializer,
    MFAVerifySerializer,
    PasswordChangeSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Login endpoint that returns user data with JWT tokens"""

    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(viewsets.ViewSet):
    """User registration endpoint"""

    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """User management endpoints"""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users can only view themselves unless they're admin"""
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=["get"])
    def me(self, request):
        """Get current authenticated user"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def change_password(self, request):
        """Change user password"""
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response(
                    {"old_password": "Incorrect password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"detail": "Password changed successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def setup_mfa(self, request):
        """Setup MFA for user"""
        user = request.user
        device = TOTPDevice.objects.create(user=user, name="default", confirmed=False)

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(device.config_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

        return Response(
            {"secret": device.key, "qr_code": f"data:image/png;base64,{qr_code_base64}"}
        )

    @action(detail=False, methods=["post"])
    def verify_mfa(self, request):
        """Verify and confirm MFA setup"""
        serializer = MFAVerifySerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            device = TOTPDevice.objects.filter(user=user, confirmed=False).first()

            if not device:
                return Response(
                    {"detail": "No pending MFA setup"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if device.verify_token(serializer.validated_data["token"]):
                device.confirmed = True
                device.save()
                user.enable_mfa()
                return Response({"detail": "MFA enabled successfully"})

            return Response(
                {"token": "Invalid verification code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def disable_mfa(self, request):
        """Disable MFA for user"""
        user = request.user
        if not user.mfa_enabled:
            return Response(
                {"detail": "MFA not enabled"}, status=status.HTTP_400_BAD_REQUEST
            )
        user.disable_mfa()
        return Response({"detail": "MFA disabled successfully"})
