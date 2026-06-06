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

from appweb.empleados import (
    Empleado,
    NombreEmpleadoException,
    EmailEmpleadoException,
    TelefonoEmpleadoException,
    UsernameEmpleadoException,
    PasswordEmpleadoException,
    AltaEmpleadoException
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


# PRUEBA 1: CREAR EMPLEADO CON NOMBRE NONE
# CUBRE: Líneas 85-86 de empleados.py (validación tipo None)
# =========================================================
def test_crear_empleado_nombre_none():
    """
    Verifica que pasar None como nombre
    active la excepción NombreEmpleadoException.
    """
    with pytest.raises(NombreEmpleadoException, match="no puede estar vacío"):
        Empleado(
            nombre=None,
            apellido_paterno="Lopez",
            email="test@example.com",
            username="testuser"
        )

# PRUEBA 2: CREAR EMPLEADO CON NOMBRE SOLO ESPACIOS
# CUBRE: Líneas 88-89 de empleados.py (validación string vacío después de strip)
# =========================================================
def test_crear_empleado_nombre_solo_espacios():
    """
    Prueba de valores límite: verifica que un nombre que contiene
    solo espacios en blanco active la excepción.
    """
    with pytest.raises(NombreEmpleadoException, match="no puede estar vacío"):
        Empleado(
            nombre="   ",
            apellido_paterno="Lopez",
            email="test@example.com",
            username="testuser"
        )

# PRUEBA 3: CREAR EMPLEADO CON NOMBRE CON NÚMEROS
# CUBRE: Líneas 98-101 de empleados.py (validación patrón nombre)
# =========================================================
def test_crear_empleado_nombre_con_numeros():
    """
    Prueba de partición de equivalencia: verifica que un nombre
    que contiene números sea rechazado.
    """
    with pytest.raises(NombreEmpleadoException, match="solo debe contener letras"):
        Empleado(
            nombre="Juan123",
            apellido_paterno="Lopez",
            email="test@example.com",
            username="testuser"
        )
# PRUEBA 4: CREAR EMPLEADO CON NOMBRE CON SÍMBOLOS
# CUBRE: Líneas 98-101 de empleados.py (validación patrón nombre - caracteres especiales)
# =========================================================
def test_crear_empleado_nombre_con_simbolos():
    """
    Prueba de partición de equivalencia: verifica que un nombre
    que contiene símbolos (@, #, $, etc.) sea rechazado.
    """
    with pytest.raises(NombreEmpleadoException, match="solo debe contener letras"):
        Empleado(
            nombre="Juan@Perez",
            apellido_paterno="Lopez",
            email="test@example.com",
            username="testuser"
        )

# PRUEBA 5: CREAR EMPLEADO CON APELLIDO PATERNO NONE
# CUBRE: Líneas 107-108 de empleados.py (validación tipo None apellido paterno)
# =========================================================
def test_crear_empleado_apellido_paterno_none():
    """
    Prueba de valores límite: verifica que pasar None como apellido paterno
    active la excepción NombreEmpleadoException.
    """
    with pytest.raises(NombreEmpleadoException, match="no puede estar vacío"):
        Empleado(
            nombre="Juan",
            apellido_paterno=None,
            email="test@example.com",
            username="testuser"
        )

# PRUEBA 6: CREAR EMPLEADO CON APELLIDO PATERNO SOLO ESPACIOS
# CUBRE: Líneas 110-111 de empleados.py (validación string vacío apellido paterno)
# =========================================================
def test_crear_empleado_apellido_paterno_solo_espacios():
    """
    Prueba de valores límite: verifica que un apellido paterno que contiene
    solo espacios en blanco active la excepción.
    """
    with pytest.raises(NombreEmpleadoException, match="no puede estar vacío"):
        Empleado(
            nombre="Juan",
            apellido_paterno="   ",
            email="test@example.com",
            username="testuser"
        )

# PRUEBA 7: CREAR EMPLEADO CON APELLIDO PATERNO CON NÚMEROS
# CUBRE: Líneas 120-123 de empleados.py (validación patrón apellido paterno)
# =========================================================
def test_crear_empleado_apellido_paterno_con_numeros():
    """
    Prueba de partición de equivalencia: verifica que un apellido paterno
    que contiene números sea rechazado.
    """
    with pytest.raises(NombreEmpleadoException, match="solo debe contener letras"):
        Empleado(
            nombre="Juan",
            apellido_paterno="Lopez123",
            email="test@example.com",
            username="testuser"
        )

# PRUEBA 8: CREAR EMPLEADO CON EMAIL NONE
# CUBRE: Líneas 149-150 de empleados.py (validación tipo None email)
# =========================================================
def test_crear_empleado_email_none():
    """
    Prueba de valores límite: verifica que pasar None como email
    active la excepción EmailEmpleadoException.
    """
    with pytest.raises(EmailEmpleadoException, match="no puede estar vacío"):
        Empleado(
            nombre="Juan",
            apellido_paterno="Lopez",
            email=None,
            username="testuser"
        )

# PRUEBA 9: CREAR EMPLEADO CON EMAIL SOLO ESPACIOS
# CUBRE: Líneas 152-153 de empleados.py (validación email vacío después de strip)
# =========================================================
def test_crear_empleado_email_solo_espacios():
    """
    Prueba de valores límite: verifica que un email que contiene
    solo espacios en blanco active la excepción.
    """
    with pytest.raises(EmailEmpleadoException, match="no puede estar vacío"):
        Empleado(
            nombre="Juan",
            apellido_paterno="Lopez",
            email="   ",
            username="testuser"
        )

# PRUEBA 10: CREAR EMPLEADO CON EMAIL SIN PUNTO EN DOMINIO
# CUBRE: Líneas 177-178 de empleados.py (validación punto en dominio)
# =========================================================
def test_crear_empleado_email_sin_punto_dominio():
    """
    Prueba de partición de equivalencia: verifica que un email
    sin punto en el dominio sea rechazado.
    """
    with pytest.raises(EmailEmpleadoException, match="formato de correo electrónico inválido"):
        Empleado(
            nombre="Juan",
            apellido_paterno="Lopez",
            email="usuario@dominio",
            username="testuser"
        )

# PRUEBA 11: CREAR EMPLEADO CON TELÉFONO CON LETRAS
# CUBRE: Líneas 190-193 de empleados.py (validación patrón teléfono)
# =========================================================
def test_crear_empleado_telefono_con_letras():
    """
    Prueba de partición de equivalencia: verifica que un teléfono
    que contiene letras sea rechazado.
    """
    with pytest.raises(TelefonoEmpleadoException, match="formato de teléfono inválido"):
        Empleado(
            nombre="Juan",
            apellido_paterno="Lopez",
            email="test@example.com",
            username="testuser",
            telefono="123ABC456"
        )

# PRUEBA 12: CREAR EMPLEADO CON TELÉFONO DEMASIADO CORTO
# CUBRE: Líneas 190-193 de empleados.py (validación longitud mínima)
# =========================================================
def test_crear_empleado_telefono_demasiado_corto():
    """
    Prueba de valores límite: verifica que un teléfono con menos de 8 dígitos
    sea rechazado.
    """
    with pytest.raises(TelefonoEmpleadoException, match="formato de teléfono inválido"):
        Empleado(
            nombre="Juan",
            apellido_paterno="Lopez",
            email="test@example.com",
            username="testuser",
            telefono="1234567"
        )

# PRUEBA 13: CREAR EMPLEADO CON FECHA COMO DATETIME
# CUBRE: Líneas 203-204 de empleados.py (conversión de datetime a string)
# =========================================================
def test_crear_empleado_fecha_contratacion_datetime():
    """
    Prueba de integración: verifica que pasar un objeto datetime
    como fecha_contratacion sea convertido correctamente a string.
    """
    from datetime import datetime
    fecha = datetime(2023, 6, 15)
    empleado = Empleado(
        nombre="Juan",
        apellido_paterno="Lopez",
        email="test@example.com",
        username="testuser",
        fecha_contratacion=fecha
    )
    assert empleado.fecha_contratacion == "2023-06-15"

    # PRUEBA 14: CREAR EMPLEADO CON USERNAME NONE
# CUBRE: Líneas 214-215 de empleados.py (validación tipo None username)
# =========================================================
def test_crear_empleado_username_none():
    """
    Prueba de valores límite: verifica que pasar None como username
    active la excepción UsernameEmpleadoException.
    """
    with pytest.raises(UsernameEmpleadoException, match="no puede estar vacío"):
        Empleado(
            nombre="Juan",
            apellido_paterno="Lopez",
            email="test@example.com",
            username=None
        )

# PRUEBA 15: ACTUALIZAR CONTRASEÑA CON NONE
# CUBRE: Líneas 410-411 de empleados.py (validación nueva_password None)
# =========================================================
def test_actualizar_password_none(empleado_temporal):
    """
    Prueba de valores límite: verifica que actualizar la contraseña
    con None active la excepción PasswordEmpleadoException.
    """
    with pytest.raises(PasswordEmpleadoException, match="no puede estar vacía"):
        empleado_temporal.actualizar_password(None)

# PRUEBA 16: ACTUALIZAR CONTRASEÑA CORTA
# CUBRE: Líneas 421-424 de empleados.py (validación longitud mínima)
# =========================================================
def test_actualizar_password_corta(empleado_temporal):
    """
    Prueba de valores límite: verifica que actualizar la contraseña
    con una cadena de menos de 6 caracteres active la excepción.
    """
    with pytest.raises(PasswordEmpleadoException, match="debe tener al menos 6 caracteres"):
        empleado_temporal.actualizar_password("12345")

# PRUEBA 17: ACTUALIZAR CONTRASEÑA LARGA
# CUBRE: Líneas 426-429 de empleados.py (validación longitud máxima)
# =========================================================
def test_actualizar_password_larga(empleado_temporal):
    """
    Prueba de valores límite: verifica que actualizar la contraseña
    con una cadena de más de 30 caracteres active la excepción.
    """
    with pytest.raises(PasswordEmpleadoException, match="no puede exceder los 30 caracteres"):
        empleado_temporal.actualizar_password("a" * 31)

# PRUEBA 18: CONSULTAR EMPLEADO POR ID NO NUMÉRICO
# CUBRE: Líneas 572-573 de empleados.py (manejo de ValueError/TypeError)
# =========================================================
def test_consultar_empleado_por_id_texto():
    """
    Prueba de valores límite: verifica que consultar un empleado
    con un ID que no es número retorne None.
    """
    resultado = Empleado.consultar_por_id("no_es_numero")
    assert resultado is None

# PRUEBA 19: VERIFICAR CREDENCIALES CON USERNAME NONE
# CUBRE: Líneas 625-626 de empleados.py (validación username None)
# =========================================================
def test_verificar_credenciales_username_none():
    """
    Prueba de valores límite: verifica que verificar credenciales
    con username None retorne None.
    """
    resultado = Empleado.verificar_credenciales(None, "password123")
    assert resultado is None

# PRUEBA 20: VERIFICAR CREDENCIALES CON USERNAME VACÍO
# CUBRE: Líneas 631-632 de empleados.py (validación username vacío después de strip)
# =========================================================
def test_verificar_credenciales_username_vacio():
    """
    Prueba de valores límite: verifica que verificar credenciales
    con username vacío retorne None.
    """
    resultado = Empleado.verificar_credenciales("   ", "password123")
    assert resultado is None

# PRUEBA 21: VERIFICAR CREDENCIALES CON PASSWORD NONE
# CUBRE: Líneas 634-635 de empleados.py (validación password None)
# =========================================================
def test_verificar_credenciales_password_none():
    """
    Prueba de valores límite: verifica que verificar credenciales
    con password None retorne None.
    """
    resultado = Empleado.verificar_credenciales("usuario", None)
    assert resultado is None

# PRUEBA 22: VERIFICAR CREDENCIALES CON PASSWORD VACÍO
# CUBRE: Líneas 640-641 de empleados.py (validación password vacío después de strip)
# =========================================================
def test_verificar_credenciales_password_vacio():
    """
    Prueba de valores límite: verifica que verificar credenciales
    con password vacío retorne None.
    """
    resultado = Empleado.verificar_credenciales("usuario", "   ")
    assert resultado is None



# PRUEBA 25: CREAR EMPLEADO CON ROL INVÁLIDO
# CUBRE: Líneas 268-269 de empleados.py (validación rol permitido)
# =========================================================
def test_crear_empleado_rol_invalido():
    """
    Prueba de partición de equivalencia: verifica que crear un empleado
    con un rol no válido (diferente de 'vendedor' o 'admin') active ValueError.
    """
    with pytest.raises(ValueError, match="rol inválido"):
        Empleado(
            nombre="Juan",
            apellido_paterno="Lopez",
            email="test@example.com",
            username="testuser",
            rol="superadmin"
        )




# =========================================================
# PRUEBA 29: CONSULTAR PRODUCTO POR NOMBRE INEXISTENTE
# CUBRE: Líneas de Producto.consultar_por_nombre (models.py)
# =========================================================
def test_consultar_producto_por_nombre_inexistente():
    """
    Prueba de valores límite: busca un nombre que no existe en la BD.
    """
    from appweb.models import Producto
    
    resultado = Producto.consultar_por_nombre("PRODUCTO_INEXISTENTE_XYZ_999")
    assert resultado == []