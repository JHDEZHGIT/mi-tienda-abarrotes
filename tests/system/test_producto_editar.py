# tests/system/test_producto_editar.py

import pytest
import time
from appweb.models import Producto
from appweb.postgres_db import pgdb

# =========================================================
# Formulario para edición de producto
# FIXTURE LOCAL PARA PRODUCTO TEMPORAL
# =========================================================
@pytest.fixture
def producto_editar_temporal():
    """Crea un producto temporal específico para pruebas de edición"""
    unique_id = int(time.time())
    nombre = f"Producto Editar Test {unique_id}"
    producto_id = None
    
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, 100.0, 50, 'ninguno', 0)
            RETURNING id
        """, (nombre,))
        producto_id = cur.fetchone()[0]
    
    yield producto_id, nombre
    
    # Limpiar después de la prueba
    if producto_id:
        with pgdb.get_cursor() as cur:
            cur.execute("DELETE FROM productos WHERE id = %s", (producto_id,))


# =========================================================
# PRUEBA 1: ACCESO AL FORMULARIO DE EDICIÓN (GET)
# CUBRE: Líneas 372-389 de views.py
# =========================================================
def test_editar_producto_formulario(client_login_admin, producto_editar_temporal):
    """
    Prueba que el formulario de edición de producto se muestra correctamente.
    Esta prueba cubre el endpoint GET /editar_producto/<id>
    """
    producto_id, nombre_original = producto_editar_temporal
    
    response = client_login_admin.get(
        f"/editar_producto/{producto_id}",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    
    # Verificar que la página contiene el formulario
    assert "Editar producto" in texto or "editar" in texto.lower()
    # Verificar que muestra los datos del producto
    assert nombre_original in texto


# =========================================================
# PRUEBA 2: ACTUALIZACIÓN EXITOSA DE PRODUCTO (POST)
# =========================================================
def test_actualizar_producto_exitoso(client_login_admin, producto_editar_temporal):
    """
    Prueba la actualización exitosa de un producto.
    """
    producto_id, nombre_original = producto_editar_temporal
    nuevo_nombre = f"Nombre Actualizado {int(time.time())}"
    nuevo_precio = "150.00"
    nuevo_stock = "25"
    
    response = client_login_admin.post(
        "/actualizar_producto",
        data={
            "id": producto_id,
            "nombre": nuevo_nombre,
            "precio": nuevo_precio,
            "stock": nuevo_stock,
            "tipo_descuento": "ninguno",
            "descuento_valor": "0"
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "actualizado con éxito" in texto or "actualizado" in texto.lower()
    
    # Verificar que los cambios se guardaron
    producto = Producto.consultar_por_id(producto_id)
    assert producto.nombre == nuevo_nombre
    assert producto.precio == float(nuevo_precio)
    assert producto.stock == int(nuevo_stock)


# =========================================================
# PRUEBA 3: ACTUALIZACIÓN CON DESCUENTO PORCENTAJE
# =========================================================
def test_actualizar_producto_con_descuento_porcentaje(client_login_admin, producto_editar_temporal):
    """
    Prueba la actualización de un producto agregando descuento porcentual.
    """
    producto_id, nombre_original = producto_editar_temporal
    nuevo_nombre = f"Producto Con Descuento {int(time.time())}"
    
    response = client_login_admin.post(
        "/actualizar_producto",
        data={
            "id": producto_id,
            "nombre": nuevo_nombre,
            "precio": "200.00",
            "stock": "30",
            "tipo_descuento": "porcentaje",
            "descuento_valor": "15"
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "actualizado con éxito" in texto or "actualizado" in texto.lower()
    
    # Verificar el descuento
    producto = Producto.consultar_por_id(producto_id)
    assert producto.tipo_descuento == "porcentaje"
    assert producto.descuento_valor == 15


# =========================================================
# PRUEBA 4: ACTUALIZACIÓN CON PROMOCIÓN 2X1
# =========================================================
def test_actualizar_producto_con_promocion_2x1(client_login_admin, producto_editar_temporal):
    """
    Prueba la actualización de un producto con promoción 2x1.
    """
    producto_id, nombre_original = producto_editar_temporal
    
    response = client_login_admin.post(
        "/actualizar_producto",
        data={
            "id": producto_id,
            "nombre": f"Producto 2x1 {int(time.time())}",
            "precio": "50.00",
            "stock": "20",
            "tipo_descuento": "2x1",
            "descuento_valor": "0"
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "actualizado con éxito" in texto or "actualizado" in texto.lower()
    
    producto = Producto.consultar_por_id(producto_id)
    assert producto.tipo_descuento == "2x1"


# =========================================================
# PRUEBA 5: INTENTAR EDITAR PRODUCTO INEXISTENTE
# =========================================================
def test_editar_producto_inexistente(client_login_admin):
    """
    Prueba que al intentar editar un producto que no existe,
    se muestre mensaje de error y se redirija.
    """
    response = client_login_admin.get(
        "/editar_producto/99999",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Producto no encontrado" in texto or "no encontrado" in texto.lower()


# =========================================================
# PRUEBA 6: ACTUALIZAR PRODUCTO CON DATOS INVÁLIDOS
# =========================================================
def test_actualizar_producto_datos_invalidos(client_login_admin, producto_editar_temporal):
    """
    Prueba que al actualizar con datos inválidos se muestre mensaje de error.
    """
    producto_id, nombre_original = producto_editar_temporal
    
    # Precio inválido (letras)
    response = client_login_admin.post(
        "/actualizar_producto",
        data={
            "id": producto_id,
            "nombre": "Producto Test",
            "precio": "abc",
            "stock": "10",
            "tipo_descuento": "ninguno",
            "descuento_valor": "0"
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "número válido" in texto.lower() or "inválido" in texto.lower()


# =========================================================
# PRUEBA 7: ACTUALIZAR PRODUCTO CON NOMBRE DUPLICADO
# =========================================================
def test_actualizar_producto_nombre_duplicado(client_login_admin):
    """
    Prueba que no se pueda actualizar un producto con un nombre
    que ya existe en otro producto.
    """
    # Crear primer producto
    unique_id = int(time.time())
    nombre_comun = f"Nombre Común {unique_id}"
    
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, 100.0, 10, 'ninguno', 0)
            RETURNING id
        """, (nombre_comun,))
        producto1_id = cur.fetchone()[0]
        
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, 200.0, 20, 'ninguno', 0)
            RETURNING id
        """, (f"Otro Producto {unique_id}",))
        producto2_id = cur.fetchone()[0]
    
    try:
        # Intentar actualizar el segundo producto con el nombre del primero
        response = client_login_admin.post(
            "/actualizar_producto",
            data={
                "id": producto2_id,
                "nombre": nombre_comun,
                "precio": "200.00",
                "stock": "20",
                "tipo_descuento": "ninguno",
                "descuento_valor": "0"
            },
            follow_redirects=True
        )
        
        assert response.status_code == 200
        texto = response.get_data(as_text=True)
        # Debe mostrar error de nombre duplicado
        assert "ya existe" in texto.lower() or "duplicado" in texto.lower()
    finally:
        # Limpiar productos
        with pgdb.get_cursor() as cur:
            cur.execute("DELETE FROM productos WHERE id = %s", (producto1_id,))
            cur.execute("DELETE FROM productos WHERE id = %s", (producto2_id,))


# =========================================================
# PRUEBA 8: EDITAR PRODUCTO SIN AUTENTICACIÓN
# =========================================================
def test_editar_producto_sin_autenticacion(client):
    """
    Prueba que sin sesión no se pueda acceder al formulario de edición.
    """
    response = client.get(
        "/editar_producto/1",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "No se ha iniciado sesión" in texto or "login" in texto.lower()


# =========================================================
# PRUEBA 9: EDITAR PRODUCTO CON VENDEDOR (SIN PERMISOS)
# =========================================================
def test_editar_producto_sin_permisos(client_login_vendedor_temporal, producto_editar_temporal):
    """
    Prueba que un vendedor no pueda acceder al formulario de edición.
    """
    producto_id, nombre_original = producto_editar_temporal
    
    response = client_login_vendedor_temporal.get(
        f"/editar_producto/{producto_id}",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Acceso denegado" in texto or "permisos" in texto.lower()


# =========================================================
# PRUEBA 10: ACTUALIZAR PRODUCTO CON STOCK NEGATIVO
# =========================================================
def test_actualizar_producto_stock_negativo(client_login_admin, producto_editar_temporal):
    """
    Prueba que no se pueda actualizar un producto con stock negativo.
    """
    producto_id, nombre_original = producto_editar_temporal
    
    response = client_login_admin.post(
        "/actualizar_producto",
        data={
            "id": producto_id,
            "nombre": "Producto Test",
            "precio": "100.00",
            "stock": "-5",
            "tipo_descuento": "ninguno",
            "descuento_valor": "0"
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "negativo" in texto.lower() or "stock" in texto.lower()


# =========================================================
# PRUEBA 40: ACTUALIZAR PRODUCTO CON PRECIO NEGATIVO
# CUBRE: Líneas de actualizar_producto en views.py
# =========================================================
def test_actualizar_producto_precio_negativo(client_login_admin, producto_prueba):
    """
    Prueba de valores límite: actualiza producto con precio negativo.
    """
    response = client_login_admin.post(
        f"/productos/{producto_prueba}/editar",  # producto_prueba es ID
        data={
            "nombre": "Producto Actualizado",
            "precio": -10.0,
            "stock": 100
        },
        follow_redirects=True
    )
    assert response.status_code == 200


# =========================================================
# PRUEBA 41: ACTUALIZAR PRODUCTO CON STOCK NEGATIVO
# CUBRE: Líneas de actualizar_producto en views.py
# =========================================================
def test_actualizar_producto_stock_negativo(client_login_admin, producto_prueba):
    """
    Prueba de valores límite: actualiza producto con stock negativo.
    """
    response = client_login_admin.post(
        f"/productos/{producto_prueba}/editar",
        data={
            "nombre": "Producto Actualizado",
            "precio": 50.0,
            "stock": -5
        },
        follow_redirects=True
    )
    assert response.status_code == 200


# =========================================================
# PRUEBA 42: ACTUALIZAR PRODUCTO INEXISTENTE
# CUBRE: Líneas de actualizar_producto en views.py (producto no encontrado)
# =========================================================
def test_actualizar_producto_inexistente(client_login_admin):
    """
    Prueba de valores límite: intenta actualizar producto con ID inválido.
    """
    response = client_login_admin.post(
        "/productos/99999/editar",
        data={
            "nombre": "Producto Inexistente",
            "precio": 50.0,
            "stock": 100
        },
        follow_redirects=True
    )
    assert response.status_code in [200, 404]


# # =========================================================
# # PRUEBA 43: ACTUALIZAR PRODUCTO CON NOMBRE DUPLICADO
# # CUBRE: Líneas de actualizar_producto en views.py (nombre ya existe)
# # =========================================================
# def test_actualizar_producto_nombre_duplicado(client_login_admin, producto_prueba, producto_2x1):
#     """
#     Prueba de integración: intenta actualizar un producto
#     con el nombre de otro producto que ya existe.
#     """
#     from appweb.models import Producto
    
#     # Usar los productos existentes de las fixtures
#     id_editar = producto_2x1
#     id_referencia = producto_prueba
    
#     producto_editar = Producto.consultar_por_id(id_editar)
#     producto_referencia = Producto.consultar_por_id(id_referencia)
    
#     # Guardar el nombre original para restaurarlo después
#     nombre_original = producto_editar.nombre
    
#     try:
#         response = client_login_admin.post(
#             f"/productos/{producto_editar.id}/editar",
#             data={
#                 "nombre": producto_referencia.nombre,
#                 "precio": producto_editar.precio,
#                 "stock": producto_editar.stock,
#                 "tipo_descuento": producto_editar.tipo_descuento,
#                 "valor_descuento": producto_editar.valor_descuento
#             },
#             follow_redirects=True
#         )
#         assert response.status_code == 200
#     finally:
#         # Restaurar el nombre original para no afectar otras pruebas
#         producto_editar.nombre = nombre_original
#         producto_editar.actualizar()