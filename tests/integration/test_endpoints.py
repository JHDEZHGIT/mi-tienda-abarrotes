# tests/integration/test_endpoints.py

import pytest
from appweb.empleados import Empleado
from appweb.postgres_db import pgdb


# Datos de rutas protegidas
RUTAS_PROTEGIDAS = [
    ("/inicio", "Tienda de Abarrotes"),
    ("/ventas", "Punto de venta"),
    ("/carrito", "Carrito de compras"),
    ("/productos", "Gestión de productos"),
    ("/empleados", "Gestión de empleados"),
    ("/historial", "Historial de ventas"),
    ("/reporte_stock", "Reporte de inventario"),
]

RUTAS_SOLO_ADMIN = ["/productos", "/empleados", "/historial", "/reporte_stock"]


# =========================================================
# FIXTURE PARA VENDEDOR DE PRUEBA
# =========================================================
@pytest.fixture
def client_login_vendedor_prueba(client):
    """Crea un vendedor temporal y hace login (similar a test_autenticacion.py)"""
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
        password=password,  # Se hasheará automáticamente al insertar
        rol="vendedor"
    )
    nuevo_vendedor.insertar()
    
    # Hacer login con la contraseña en texto plano
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
# PRUEBAS SIN SESIÓN
# =========================================================
@pytest.mark.parametrize("ruta,texto_esperado", RUTAS_PROTEGIDAS)
def test_rutas_protegidas_sin_sesion(client, ruta, texto_esperado):
    """Verifica que las rutas protegidas redirigen al login sin sesión"""
    response = client.get(ruta, follow_redirects=True)
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Iniciar sesión" in texto or "login" in texto.lower()


# =========================================================
# PRUEBAS CON SESIÓN DE ADMIN
# =========================================================
@pytest.mark.parametrize("ruta,texto_esperado", RUTAS_PROTEGIDAS)
def test_rutas_protegidas_con_sesion_admin(client_login_admin, ruta, texto_esperado):
    """Verifica que el admin puede acceder a todas las rutas protegidas"""
    response = client_login_admin.get(ruta, follow_redirects=True)
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert texto_esperado in texto


# =========================================================
# PRUEBAS CON SESIÓN DE VENDEDOR (usando fixture con hash)
# =========================================================
@pytest.mark.parametrize("ruta,texto_esperado", [
    ("/inicio", "Tienda de Abarrotes"),
    ("/ventas", "Punto de venta"),
    ("/carrito", "Carrito de compras"),
])
def test_rutas_protegidas_con_sesion_vendedor(client_login_vendedor_prueba, ruta, texto_esperado):
    """Verifica que el vendedor puede acceder a rutas permitidas"""
    response = client_login_vendedor_prueba.get(ruta, follow_redirects=True)
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert texto_esperado in texto


# =========================================================
# PRUEBAS: VENDEDOR NO ACCEDE A RUTAS DE ADMIN
# =========================================================
@pytest.mark.parametrize("ruta", RUTAS_SOLO_ADMIN)
def test_rutas_vendedor_no_acceso(client_login_vendedor_prueba, ruta):
    """Verifica que el vendedor NO puede acceder a rutas de admin"""
    response = client_login_vendedor_prueba.get(ruta, follow_redirects=True)
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Acceso denegado" in texto or "permisos" in texto


# =========================================================
# ERROR 404
# =========================================================
def test_error_404(client):
    """Verifica que rutas inexistentes devuelven página de error o redirigen"""
    response = client.get("/ruta_que_no_existe_12345", follow_redirects=True)
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "No se ha iniciado sesión" in texto or "login" in texto.lower()