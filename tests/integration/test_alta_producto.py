# tests/integration/test_alta_producto.py

import pytest
import time
from appweb.empleados import Empleado
from appweb.postgres_db import pgdb


# =========================================================
# DATOS DE PRUEBA CON NOMBRE ÚNICO
# =========================================================

def producto_valido():
    unique_id = int(time.time())
    return {
        "nombre": f"Producto Test {unique_id}",
        "precio": "100.00",
        "stock": "10",
        "tipo_descuento": "ninguno",
        "descuento_valor": "0"
    }


DATOS_INVALIDOS = [
    ({"nombre": "", "precio": "100", "stock": "10", "tipo_descuento": "ninguno", "descuento_valor": "0"},
     "El nombre del producto no puede estar vacío"),
    ({"nombre": "Producto", "precio": "0", "stock": "10", "tipo_descuento": "ninguno", "descuento_valor": "0"},
     "El precio debe ser mayor que cero"),
    ({"nombre": "Producto", "precio": "100", "stock": "-5", "tipo_descuento": "ninguno", "descuento_valor": "0"},
     "El stock no puede ser negativo"),
    ({"nombre": "Producto", "precio": "abc", "stock": "10", "tipo_descuento": "ninguno", "descuento_valor": "0"},
     "El precio debe ser un número válido"),
    ({"nombre": "Producto", "precio": "100", "stock": "xyz", "tipo_descuento": "ninguno", "descuento_valor": "0"},
     "El stock debe ser un número entero válido"),
]


# =========================================================
# FIXTURE PARA VENDEDOR DE PRUEBA
# =========================================================
@pytest.fixture
def client_login_vendedor_prueba(client):
    """Crea un vendedor temporal y hace login (misma solución que antes)"""
    username = "vendedor_test"
    password = "test123"
    
    # Limpiar si existe
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE username = %s", (username,))
    
    # Crear vendedor (el método insertar ya hashea la contraseña)
    nuevo_vendedor = Empleado(
        nombre="Test",
        apellido_paterno="Vendedor",
        apellido_materno="Prueba",
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
    
    # Limpiar después de la prueba
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE username = %s", (username,))


# =========================================================
# PRUEBAS
# =========================================================

def test_alta_producto_exitosa(client_login_admin):
    """Admin puede crear producto exitosamente con nombre único"""
    datos = producto_valido()
    
    response = client_login_admin.post(
        "/agregar_producto",
        data=datos,
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "agregado correctamente" in texto.lower()
    
    # Limpiar: eliminar el producto creado
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM productos WHERE nombre = %s", (datos["nombre"],))


@pytest.mark.parametrize("datos,mensaje_esperado", DATOS_INVALIDOS)
def test_alta_producto_datos_invalidos(client_login_admin, datos, mensaje_esperado):
    """Datos inválidos deben mostrar mensaje de error"""
    response = client_login_admin.post(
        "/agregar_producto",
        data=datos,
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert mensaje_esperado in texto


def test_alta_producto_sin_autenticacion(client):
    """Sin sesión debe redirigir al login"""
    response = client.post(
        "/agregar_producto",
        data=producto_valido(),
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "No se ha iniciado sesión" in texto or "login" in texto.lower()


def test_alta_producto_con_vendedor(client_login_vendedor_prueba):
    """Vendedor NO debe poder crear productos (solo admin)"""
    response = client_login_vendedor_prueba.post(
        "/agregar_producto",
        data=producto_valido(),
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    # Debe mostrar mensaje de acceso denegado
    assert "Acceso denegado" in texto or "permisos de administrador" in texto