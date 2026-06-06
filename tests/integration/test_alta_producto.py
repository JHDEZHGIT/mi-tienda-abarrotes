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


# =========================================================
# DATOS PARA PRUEBAS DE EXCEPCIONES
# =========================================================

def producto_con_tipo_descuento_invalido():
    unique_id = int(time.time())
    return {
        "nombre": f"Producto Descuento Inválido {unique_id}",
        "precio": "100.00",
        "stock": "10",
        "tipo_descuento": "tipo_invalido",
        "descuento_valor": "0"
    }


def producto_con_valor_descuento_invalido():
    unique_id = int(time.time())
    return {
        "nombre": f"Producto Valor Descuento Inválido {unique_id}",
        "precio": "100.00",
        "stock": "10",
        "tipo_descuento": "porcentaje",
        "descuento_valor": "3"  # 3% no es múltiplo de 5
    }


def producto_duplicado():
    # Usar un nombre fijo para probar duplicados
    return {
        "nombre": "Producto Duplicado Test",
        "precio": "100.00",
        "stock": "10",
        "tipo_descuento": "ninguno",
        "descuento_valor": "0"
    }


# =========================================================
# FIXTURE PARA VENDEDOR DE PRUEBA
# =========================================================
@pytest.fixture
def client_login_vendedor_prueba(client):
    """Crea un vendedor temporal y hace login"""
    username = "vendedor_test"
    password = "test123"
    
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE username = %s", (username,))
    
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
    
    client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True
    )
    
    yield client
    
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE username = %s", (username,))


# =========================================================
# PRUEBA DE ALTA DE PRODUCTO EXITOSA
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
    
    # Limpiar
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM productos WHERE nombre = %s", (datos["nombre"],))


# =========================================================
# PRUEBAS DE EXCEPCIONES - CUBREN LÍNEAS 311-322
# =========================================================

def test_alta_producto_exception_tipo_descuento(client_login_admin):
    """
    Prueba para cubrir TipoDescuentoException (línea 317-318)
    Tipo de descuento inválido
    """
    datos = producto_con_tipo_descuento_invalido()
    
    response = client_login_admin.post(
        "/agregar_producto",
        data=datos,
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "descuento" in texto.lower() or "inválido" in texto.lower()


def test_alta_producto_exception_valor_descuento(client_login_admin):
    """
    Prueba para cubrir DescuentoValorException (línea 319-320)
    Valor de descuento inválido (porcentaje no múltiplo de 5)
    """
    datos = producto_con_valor_descuento_invalido()
    
    response = client_login_admin.post(
        "/agregar_producto",
        data=datos,
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "porcentaje" in texto.lower() or "inválido" in texto.lower() or "múltiplo" in texto.lower()


def test_alta_producto_exception_duplicado(client_login_admin):
    """
    Prueba para cubrir AltaProductoException (línea 321-322)
    Producto duplicado (mismo nombre)
    """
    datos = producto_duplicado()
    
    # Primera inserción - debe funcionar
    response1 = client_login_admin.post(
        "/agregar_producto",
        data=datos,
        follow_redirects=True
    )
    assert response1.status_code == 200
    
    # Segunda inserción con el mismo nombre - debe lanzar AltaProductoException
    response2 = client_login_admin.post(
        "/agregar_producto",
        data=datos,
        follow_redirects=True
    )
    texto = response2.get_data(as_text=True)
    assert response2.status_code == 200
    assert "ya existe" in texto.lower() or "duplicado" in texto.lower()
    
    # Limpiar el producto creado
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM productos WHERE nombre = %s", (datos["nombre"],))


def test_alta_producto_exception_precio_invalido(client_login_admin):
    """
    Prueba para cubrir PrecioProductoException (línea 313-314)
    Precio inválido (caracteres no numéricos)
    """
    unique_id = int(time.time())
    
    datos = {
        "nombre": f"Producto Precio Inválido {unique_id}",
        "precio": "abc",
        "stock": "10",
        "tipo_descuento": "ninguno",
        "descuento_valor": "0"
    }
    
    response = client_login_admin.post(
        "/agregar_producto",
        data=datos,
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "número válido" in texto.lower() or "válido" in texto.lower()


def test_alta_producto_exception_precio_cero(client_login_admin):
    """
    Prueba para cubrir PrecioProductoException (línea 313-314)
    Precio cero
    """
    unique_id = int(time.time())
    
    datos = {
        "nombre": f"Producto Precio Cero {unique_id}",
        "precio": "0",
        "stock": "10",
        "tipo_descuento": "ninguno",
        "descuento_valor": "0"
    }
    
    response = client_login_admin.post(
        "/agregar_producto",
        data=datos,
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "mayor que cero" in texto.lower()


def test_alta_producto_exception_stock_negativo(client_login_admin):
    """
    Prueba para cubrir StockProductoException (línea 315-316)
    Stock negativo
    """
    unique_id = int(time.time())
    
    datos = {
        "nombre": f"Producto Stock Negativo {unique_id}",
        "precio": "100.00",
        "stock": "-5",
        "tipo_descuento": "ninguno",
        "descuento_valor": "0"
    }
    
    response = client_login_admin.post(
        "/agregar_producto",
        data=datos,
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "negativo" in texto.lower() or "stock" in texto.lower()


def test_alta_producto_exception_stock_no_numerico(client_login_admin):
    """
    Prueba para cubrir StockProductoException (línea 315-316)
    Stock no numérico
    """
    unique_id = int(time.time())
    
    datos = {
        "nombre": f"Producto Stock No Numerico {unique_id}",
        "precio": "100.00",
        "stock": "abc",
        "tipo_descuento": "ninguno",
        "descuento_valor": "0"
    }
    
    response = client_login_admin.post(
        "/agregar_producto",
        data=datos,
        follow_redirects=True
    )
    texto = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "número entero válido" in texto.lower()


# =========================================================
# PRUEBAS DE DATOS INVÁLIDOS (PARAMETRIZADAS)
# =========================================================

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


# =========================================================
# PRUEBAS DE AUTENTICACIÓN
# =========================================================

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
    assert "Acceso denegado" in texto or "permisos de administrador" in texto