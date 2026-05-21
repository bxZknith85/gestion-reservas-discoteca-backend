import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        return Response(
            {"detail": "Conflicto: el registro ya existe o viola restricciones de integridad."},
            status=status.HTTP_409_CONFLICT,
        )

    if response is not None:
        return response

    logger.exception("Excepción no manejada: %s", exc)
    return Response(
        {"detail": "Error interno del servidor."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
