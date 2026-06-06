# tests/conftest.py

import pytest
import sys
import os
import secrets

# Agregar el directorio src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Verificar que funciona
try:
    from appweb.sistema import app
    print("✅ App importada correctamente")
except ImportError as e:
    print(f"❌ Error importando app: {e}")
    sys.exit(1)

# Importar fixtures de productos
from tests.fixtures.productos_fixtures import (
    producto_prueba,
    producto_con_descuento,
    producto_2x1,
    producto_stock_limite
)


# ============================================
# CLIENTE FLASK
# ============================================
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ============================================
# LOGIN ADMIN
# ============================================
@pytest.fixture
def client_login_admin(client):
    client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=True
    )
    return client


# ============================================
# FIXTURE PARA GARANTIZAR VENDEDOR EXISTENTE (tello)
# ============================================
@pytest.fixture
def vendedor_existente():
    """Fixture que asegura que el vendedor 'tello' existe en la BD para pruebas"""
    from appweb.empleados import Empleado
    
    vendedor = Empleado.verificar_credenciales("tello", "vendedor123")
    
    if not vendedor:
        try:
            nuevo_vendedor = Empleado(
                nombre="Angel Antonio",
                apellido_paterno="Tello",
                apellido_materno="Montes De Oca",
                email="tello@example.com",
                telefono="5512345678",
                username="tello",
                password="vendedor123",
                rol="vendedor"
            )
            nuevo_vendedor.insertar()
        except Exception as e:
            print(f"Nota: El vendedor ya existe o error: {e}")
    
    yield


# ============================================
# LOGIN VENDEDOR TELLO
# ============================================
@pytest.fixture
def client_login_vendedor(client, vendedor_existente):
    client.post(
        "/login",
        data={"username": "tello", "password": "vendedor123"},
        follow_redirects=True
    )
    return client


# ============================================
# FIXTURE PARA VENDEDOR TEMPORAL (para pruebas de ventas)
# ============================================
@pytest.fixture
def client_login_vendedor_temporal(client):
    """Usa un vendedor fijo para pruebas de ventas."""
    from appweb.empleados import Empleado
    
    username = "vendedor_ventas_test"
    password = "test123"
    
    vendedor = Empleado.verificar_credenciales(username, password)
    
    if not vendedor:
        nuevo_vendedor = Empleado(
            nombre="Ventas",
            apellido_paterno="Test",
            apellido_materno="Vendedor",
            email=f"{username}@example.com",
            telefono="5512345678",
            username=username,
            password=password,
            rol="vendedor"
        )
        nuevo_vendedor.insertar()
    
    client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True
    )
    
    yield client


# ============================================
# FIXTURES PARA PRUEBAS DE EMPLEADOS
# ============================================

@pytest.fixture
def empleado_temporal():
    """
    Crea un empleado temporal para pruebas y lo elimina al finalizar.
    CUBRE: Pruebas de actualización, cambio de contraseña, etc.
    """
    from appweb.empleados import Empleado
    from appweb.postgres_db import pgdb
    
    suffix = secrets.token_hex(4)
    empleado = Empleado(
        nombre="Temp",
        apellido_paterno="Test",
        email=f"temp{suffix}@example.com",
        username=f"tempuser{suffix}",
        password="password123"
    )
    empleado_id = empleado.insertar()
    empleado.id = empleado_id
    
    yield empleado
    
    # Limpiar después de la prueba
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE id = %s", (empleado.id,))


@pytest.fixture
def empleado_existente():
    """
    Crea un empleado con credenciales fijas para pruebas de duplicados.
    NO se elimina al finalizar porque se reutiliza entre pruebas.
    """
    from appweb.empleados import Empleado
    from appweb.postgres_db import pgdb
    
    empleado = Empleado(
        nombre="Existente",
        apellido_paterno="Test",
        email="existente_test@example.com",
        username="existente_test",
        password="password123",
        rol="admin"
    )
    
    # Verificar si ya existe para evitar duplicados entre ejecuciones
    with pgdb.get_cursor() as cur:
        cur.execute("SELECT id FROM empleados WHERE username = %s", ("existente_test",))
        existing = cur.fetchone()
    
    if existing:
        empleado.id = existing[0]
        return empleado
    
    empleado.insertar()
    return empleado


# ============================================
# EXPORTACIÓN EXPLÍCITA DE FIXTURES
# ============================================
__all__ = [
    'client',
    'client_login_admin',
    'vendedor_existente',
    'client_login_vendedor',
    'client_login_vendedor_temporal',
    'empleado_temporal',
    'empleado_existente',
    'producto_prueba',
    'producto_con_descuento',
    'producto_2x1',
    'producto_stock_limite'
]