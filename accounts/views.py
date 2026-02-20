from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Login: devuelve access y refresh token con email en el payload."""
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    """Vista de registro de usuarios. POST con email, password, password_confirm, username (opcional)."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """ViewSet para ver y actualizar el perfil del usuario autenticado (GET, PUT, PATCH en /profile/)."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
