# tests/system/test_producto_eliminar.py

import pytest

from appweb.models import Producto, DBException

# PRUEBA: ELIMINAR PRODUCTO EXITOSO 
# CUBRE: Líneas de eliminar producto en views.py
# =========================================================
def test_eliminar_producto_exitoso(client_login_admin):
    """
    Prueba de integración: crea un producto SIN ventas y lo elimina.
    """
    sufijo = secrets.token_hex(4)
    nombre_unico = f"ProductoTempEliminar{sufijo}"
    
    nuevo_producto = Producto(
        nombre=nombre_unico,
        precio=100.0,
        stock=50,
        tipo_descuento="ninguno"
    )
    producto_id = nuevo_producto.insertar()
    
    # Verificar que el producto NO tiene ventas asociadas
    with pgdb.get_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM ventas WHERE producto_id = %s", (producto_id,))
        ventas_count = cur.fetchone()[0]
    assert ventas_count == 0, "El producto no debería tener ventas asociadas"
    
    # Eliminar el producto
    response = client_login_admin.get(
        f"/eliminar_producto/{producto_id}",
        follow_redirects=True
    )
    assert response.status_code == 200
    
    # Verificar que fue eliminado
    with pgdb.get_cursor() as cur:
        cur.execute("SELECT id FROM productos WHERE id = %s", (producto_id,))
        existe = cur.fetchone()
    
    assert existe is None, f"El producto {producto_id} debería haber sido eliminado"


def test_eliminar_producto_exitoso(client_login_admin):
    """
    Prueba de integración: crea un producto NUEVO sin ventas y lo elimina.
    """
    from appweb.models import Producto
    from appweb.postgres_db import pgdb
    import secrets
    import time
    
    # Usar timestamp para unicidad extrema
    timestamp = int(time.time() * 1000)
    nombre_unico = f"ProdTemp{timestamp}{secrets.token_hex(4)}"
    
    nuevo_producto = Producto(
        nombre=nombre_unico,
        precio=100.0,
        stock=50,
        tipo_descuento="ninguno"
    )
    producto_id = nuevo_producto.insertar()
    
    # Verificar que NO tiene ventas
    with pgdb.get_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM ventas WHERE producto_id = %s", (producto_id,))
        ventas_count = cur.fetchone()[0]
        assert ventas_count == 0
    
    # Eliminar
    response = client_login_admin.get(
        f"/eliminar_producto/{producto_id}",
        follow_redirects=True
    )
    assert response.status_code == 200
    
    # Verificar eliminación
    with pgdb.get_cursor() as cur:
        cur.execute("SELECT id FROM productos WHERE id = %s", (producto_id,))
        assert cur.fetchone() is None


# =========================================================
# PRUEBA: NO ELIMINAR PRODUCTO CON VENTAS ASOCIADAS
# CUBRE: Líneas de eliminar en models.py (ventas_count > 0)
# =========================================================
def test_eliminar_producto_con_ventas(client_login_admin, producto_prueba):
    """
    Prueba de integración: intenta eliminar un producto que YA tiene ventas.
    Debe fallar con DBException.
    """
    from appweb.models import Producto, DBException
    
    producto_obj = Producto.consultar_por_id(producto_prueba)
    
    # Verificar que tiene ventas
    with pgdb.get_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM ventas WHERE producto_id = %s", (producto_prueba,))
        ventas_count = cur.fetchone()[0]
    
    if ventas_count == 0:
        pytest.skip("El producto no tiene ventas asociadas - no se puede probar este caso")
    
    # Intentar eliminar - debe lanzar excepción
    with pytest.raises(DBException, match="No se puede eliminar el producto porque tiene"):
        producto_obj.eliminar()

# ELIMINAR PRODUCTO CON VENTAS ASOCIADAS
# =========================================================
def test_eliminar_producto_con_ventas():
    producto = Producto.consultar_por_id(1)
    
    with pytest.raises(DBException) as error:
        producto.eliminar()
    assert "No se puede eliminar" in str(error.value)


# ELIMINAR PRODUCTO INEXISTENTE
# =========================================================
def test_eliminar_producto_inexistente(client_login_admin):
    response = client_login_admin.get(
        "/eliminar_producto/9999",
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Producto no encontrado" in response.get_data(as_text=True)


# ELIMINAR PRODUCTO DESDE ENDPOINT
# =========================================================
def test_eliminar_producto_endpoint_exitoso(client_login_admin):
    # Crear producto temporal vía endpoint
    response = client_login_admin.post(
        "/agregar_producto",
        data={
            "nombre": "Producto Eliminar",
            "precio": 10.00,
            "stock": 100
        },
        follow_redirects=True
    )
    
    # Obtener ID del producto creado
    productos = Producto.consultar_todo()
    producto_creado = None
    for p in productos:
        if p.nombre == "Producto Eliminar":
            producto_creado = p
            break
    
    if producto_creado:
        response = client_login_admin.get(
            f"/eliminar_producto/{producto_creado.id}",
            follow_redirects=True
        )
        assert response.status_code == 200
        assert "eliminado correctamente" in response.get_data(as_text=True)

# ELIMINAR PRODUCTO SIN PERMISOS
# =========================================================
def test_eliminar_producto_sin_permisos(client_login_vendedor_temporal):
    response = client_login_vendedor_temporal.get("/eliminar_producto/1", follow_redirects=True)
    assert "Acceso denegado" in response.get_data(as_text=True)