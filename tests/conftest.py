# tests/conftest.py

import pytest
import sys
import os

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


# CLIENTE FLASK
# ============================================
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


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
    
    # Verificar si ya existe - si existe, no hacer nada
    vendedor = Empleado.verificar_credenciales("tello", "vendedor123")
    
    if not vendedor:
        # Solo crear si NO existe
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
            # Si ya existe (error de concurrencia), ignorar
            print(f"Nota: El vendedor ya existe o error: {e}")
    
    yield


# LOGIN VENDEDOR TELLO
# ============================================
@pytest.fixture
def client_login_vendedor(client, vendedor_existente):
    """Fixture que asegura que el vendedor 'tello' existe antes de hacer login"""
    client.post(
        "/login",
        data={"username": "tello", "password": "vendedor123"},
        follow_redirects=True
    )
    return client


# ============================================
# NUEVO FIXTURE PARA VENDEDOR TEMPORAL (PARA TESTS DE VENTAS)
# NO elimina el empleado para evitar violación de FK
# ============================================
@pytest.fixture
def client_login_vendedor_temporal(client):
    """
    Usa un vendedor fijo para pruebas de ventas.
    No se elimina para evitar violaciones de foreign key.
    """
    from appweb.empleados import Empleado
    from appweb.postgres_db import pgdb
    
    username = "vendedor_ventas_test"
    password = "test123"
    
    # Verificar si existe
    vendedor = Empleado.verificar_credenciales(username, password)
    
    if not vendedor:
        # Crear vendedor
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
    
    # Hacer login
    client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True
    )
    
    yield client
    
    # No eliminar para preservar integridad referencial
    # El empleado permanece para futuras pruebas
    pass