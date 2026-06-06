# tests/integration/test_autenticacion.py

import pytest
import time
from appweb.empleados import Empleado
from appweb.postgres_db import pgdb


# =========================================================
# LOGIN EXITOSO ADMIN
# =========================================================
@pytest.mark.parametrize("username,password", [
    ("admin", "admin"),
])
def test_login_admin_exitoso(client, username, password):
    response = client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Bienvenido" in texto
    assert "Administrador" in texto or "admin" in texto


# =========================================================
# LOGIN EXITOSO VENDEDOR - Creación con hash correcto
# =========================================================
def test_login_vendedor_exitoso(client):
    """Prueba login de vendedor - crea un vendedor con contraseña hasheada"""
    
    username = "vendedor_test"
    password = "test123"
    
    # Limpiar si existe
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE username = %s", (username,))
    
    # Crear vendedor (el método insertar ya hashea la contraseña)
    nuevo_vendedor = Empleado(
        nombre="Test",
        apellido_paterno="Vendedor",
        email=f"{username}@example.com",
        username=username,
        password=password,  # Se hasheará automáticamente al insertar
        rol="vendedor"
    )
    nuevo_vendedor.insertar()
    
    # Probar login con la contraseña en texto plano
    response = client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Bienvenido" in texto
    
    # Limpiar
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE username = %s", (username,))


# =========================================================
# LOGIN INVALIDO - Credenciales incorrectas
# =========================================================
def test_login_password_incorrecta(client):
    """Contraseña incorrecta - debe retornar 401 y mensaje de error"""
    response = client.post(
        "/login",
        data={"username": "admin", "password": "incorrecta"},
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 401
    assert "Credenciales incorrectas" in texto


def test_login_usuario_inexistente(client):
    """Usuario inexistente - debe retornar 401 y mensaje de error"""
    response = client.post(
        "/login",
        data={"username": "usuario_inexistente_xyz", "password": "admin"},
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 401
    assert "Credenciales incorrectas" in texto


def test_login_usuario_vacio(client):
    """Usuario vacío - debe retornar 401 y mensaje específico"""
    response = client.post(
        "/login",
        data={"username": "", "password": "admin"},
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 401
    assert "nombre de usuario es requerido" in texto.lower()


def test_login_password_vacio(client):
    """Contraseña vacía - debe retornar 401 y mensaje específico"""
    response = client.post(
        "/login",
        data={"username": "admin", "password": ""},
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 401
    assert "contraseña es requerida" in texto.lower()


def test_login_credenciales_vacias(client):
    """Credenciales vacías - debe retornar 401 y mensaje de usuario requerido"""
    response = client.post(
        "/login",
        data={"username": "", "password": ""},
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 401
    assert "nombre de usuario es requerido" in texto.lower()


# =========================================================
# LOGOUT
# =========================================================
def test_logout(client):
    # Primero iniciar sesión
    client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=True
    )
    # Luego cerrar sesión
    response = client.get("/logout", follow_redirects=True)
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Has cerrado sesión correctamente" in texto
    assert "Iniciar sesión" in texto

# =========================================================
# EMPLEADO ADMIN EXITOSO
# =========================================================
def test_login_empleado_admin_exitoso(client):
    """Prueba login de empleado con rol administrador"""
    from appweb.empleados import Empleado
    from appweb.postgres_db import pgdb
    
    unique_id = int(time.time())  # AHORA FUNCIONA
    username = f"admin_test_{unique_id}"
    password = "admin123"
    
    # Limpiar por si acaso
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE username = %s", (username,))
    
    # Crear empleado admin
    empleado = Empleado(
        nombre="Admin",
        apellido_paterno="Test",
        email=f"{username}@example.com",
        username=username,
        password=password,
        rol="admin"
    )
    empleado.insertar()
    
    # Login
    response = client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Bienvenido" in texto
    assert "admin" in texto.lower()
    
    # Limpiar
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE username = %s", (username,))