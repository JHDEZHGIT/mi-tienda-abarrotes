# tests/system/test_carrito.py

import pytest


# AGREGAR PRODUCTO AL CARRITO
# =========================================================
def test_agregar_carrito_exitoso(client_login_vendedor_temporal, producto_prueba):
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_prueba, "cantidad": 2},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Agregado" in response.get_data(as_text=True)


# AGREGAR PRODUCTO AL CARRITO CANTIDAD CERO
# =========================================================
def test_agregar_carrito_cantidad_cero(client_login_vendedor_temporal, producto_prueba):
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_prueba, "cantidad": 0},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "La cantidad debe ser mayor que cero" in response.get_data(as_text=True)


# AGREGAR PRODUCTO AL CARRITO CANTIDAD NEGATIVA
# =========================================================
def test_agregar_carrito_cantidad_negativa(client_login_vendedor_temporal, producto_prueba):
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_prueba, "cantidad": -5},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "La cantidad debe ser mayor que cero" in response.get_data(as_text=True)


# AGREGAR PRODUCTO AL CARRITO PRODUCTO INEXISTENTE
# =========================================================
def test_agregar_carrito_producto_inexistente(client_login_vendedor_temporal):
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": 99999, "cantidad": 1},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Producto no encontrado" in response.get_data(as_text=True)


# AGREGAR PRODUCTO AL CARRITO SIN SESION
# =========================================================
def test_agregar_carrito_sin_sesion(client):
    response = client.post(
        "/agregar_carrito",
        data={"producto_id": 1, "cantidad": 1},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "No se ha iniciado sesión" in response.get_data(as_text=True)


# AGREGAR MISMO PRODUCTO MULTIPLES VECES (ACUMULA)
# =========================================================
def test_agregar_carrito_mismo_producto_acumula(client_login_vendedor_temporal, producto_prueba):
    # Primera adición
    client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_prueba, "cantidad": 2},
        follow_redirects=True
    )
    
    # Segunda adición del mismo producto
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_prueba, "cantidad": 3},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Total en carrito: 5" in response.get_data(as_text=True)


# AGREGAR PRODUCTO CON DESCUENTO
# =========================================================
def test_agregar_carrito_con_descuento(client_login_vendedor_temporal, producto_con_descuento):
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_con_descuento, "cantidad": 2},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Agregado" in response.get_data(as_text=True)


# AGREGAR PRODUCTO CON PROMOCION 2X1
# =========================================================
def test_agregar_carrito_promocion_2x1(client_login_vendedor_temporal, producto_2x1):
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_2x1, "cantidad": 3},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Agregado" in response.get_data(as_text=True)


# AGREGAR PRODUCTO STOCK INSUFICIENTE
# =========================================================
def test_agregar_carrito_stock_insuficiente(client_login_vendedor_temporal, producto_stock_limite):
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_stock_limite, "cantidad": 10},
        follow_redirects=True
    )
    assert response.status_code == 200
    response_text = response.get_data(as_text=True)
    assert ("stock" in response_text.lower() or 
            "solo puedes" in response_text.lower() or
            "disponible" in response_text.lower())