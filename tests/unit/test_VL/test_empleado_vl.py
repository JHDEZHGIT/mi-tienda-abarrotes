# tests/unit/test_VL/test_empleado_vl.py

import pytest

from appweb.empleados import (
    Empleado,
    NombreEmpleadoException,
    EmailEmpleadoException,
    UsernameEmpleadoException,
    PasswordEmpleadoException
)

from tests.helpers.fechas_helper import fecha_hace_30_anios


# =========================================================
# VALORES LIMITE - NOMBRE
# =========================================================

@pytest.mark.parametrize("nombre,valido,longitud_esperada", [
    ("a", True, 1),
    ("a" * 100, True, 100),
    ("a" * 101, False, None),
])
def test_nombre_valores_limite(nombre, valido, longitud_esperada):
    kwargs = {
        "nombre": nombre,
        "apellido_paterno": "Perez",
        "apellido_materno": "Gomez",
        "email": "test@example.com",
        "fecha_contratacion": fecha_hace_30_anios(),
        "username": "testuser",
        "password": "vendedor123",
        "rol": "vendedor"
    }
    if valido:
        empleado = Empleado(**kwargs)
        assert len(empleado.nombre) == longitud_esperada
    else:
        with pytest.raises(NombreEmpleadoException):
            Empleado(**kwargs)


# =========================================================
# VALORES LIMITE - APELLIDO PATERNO
# =========================================================

@pytest.mark.parametrize("apellido,valido,longitud_esperada", [
    ("a", True, 1),
    ("a" * 100, True, 100),
    ("a" * 101, False, None),
])
def test_apellido_paterno_valores_limite(apellido, valido, longitud_esperada):
    kwargs = {
        "nombre": "Juan",
        "apellido_paterno": apellido,
        "apellido_materno": "Gomez",
        "email": "test@example.com",
        "fecha_contratacion": fecha_hace_30_anios(),
        "username": "testuser",
        "password": "vendedor123",
        "rol": "vendedor"
    }
    if valido:
        empleado = Empleado(**kwargs)
        assert len(empleado.apellido_paterno) == longitud_esperada
    else:
        with pytest.raises(NombreEmpleadoException):
            Empleado(**kwargs)


# =========================================================
# VALORES LIMITE - APELLIDO MATERNO
# =========================================================

@pytest.mark.parametrize("apellido,valido,longitud_esperada", [
    ("a", True, 1),
    ("a" * 100, True, 100),
    ("a" * 101, False, None),
])
def test_apellido_materno_valores_limite(apellido, valido, longitud_esperada):
    kwargs = {
        "nombre": "Juan",
        "apellido_paterno": "Perez",
        "apellido_materno": apellido,
        "email": "test@example.com",
        "fecha_contratacion": fecha_hace_30_anios(),
        "username": "testuser",
        "password": "vendedor123",
        "rol": "vendedor"
    }
    if valido:
        empleado = Empleado(**kwargs)
        assert len(empleado.apellido_materno) == longitud_esperada
    else:
        with pytest.raises(NombreEmpleadoException):
            Empleado(**kwargs)


# =========================================================
# VALORES LIMITE - EMAIL (longitud)
# =========================================================

@pytest.mark.parametrize("email,valido", [
    ("a@b.cd", True),                    # mínimo válido
    ("usuario@example.com", True),       # email estándar
    ("a" * 138 + "@example.com", True),  # 150 caracteres exactos (138 + 12)
])
def test_email_valores_limite_validos(email, valido):
    kwargs = {
        "nombre": "Juan",
        "apellido_paterno": "Perez",
        "apellido_materno": "Gomez",
        "email": email,
        "fecha_contratacion": fecha_hace_30_anios(),
        "username": "testuser",
        "password": "vendedor123",
        "rol": "vendedor"
    }
    empleado = Empleado(**kwargs)
    assert empleado.email == email.lower()


def test_email_valores_limite_excedido():
    """Email que excede 150 caracteres debe ser rechazado"""
    # 139 + 12 = 151 caracteres
    email_excedido = "a" * 139 + "@example.com"
    
    with pytest.raises(EmailEmpleadoException):
        Empleado(
            nombre="Juan",
            apellido_paterno="Perez",
            apellido_materno="Gomez",
            email=email_excedido,
            fecha_contratacion=fecha_hace_30_anios(),
            username="testuser",
            password="vendedor123",
            rol="vendedor"
        )


# =========================================================
# VALORES LIMITE - USERNAME (longitud)
# =========================================================

@pytest.mark.parametrize("username,valido,longitud_esperada", [
    ("a", True, 1),
    ("a" * 50, True, 50),
    ("a" * 51, False, None),
])
def test_username_valores_limite_longitud(username, valido, longitud_esperada):
    kwargs = {
        "nombre": "Juan",
        "apellido_paterno": "Perez",
        "apellido_materno": "Gomez",
        "email": "test@example.com",
        "fecha_contratacion": fecha_hace_30_anios(),
        "username": username,
        "password": "vendedor123",
        "rol": "vendedor"
    }
    if valido:
        empleado = Empleado(**kwargs)
        assert len(empleado.username) == longitud_esperada
    else:
        with pytest.raises(UsernameEmpleadoException):
            Empleado(**kwargs)


# =========================================================
# VALORES LIMITE - USERNAME (caracteres)
# =========================================================

@pytest.mark.parametrize("username,valido", [
    ("testuser", True),      # minúsculas - válido
    ("test_user", True),     # con guión bajo - válido
    ("test123", True),       # con números - válido
    ("TESTUSER", True),      # mayúsculas - se convierten a minúsculas
    ("test-user", False),    # guión - inválido
    ("test.user", False),    # punto - inválido
    ("test user", False),    # espacio - inválido
])
def test_username_valores_limite_caracteres(username, valido):
    kwargs = {
        "nombre": "Juan",
        "apellido_paterno": "Perez",
        "apellido_materno": "Gomez",
        "email": "test@example.com",
        "fecha_contratacion": fecha_hace_30_anios(),
        "username": username,
        "password": "vendedor123",
        "rol": "vendedor"
    }
    if valido:
        empleado = Empleado(**kwargs)
        assert empleado.username is not None
    else:
        with pytest.raises(UsernameEmpleadoException):
            Empleado(**kwargs)


# =========================================================
# VALORES LIMITE - PASSWORD
# =========================================================

@pytest.mark.parametrize("password,valido,longitud", [
    ("12345", False, 5),      # 5 - inválido
    ("123456", True, 6),      # 6 - límite inferior
    ("1234567", True, 7),     # 7 - justo arriba
    ("a" * 29, True, 29),     # 29 - justo debajo
    ("a" * 30, True, 30),     # 30 - límite superior
    ("a" * 31, False, 31),    # 31 - inválido
])
def test_password_valores_limite_longitud(password, valido, longitud):
    kwargs = {
        "nombre": "Juan",
        "apellido_paterno": "Perez",
        "apellido_materno": "Gomez",
        "email": "test@example.com",
        "fecha_contratacion": fecha_hace_30_anios(),
        "username": "testuser",
        "password": password,
        "rol": "vendedor"
    }
    if valido:
        empleado = Empleado(**kwargs)
        assert empleado.password is not None
    else:
        with pytest.raises(PasswordEmpleadoException):
            Empleado(**kwargs)