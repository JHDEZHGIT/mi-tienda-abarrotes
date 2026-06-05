# tests/helpers/empleados_helper.py
"""
Helpers para pruebas unitarias de empleados (PE y VL)
Basado en el código REAL de models.py
"""

import pytest
from appweb.models import Usuario, UsuarioException


# =========================================================
# USERNAME - VALORES VALIDOS (según código real)
# =========================================================

def datos_username_validos():
    """
    Usernames válidos según código real:
    - Convierte automáticamente números/booleanos a string
    - Acepta mayúsculas (las convierte a minúsculas)
    - Acepta guión bajo
    """
    return [
        ("admin", "admin"),
        ("usuario1", "usuario1"),
        ("user_name", "user_name"),
        ("user123", "user123"),
        ("a" * 100, "a" * 100),  # máximo 100 caracteres
        (123, "123"),              # número se convierte a string
        (True, "true"),            # booleano se convierte a string
    ]


def datos_username_invalidos():
    """
    Usernames inválidos según código real:
    - None (no puede ser nulo)
    - vacío o solo espacios
    - excede 100 caracteres
    - contiene caracteres no permitidos (espacios, puntos, guiones, @, etc.)
    """
    return [
        (None, "nulo"),
        ("", "vacío"),
        ("   ", "solo espacios"),
        ("a" * 101, "excede 100 caracteres"),
        ("usuario nombre", "contiene espacio"),
        ("usuario.nombre", "contiene punto"),
        ("usuario-nombre", "contiene guión"),
        ("usuario@nombre", "contiene @"),
    ]


# =========================================================
# PASSWORD - VALORES VALIDOS (según código real)
# =========================================================

def datos_password_validos():
    """
    Contraseñas válidas según código real:
    - Cualquier string no vacío es válido
    - No hay validación de longitud en el constructor
    """
    return [
        ("password123", "password123"),
        ("123", "123"),           # corta es válida
        ("a" * 100, "a" * 100),   # larga es válida
        ("", None),               # vacío NO es válido (se prueba en inválidos)
    ]


def datos_password_invalidos():
    """
    Contraseñas inválidas según código real:
    - None
    - vacío o solo espacios
    """
    return [
        (None, "nula"),
        ("", "vacía"),
        ("   ", "solo espacios"),
    ]


# =========================================================
# ROL - VALORES VALIDOS (según código real)
# =========================================================

def datos_roles_validos():
    """Roles válidos según código real"""
    return [
        ("admin", "admin"),
        ("cliente", "cliente"),
        (None, "cliente"),  # None se convierte a "cliente"
    ]


def datos_roles_invalidos():
    """
    Roles inválidos según código real:
    - Strings vacíos
    - Valores no permitidos (diferente de admin/cliente)
    """
    return [
        ("", "vacío"),
        ("   ", "solo espacios"),
        ("vendedor", "rol no válido"),
        ("ADMIN", "mayúsculas (no coincide exactamente)"),
        ("CLIENTE", "mayúsculas (no coincide exactamente)"),
        (123, "número (no es string)"),
    ]


# =========================================================
# VERIFICAR CREDENCIALES (según código real)
# =========================================================

def datos_verificacion_credenciales():
    """Datos para verificación de credenciales"""
    return [
        ("admin", "admin", True),      # credenciales correctas
        ("admin", "wrong", False),     # contraseña incorrecta
        ("no_existe", "pass", False),  # usuario no existe
        ("", "password", False),       # username vacío
        ("admin", "", False),          # password vacío
        (None, "password", False),     # username nulo
        ("admin", None, False),        # password nulo
    ]


# =========================================================
# CONSULTAR POR ID (según código real)
# =========================================================

def datos_consultar_por_id():
    """
    Datos para consultar por ID según código real:
    - El método convierte a int si puede
    - Si no puede convertir, retorna None
    """
    return [
        (-999, None),      # ID negativo no existe
        (999999, None),    # ID inexistente
        ("no_numero", None),  # string no numérico
        (True, 1),          # True se convierte a 1, puede existir
    ]


def test_consultar_usuario_por_id_existente():
    """Verificar que el usuario admin (ID=1) existe"""
    resultado = Usuario.consultar_por_id(1)
    assert resultado is not None
    assert resultado.id == 1


# =========================================================
# LONGITUD DE USERNAME (según código real)
# =========================================================

def datos_longitud_username():
    """Pruebas de longitud - según validación real (máximo 100)"""
    return [
        ("a", True, "mínimo 1 carácter - válido"),
        ("a" * 100, True, "máximo 100 - válido"),
        ("a" * 101, False, "101 caracteres - inválido"),
        ("", False, "vacío - inválido"),
        (None, False, "nulo - inválido"),
    ]


# =========================================================
# PATRON DE USERNAME (según código real)
# =========================================================

def datos_patron_username():
    """
    Pruebas de patrón - según regex real:
    ^[A-Za-z0-9_]+$
    Permite: letras (mayúsculas y minúsculas), números, guión bajo
    """
    return [
        ("testuser", True, "solo letras minúsculas"),
        ("TestUser", True, "letras mayúsculas y minúsculas"),
        ("TESTUSER", True, "solo mayúsculas"),
        ("test_user", True, "letras con guión bajo"),
        ("test_123", True, "números con guión bajo"),
        ("testuser123", True, "letras y números"),
        ("test-user", False, "contiene guión medio"),
        ("test.user", False, "contiene punto"),
        ("test user", False, "contiene espacio"),
        ("test@user", False, "contiene @"),
    ]


# =========================================================
# VALORES NONE (según código real)
# =========================================================

def datos_valores_none():
    """
    Pruebas de valores None - según comportamiento real:
    - username None → inválido
    - password None → inválido
    - rol None → válido (asigna "cliente")
    """
    return [
        (None, "password123", "cliente"),   # username None → inválido
        ("testuser", None, "cliente"),      # password None → inválido
        (None, None, "cliente"),            # ambos None → inválido
        ("testuser", "password123", None),  # rol None → VÁLIDO (no debe fallar)
    ]