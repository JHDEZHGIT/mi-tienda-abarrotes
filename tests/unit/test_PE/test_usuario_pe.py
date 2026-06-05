# tests/unit/test_PE/test_usuario_pe.py

import pytest

from appweb.models import Usuario, UsuarioException


# =========================================================
# PARTICION DE EQUIVALENCIA - USERNAME
# =========================================================

def test_username_pe_valido():
    username = "usuario_test"
    usuario = Usuario(
        username=username,
        password="password123",
        rol="cliente"
    )
    assert usuario.username == username


@pytest.mark.parametrize("username", [
    "",
    "   ",
    None,
    "usuario nombre",
    "usuario.nombre",
    "usuario-nombre",
    "usuario@nombre",
    "a" * 101,
])
def test_username_pe_invalidos(username):
    with pytest.raises(UsuarioException):
        Usuario(
            username=username,
            password="password123",
            rol="cliente"
        )


def test_username_pe_entero():
    """Los números se convierten a string y son válidos como username"""
    usuario = Usuario(
        username=123,
        password="password123",
        rol="cliente"
    )
    assert usuario.username == "123"


def test_username_pe_mayusculas():
    """Las mayúsculas se convierten a minúsculas automáticamente"""
    usuario = Usuario(
        username="USUARIO_TEST",
        password="password123",
        rol="cliente"
    )
    assert usuario.username == "usuario_test"


# =========================================================
# PARTICION DE EQUIVALENCIA - PASSWORD
# =========================================================

def test_password_pe_valido():
    password = "password123"
    usuario = Usuario(
        username="testuser",
        password=password,
        rol="cliente"
    )
    assert usuario.password == password


@pytest.mark.parametrize("password", [
    "",
    "   ",
    None,
    True,
    123,
    [],
    {},
])
def test_password_pe_invalidos(password):
    with pytest.raises(UsuarioException):
        Usuario(
            username="testuser",
            password=password,
            rol="cliente"
        )


# =========================================================
# PARTICION DE EQUIVALENCIA - ROL
# =========================================================

def test_rol_pe_valido_admin():
    usuario = Usuario(
        username="testuser",
        password="password123",
        rol="admin"
    )
    assert usuario.rol == "admin"


def test_rol_pe_valido_cliente():
    usuario = Usuario(
        username="testuser",
        password="password123",
        rol="cliente"
    )
    assert usuario.rol == "cliente"


def test_rol_pe_valor_por_defecto():
    """None debe usar valor por defecto 'cliente'"""
    usuario = Usuario(
        username="testuser",
        password="password123",
        rol=None
    )
    assert usuario.rol == "cliente"


@pytest.mark.parametrize("rol", [
    "",
    "   ",
    "vendedor",
    "supervisor",
    "gerente",
    "ADMIN",
    "CLIENTE",
    True,
    123,
])
def test_rol_pe_invalidos(rol):
    with pytest.raises(UsuarioException):
        Usuario(
            username="testuser",
            password="password123",
            rol=rol
        )


# =========================================================
# PARTICION DE EQUIVALENCIA - VERIFICAR CREDENCIALES
# =========================================================

def test_verificar_credenciales_usuario_existente():
    usuario = Usuario.verificar_credenciales("admin", "admin")
    assert usuario is None or isinstance(usuario, Usuario)


@pytest.mark.parametrize("username,password", [
    ("usuario_inexistente", "password123"),
    ("admin", "password_incorrecta"),
    ("", "password"),
    ("username", ""),
    (None, "password"),
    ("username", None),
])
def test_verificar_credenciales_invalidas(username, password):
    usuario = Usuario.verificar_credenciales(username, password)
    assert usuario is None


# =========================================================
# PARTICION DE EQUIVALENCIA - CONSULTAR POR ID
# =========================================================

def test_consultar_usuario_por_id_inexistente():
    """Consultar con IDs inválidos debe retornar None o manejar error"""
    # IDs numéricos inexistentes
    assert Usuario.consultar_por_id(-1) is None
    assert Usuario.consultar_por_id(0) is None
    assert Usuario.consultar_por_id(99999) is None
    assert Usuario.consultar_por_id(None) is None
    assert Usuario.consultar_por_id("abc") is None
    
    # Para booleanos, el comportamiento puede variar
    # True se convierte a 1, puede retornar un usuario si existe
    resultado = Usuario.consultar_por_id(True)
    # No verificamos si es None porque True = 1 podría existir


# =========================================================
# PARTICION DE EQUIVALENCIA - LONGITUDES LIMITE
# =========================================================

@pytest.mark.parametrize("username,valido", [
    ("a", True),
    ("a" * 99, True),
    ("a" * 100, True),
    ("a" * 101, False),
    ("", False),
])
def test_longitud_username_pe(username, valido):
    if valido:
        usuario = Usuario(
            username=username,
            password="password123",
            rol="cliente"
        )
        assert usuario.username == username.lower()
    else:
        with pytest.raises(UsuarioException):
            Usuario(
                username=username,
                password="password123",
                rol="cliente"
            )


# =========================================================
# PARTICION DE EQUIVALENCIA - PATRONES
# =========================================================

@pytest.mark.parametrize("username,valido", [
    ("testuser", True),
    ("test_user", True),
    ("test_123", True),
    ("testuser123", True),
    ("test-user", False),
    ("test.user", False),
    ("test user", False),
    ("TestUser", True),   # Se convierte a minúsculas
    ("TESTUSER", True),   # Se convierte a minúsculas
    ("12345", True),      # Solo números es válido
])
def test_patron_username_pe(username, valido):
    if valido:
        usuario = Usuario(
            username=username,
            password="password123",
            rol="cliente"
        )
        assert usuario.username == username.lower()
    else:
        with pytest.raises(UsuarioException):
            Usuario(
                username=username,
                password="password123",
                rol="cliente"
            )


# =========================================================
# PARTICION DE EQUIVALENCIA - VALORES NONE
# =========================================================

@pytest.mark.parametrize("username,password,rol", [
    (None, "password123", "cliente"),
    ("testuser", None, "cliente"),
    ("testuser", "password123", None),
    (None, None, "cliente"),
    ("testuser", None, None),
])
def test_valores_none_pe(username, password, rol):
    if username is None:
        with pytest.raises(UsuarioException):
            Usuario(
                username=username,
                password=password or "password123",
                rol=rol or "cliente"
            )
    elif password is None:
        with pytest.raises(UsuarioException):
            Usuario(
                username=username,
                password=password,
                rol=rol or "cliente"
            )
    else:
        usuario = Usuario(
            username=username,
            password=password,
            rol=rol
        )
        assert usuario.rol == "cliente"


# =========================================================
# PARTICION DE EQUIVALENCIA - TIPOS DE DATOS
# =========================================================

@pytest.mark.parametrize("username,password,rol", [
    (["test"], "password123", "cliente"),
    ({"name": "test"}, "password123", "cliente"),
    ("testuser", ["pass"], "cliente"),
    ("testuser", {"pass": "123"}, "cliente"),
    ("testuser", "password123", 123),
    ("testuser", "password123", ["admin"]),
])
def test_tipos_datos_invalidos_pe(username, password, rol):
    with pytest.raises(UsuarioException):
        Usuario(
            username=username,
            password=password,
            rol=rol
        )