"""Constantes de la aplicación"""

# Estados de reserva
RESERVA_ESTADOS = {
    "pendiente": "pendiente",
    "confirmada": "confirmada",
    "cancelada": "cancelada",
    "completada": "completada",
}

# Roles de usuario
USUARIO_ROLES = {
    "admin": "admin",
    "cliente": "cliente",
    "gerente": "gerente",
}

# Límites
LIMITE_PERSONAS_MINIMO = 1
LIMITE_PERSONAS_MAXIMO = 500
LIMITE_DIAS_ANTICIPACION = 365
