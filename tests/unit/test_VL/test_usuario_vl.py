# tests/unit/test_VL/test_usuario_vl.py

import pytest

from appweb.models import Usuario, UsuarioException


# =========================================================
# VALORES LIMITE - USERNAME (3 valores)
# =========================================================

# VL USERNAME - Longitud mínima (1 carácter)
# =========================================================
def test_username_vl_longitud_minima():
    """VL: Username con 1 carácter (límite inferior válido)"""
    usuario = Usuario(
        username="a",
        password="password123",
        rol="cliente"
    )
    assert usuario.username == "a"
    assert len(usuario.username) == 1


def test_username_vl_longitud_menor_que_minima():
    """VL: Username con 0 caracteres (por debajo del límite - inválido)"""
    with pytest.raises(UsuarioException) as error:
        Usuario(
            username="",
            password="password123",
            rol="cliente"
        )
    assert "vacío" in str(error.value).lower() or "no puede estar vacío" in str(error.value).lower()


def test_username_vl_longitud_justo_arriba_minima():
    """VL: Username con 2 caracteres (justo por encima del límite inferior - válido)"""
    usuario = Usuario(
        username="ab",
        password="password123",
        rol="cliente"
    )
    assert usuario.username == "ab"
    assert len(usuario.username) == 2


# VL USERNAME - Longitud máxima (100 caracteres)
# =========================================================
def test_username_vl_longitud_maxima():
    """VL: Username con 100 caracteres (límite superior válido)"""
    username = "a" * 100
    usuario = Usuario(
        username=username,
        password="password123",
        rol="cliente"
    )
    assert len(usuario.username) == 100


def test_username_vl_longitud_justo_abajo_maxima():
    """VL: Username con 99 caracteres (justo por debajo del límite superior - válido)"""
    username = "a" * 99
    usuario = Usuario(
        username=username,
        password="password123",
        rol="cliente"
    )
    assert len(usuario.username) == 99


def test_username_vl_longitud_mayor_que_maxima():
    """VL: Username con 101 caracteres (por encima del límite - inválido)"""
    username = "a" * 101
    with pytest.raises(UsuarioException) as error:
        Usuario(
            username=username,
            password="password123",
            rol="cliente"
        )
    assert "exceder" in str(error.value).lower() or "demasiado largo" in str(error.value).lower()


# VL USERNAME - Caracteres permitidos (límite de patrón)
# =========================================================
def test_username_vl_caracter_permitido_limite():
    """VL: Username con guión bajo (carácter permitido en el límite del patrón)"""
    usuario = Usuario(
        username="test_user",
        password="password123",
        rol="cliente"
    )
    assert usuario.username == "test_user"


def test_username_vl_caracter_prohibido_limite():
    """VL: Username con guión (carácter prohibido por debajo del límite del patrón)"""
    with pytest.raises(UsuarioException) as error:
        Usuario(
            username="test-user",
            password="password123",
            rol="cliente"
        )
    assert "inválido" in str(error.value).lower()


def test_username_vl_caracter_justo_despues_prohibido():
    """VL: Username con punto (carácter prohibido después del límite del patrón)"""
    with pytest.raises(UsuarioException) as error:
        Usuario(
            username="test.user",
            password="password123",
            rol="cliente"
        )
    assert "inválido" in str(error.value).lower()


# =========================================================
# VALORES LIMITE - PASSWORD (3 valores)
# =========================================================

# VL PASSWORD - Longitud mínima (6 caracteres)
# =========================================================
def test_password_vl_longitud_minima():
    """VL: Password con 6 caracteres (límite inferior válido)"""
    usuario = Usuario(
        username="testuser",
        password="123456",
        rol="cliente"
    )
    assert usuario.password == "123456"


def test_password_vl_longitud_menor_que_minima():
    """VL: Password con 5 caracteres (por debajo del límite - válido? el modelo no valida longitud mínima)"""
    # Nota: El modelo Usuario no valida longitud mínima, solo que no esté vacío
    usuario = Usuario(
        username="testuser",
        password="12345",
        rol="cliente"
    )
    assert usuario.password == "12345"


def test_password_vl_longitud_justo_arriba_minima():
    """VL: Password con 7 caracteres (justo por encima del límite inferior - válido)"""
    usuario = Usuario(
        username="testuser",
        password="1234567",
        rol="cliente"
    )
    assert usuario.password == "1234567"


# VL PASSWORD - Valor vacío (límite inferior de contenido)
# =========================================================
def test_password_vl_vacio():
    """VL: Password vacío (límite inferior de contenido - inválido)"""
    with pytest.raises(UsuarioException) as error:
        Usuario(
            username="testuser",
            password="",
            rol="cliente"
        )
    assert "vacía" in str(error.value).lower()


def test_password_vl_un_caracter():
    """VL: Password con 1 carácter (justo por encima del vacío - válido)"""
    usuario = Usuario(
        username="testuser",
        password="a",
        rol="cliente"
    )
    assert usuario.password == "a"


def test_password_vl_espacios():
    """VL: Password con solo espacios (por debajo del límite de contenido significativo - inválido)"""
    with pytest.raises(UsuarioException) as error:
        Usuario(
            username="testuser",
            password="   ",
            rol="cliente"
        )
    assert "vacía" in str(error.value).lower()


# VL PASSWORD - Valor None (límite de nulabilidad)
# =========================================================
def test_password_vl_none():
    """VL: Password None (límite inferior de nulabilidad - inválido)"""
    with pytest.raises(UsuarioException) as error:
        Usuario(
            username="testuser",
            password=None,
            rol="cliente"
        )
    assert "vacía" in str(error.value).lower()


# =========================================================
# VALORES LIMITE - ROL (3 valores)
# =========================================================

# VL ROL - Valor por defecto (cliente)
# =========================================================
def test_rol_vl_por_defecto():
    """VL: Rol None (usa valor por defecto 'cliente' - límite inferior válido)"""
    usuario = Usuario(
        username="testuser",
        password="password123",
        rol=None
    )
    assert usuario.rol == "cliente"


def test_rol_vl_valor_justo_antes_por_defecto():
    """VL: Rol con string vacío (por debajo del límite de valores válidos - inválido)"""
    with pytest.raises(UsuarioException) as error:
        Usuario(
            username="testuser",
            password="password123",
            rol=""
        )
    assert "inválido" in str(error.value).lower()


def test_rol_vl_valor_justo_despues_por_defecto():
    """VL: Rol 'cliente' (el valor por defecto - válido)"""
    usuario = Usuario(
        username="testuser",
        password="password123",
        rol="cliente"
    )
    assert usuario.rol == "cliente"


# VL ROL - Valor admin (segundo valor válido)
# =========================================================
def test_rol_vl_admin():
    """VL: Rol 'admin' (segundo valor válido - límite superior de valores válidos)"""
    usuario = Usuario(
        username="testuser",
        password="password123",
        rol="admin"
    )
    assert usuario.rol == "admin"


def test_rol_vl_justo_antes_admin():
    """VL: Rol 'cliente' (justo antes de 'admin' en términos de valores válidos - válido)"""
    usuario = Usuario(
        username="testuser",
        password="password123",
        rol="cliente"
    )
    assert usuario.rol == "cliente"


def test_rol_vl_justo_despues_admin():
    """VL: Rol 'vendedor' (por encima del límite de valores válidos - inválido)"""
    with pytest.raises(UsuarioException) as error:
        Usuario(
            username="testuser",
            password="password123",
            rol="vendedor"
        )
    assert "inválido" in str(error.value).lower()


# =========================================================
# VALORES LIMITE - VERIFICAR CREDENCIALES
# =========================================================

# VL CREDENCIALES - Username
# =========================================================
def test_verificar_credenciales_username_un_caracter():
    """VL: Username con 1 carácter (límite inferior de longitud)"""
    # Nota: Depende de que exista un usuario con ese nombre
    usuario = Usuario.verificar_credenciales("a", "password")
    # No debe fallar, solo retorna None si no existe
    assert usuario is None or isinstance(usuario, Usuario)


def test_verificar_credenciales_username_cien_caracteres():
    """VL: Username con 100 caracteres (límite superior de longitud)"""
    username = "a" * 100
    usuario = Usuario.verificar_credenciales(username, "password")
    assert usuario is None or isinstance(usuario, Usuario)


def test_verificar_credenciales_username_ciento_un_caracteres():
    """VL: Username con 101 caracteres (por encima del límite - debería ser ignorado o fallar)"""
    username = "a" * 101
    usuario = Usuario.verificar_credenciales(username, "password")
    # El método debería manejar el error o retornar None
    assert usuario is None


# =========================================================
# VALORES LIMITE - CONSULTAR POR ID
# =========================================================

# VL CONSULTAR POR ID - Valores numéricos
# =========================================================
def test_consultar_usuario_id_1():
    """VL: ID = 1 (límite inferior de IDs existentes)"""
    usuario = Usuario.consultar_por_id(1)
    # Puede ser None si no existe, pero no debe fallar
    assert usuario is None or isinstance(usuario, Usuario)


def test_consultar_usuario_id_0():
    """VL: ID = 0 (por debajo del límite de IDs válidos - inválido)"""
    usuario = Usuario.consultar_por_id(0)
    assert usuario is None


def test_consultar_usuario_id_2():
    """VL: ID = 2 (justo por encima del límite inferior)"""
    usuario = Usuario.consultar_por_id(2)
    assert usuario is None or isinstance(usuario, Usuario)


# VL CONSULTAR POR ID - Valores negativos
# =========================================================
def test_consultar_usuario_id_negativo_1():
    """VL: ID = -1 (valor negativo - por debajo del límite)"""
    usuario = Usuario.consultar_por_id(-1)
    assert usuario is None


def test_consultar_usuario_id_negativo_grande():
    """VL: ID = -100 (valor negativo grande - muy por debajo del límite)"""
    usuario = Usuario.consultar_por_id(-100)
    assert usuario is None


# VL CONSULTAR POR ID - Valores grandes inexistentes
# =========================================================
def test_consultar_usuario_id_9999():
    """VL: ID = 9999 (valor grande probablemente inexistente - por encima del límite)"""
    usuario = Usuario.consultar_por_id(9999)
    assert usuario is None


def test_consultar_usuario_id_10000():
    """VL: ID = 10000 (valor redondo grande)"""
    usuario = Usuario.consultar_por_id(10000)
    assert usuario is None


# VL CONSULTAR POR ID - Tipos inválidos
# =========================================================
def test_consultar_usuario_id_string_vacio():
    """VL: ID = '' (string vacío - tipo inválido)"""
    usuario = Usuario.consultar_por_id("")
    assert usuario is None


def test_consultar_usuario_id_string_numerico():
    """VL: ID = '1' (string numérico - debería convertirse a entero)"""
    usuario = Usuario.consultar_por_id("1")
    # Puede ser None si no existe, pero no debe fallar
    assert usuario is None or isinstance(usuario, Usuario)


# =========================================================
# VALORES LIMITE - PATRONES
# =========================================================

# VL PATRON USERNAME - Límites de caracteres permitidos
# =========================================================
def test_username_patron_guion_bajo():
    """VL: Username con guión bajo (carácter permitido en el límite del patrón)"""
    usuario = Usuario(
        username="test_user_123",
        password="password123",
        rol="cliente"
    )
    assert usuario.username == "test_user_123"


def test_username_patron_mayuscula_inicio():
    """VL: Username con mayúscula al inicio (justo antes del límite de minúsculas)"""
    usuario = Usuario(
        username="Testuser",
        password="password123",
        rol="cliente"
    )
    # Se convierte a minúsculas
    assert usuario.username == "testuser"


def test_username_patron_mayuscula_intermedia():
    """VL: Username con mayúscula intermedia (justo después del límite de minúsculas)"""
    usuario = Usuario(
        username="testUser",
        password="password123",
        rol="cliente"
    )
    # Se convierte a minúsculas
    assert usuario.username == "testuser"


# VL PATRON USERNAME - Caracteres especiales
# =========================================================
def test_username_patron_espacio():
    """VL: Username con espacio (carácter prohibido en el límite)"""
    with pytest.raises(UsuarioException):
        Usuario(
            username="test user",
            password="password123",
            rol="cliente"
        )


def test_username_patron_arroba():
    """VL: Username con @ (carácter prohibido justo después del límite)"""
    with pytest.raises(UsuarioException):
        Usuario(
            username="test@user",
            password="password123",
            rol="cliente"
        )


# =========================================================
# VALORES LIMITE - VALORES NONE
# =========================================================

# VL VALORES NONE - Combinaciones límite
# =========================================================
def test_username_none_password_valido():
    """VL: Username None, password válido (límite de nulabilidad)"""
    with pytest.raises(UsuarioException):
        Usuario(
            username=None,
            password="password123",
            rol="cliente"
        )


def test_username_valido_password_none():
    """VL: Username válido, password None (límite de nulabilidad)"""
    with pytest.raises(UsuarioException):
        Usuario(
            username="testuser",
            password=None,
            rol="cliente"
        )


def test_both_none():
    """VL: Username None, password None (ambos en el límite de nulabilidad)"""
    with pytest.raises(UsuarioException):
        Usuario(
            username=None,
            password=None,
            rol="cliente"
        )


# =========================================================
# VALORES LIMITE - LONGITUD DE CAMPOS
# =========================================================

# VL LONGITUD USERNAME - Serie de valores límite
# =========================================================
@pytest.mark.parametrize("longitud,valido,descripcion", [
    (0, False, "Longitud 0 (por debajo del límite)"),
    (1, True, "Longitud 1 (límite inferior)"),
    (2, True, "Longitud 2 (justo arriba del límite)"),
    (99, True, "Longitud 99 (justo debajo del límite superior)"),
    (100, True, "Longitud 100 (límite superior)"),
    (101, False, "Longitud 101 (por encima del límite)"),
])
def test_username_longitud_valores_limite(longitud, valido, descripcion):
    """Prueba serie de valores límite para longitud de username"""
    username = "a" * longitud
    
    if valido:
        usuario = Usuario(
            username=username,
            password="password123",
            rol="cliente"
        )
        assert len(usuario.username) == longitud
    else:
        with pytest.raises(UsuarioException):
            Usuario(
                username=username,
                password="password123",
                rol="cliente"
            )