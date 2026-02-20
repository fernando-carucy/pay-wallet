from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializador para registro de usuarios con email, password y username (nombre)."""

    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        label="Confirmar contraseña",
    )
    username = serializers.CharField(required=False, allow_blank=True, max_length=150)

    class Meta:
        model = User
        fields = ("email", "password", "password_confirm", "username")

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este email.")
        return value.lower()

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "Las contraseñas no coinciden."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        username = validated_data.pop("username", None) or ""
        password = validated_data.pop("password")
        user = User.objects.create_user(
            **validated_data,
            password=password,
            first_name=username.strip() or validated_data.get("email", "").split("@")[0],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializador para perfil de usuario (lectura y actualización)."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
            "is_verified",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("id", "email", "is_verified", "date_joined", "last_login")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Incluye el email en el payload del token JWT."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token
