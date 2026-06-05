# tests/unit/test_PE/test_empleado_pe.py

import pytest
from appweb.models import Usuario, UsuarioException
from tests.helpers.empleados_helper import (
    datos_username_validos,
    datos_username_invalidos,
    datos_password_validos,
    datos_password_invalidos,
    datos_roles_validos,
    datos_roles_invalidos,
    datos_verificacion_credenciales,
    datos_consultar_por_id,
    datos_longitud_username,
    datos_patron_username,
    datos_valores_none,
)


# =========================================================
# USERNAME - VALORES VALIDOS
# =========================================================

@pytest.mark.parametrize("username,esperado", datos_username_validos())  # ← CORREGIDO: añadir decorador
def test_username_pe_valido(username, esperado):
    usuario = Usuario(username=username, password="password123", rol="cliente")
    assert usuario.username == esperado


# =========================================================
# USERNAME - VALORES INVALIDOS
# =========================================================

@pytest.mark.parametrize("username,descripcion", datos_username_invalidos())
def test_username_pe_invalidos(username, descripcion):
    with pytest.raises(UsuarioException):
        Usuario(username=username, password="password123", rol="cliente")


# =========================================================
# PASSWORD - VALORES VALIDOS
# =========================================================

@pytest.mark.parametrize("password,esperado", datos_password_validos())
def test_password_pe_valido(password, esperado):
    if esperado is None:
        # Caso vacío se prueba en inválidos
        return
    usuario = Usuario(username="testuser", password=password, rol="cliente")
    assert usuario.password == esperado


# =========================================================
# PASSWORD - VALORES INVALIDOS
# =========================================================

@pytest.mark.parametrize("password,descripcion", datos_password_invalidos())
def test_password_pe_invalidos(password, descripcion):
    with pytest.raises(UsuarioException):
        Usuario(username="testuser", password=password, rol="cliente")


# =========================================================
# ROL - VALORES VALIDOS
# =========================================================

@pytest.mark.parametrize("rol,esperado", datos_roles_validos())
def test_rol_pe_valido(rol, esperado):
    usuario = Usuario(username="testuser", password="password123", rol=rol)
    assert usuario.rol == esperado


# =========================================================
# ROL - VALORES INVALIDOS
# =========================================================

@pytest.mark.parametrize("rol,descripcion", datos_roles_invalidos())
def test_rol_pe_invalidos(rol, descripcion):
    with pytest.raises(UsuarioException):
        Usuario(username="testuser", password="password123", rol=rol)


# =========================================================
# VERIFICAR CREDENCIALES
# =========================================================

@pytest.mark.parametrize("username,password,esperado_existe", datos_verificacion_credenciales())
def test_verificar_credenciales(username, password, esperado_existe):
    resultado = Usuario.verificar_credenciales(username, password)
    if esperado_existe:
        assert resultado is not None
        assert resultado.username == username
    else:
        assert resultado is None


# =========================================================
# CONSULTAR POR ID
# =========================================================

@pytest.mark.parametrize("user_id,esperado_id", datos_consultar_por_id())
def test_consultar_usuario_por_id(user_id, esperado_id):
    resultado = Usuario.consultar_por_id(user_id)
    if esperado_id is None:
        assert resultado is None
    else:
        assert resultado is not None
        assert resultado.id == esperado_id


def test_consultar_usuario_por_id_existente():
    resultado = Usuario.consultar_por_id(1)
    assert resultado is not None
    assert resultado.id == 1


# =========================================================
# LONGITUD DE USERNAME
# =========================================================

@pytest.mark.parametrize("username,es_valido,descripcion", datos_longitud_username())
def test_longitud_username_pe(username, es_valido, descripcion):
    if es_valido:
        usuario = Usuario(username=username, password="password123", rol="cliente")
        assert usuario.username == username
    else:
        with pytest.raises(UsuarioException):
            Usuario(username=username, password="password123", rol="cliente")


# =========================================================
# PATRON DE USERNAME
# =========================================================

@pytest.mark.parametrize("username,es_valido,descripcion", datos_patron_username())
def test_patron_username_pe(username, es_valido, descripcion):
    if es_valido:
        usuario = Usuario(username=username, password="password123", rol="cliente")
        assert usuario.username == username.lower()
    else:
        with pytest.raises(UsuarioException):
            Usuario(username=username, password="password123", rol="cliente")


# =========================================================
# VALORES NONE
# =========================================================

@pytest.mark.parametrize("username,password,rol", datos_valores_none())
def test_valores_none_pe(username, password, rol):
    """Probar comportamiento con valores None según código real"""
    if rol is None:
        # rol=None es válido (tiene valor por defecto)
        usuario = Usuario(username=username, password=password, rol=rol)
        assert usuario.rol == "cliente"
    else:
        with pytest.raises(UsuarioException):
            Usuario(username=username, password=password, rol=rol)