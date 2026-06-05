# tests/system/test_producto_eliminar.py

import pytest

from appweb.models import Producto, DBException


# ELIMINAR PRODUCTO EXITOSO
# =========================================================
def test_eliminar_producto_exitoso():
    # Crear producto temporal
    nuevo_producto = Producto(
        nombre="Producto Temporal",
        precio=10.00,
        stock=100
    )
    nuevo_producto.insertar()
    producto_id = nuevo_producto.id
    
    # Eliminar producto
    producto = Producto.consultar_por_id(producto_id)
    producto.eliminar()
    
    # Verificar eliminado
    producto_eliminado = Producto.consultar_por_id(producto_id)
    assert producto_eliminado is None


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