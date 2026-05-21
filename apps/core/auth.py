from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.core.models import User
from apps.core.serializers import LoginResponseSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"detail": "Email y contraseña son obligatorios."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"detail": "Credenciales inválidas."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.check_password(password):
        return Response(
            {"detail": "Credenciales inválidas."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        return Response(
            {"detail": "Usuario desactivado."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)
    serializer = LoginResponseSerializer({
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "user_id": user.id,
        "email": user.email,
        "username": user.username,
    })
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def token_refresh_view(request):
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response(
            {"detail": "El token de refresco es obligatorio."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return Response({"access_token": access_token})
    except TokenError:
        return Response(
            {"detail": "Token de refresco inválido o expirado."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def token_verify_view(request):
    token = request.data.get("token")

    if not token:
        return Response(
            {"detail": "El token es obligatorio."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        RefreshToken(token).access_token
        return Response({"valid": True})
    except TokenError:
        return Response({"valid": False}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if not old_password or not new_password:
        return Response(
            {"detail": "Contraseña actual y nueva son obligatorias."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(new_password) < 8:
        return Response(
            {"detail": "La nueva contraseña debe tener al menos 8 caracteres."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not user.check_password(old_password):
        return Response(
            {"detail": "La contraseña actual es incorrecta."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(new_password)
    user.save()

    return Response({"detail": "Contraseña actualizada correctamente."})
