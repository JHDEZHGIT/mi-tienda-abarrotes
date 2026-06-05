# tests/system/test_flujo_venta.py

import pytest
from appweb.postgres_db import pgdb


# =========================================================
# FLUJO VENTA COMPLETO
# =========================================================
def test_flujo_venta_completo(client_login_vendedor_temporal):
    import time
    unique_id = int(time.time())
    
    # Crear producto de prueba
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, 100.0, 50, 'ninguno', 0)
            RETURNING id
        """, (f"Producto Flujo {unique_id}",))
        producto_id = cur.fetchone()[0]
    
    # 1. Agregar producto al carrito
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_id, "cantidad": 2},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Agregado" in response.get_data(as_text=True)

    # 2. Ver carrito
    response = client_login_vendedor_temporal.get("/carrito", follow_redirects=True)
    assert response.status_code == 200
    assert "Carrito de compras" in response.get_data(as_text=True)

    # 3. Procesar compra
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Ticket de venta" in texto or "ticket" in texto.lower()


# =========================================================
# FLUJO VENTA CARRITO VACIO
# =========================================================
def test_flujo_venta_carrito_vacio(client_login_vendedor_temporal):
    # Asegurar que el carrito está vacío
    client_login_vendedor_temporal.get("/limpiar_carrito", follow_redirects=True)
    
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "vacío" in texto.lower() or "vacío" in texto


# =========================================================
# FLUJO VENTA AGREGAR MULTIPLES PRODUCTOS
# =========================================================
def test_flujo_venta_agregar_multiples(client_login_vendedor_temporal):
    import time
    unique_id = int(time.time())
    
    # Crear dos productos de prueba
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, 100.0, 50, 'ninguno', 0)
            RETURNING id
        """, (f"Producto Multi A {unique_id}",))
        producto1_id = cur.fetchone()[0]
        
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, 50.0, 30, 'ninguno', 0)
            RETURNING id
        """, (f"Producto Multi B {unique_id}",))
        producto2_id = cur.fetchone()[0]
    
    # Agregar primer producto
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto1_id, "cantidad": 1},
        follow_redirects=True
    )
    assert response.status_code == 200

    # Agregar segundo producto
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto2_id, "cantidad": 3},
        follow_redirects=True
    )
    assert response.status_code == 200

    # Verificar carrito
    response = client_login_vendedor_temporal.get("/carrito", follow_redirects=True)
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Carrito de compras" in texto
    assert f"Producto Multi A {unique_id}" in texto
    assert f"Producto Multi B {unique_id}" in texto


# =========================================================
# FLUJO VENTA LIMPIAR CARRITO
# =========================================================
def test_flujo_venta_limpiar_carrito(client_login_vendedor_temporal):
    import time
    unique_id = int(time.time())
    
    # Crear producto de prueba
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, 100.0, 50, 'ninguno', 0)
            RETURNING id
        """, (f"Producto Limpiar {unique_id}",))
        producto_id = cur.fetchone()[0]
    
    # Agregar producto
    client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_id, "cantidad": 2},
        follow_redirects=True
    )

    # Limpiar carrito
    response = client_login_vendedor_temporal.get("/limpiar_carrito", follow_redirects=True)
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Carrito vaciado" in texto or "vaciado" in texto.lower()

    # Verificar carrito vacío
    response = client_login_vendedor_temporal.get("/carrito", follow_redirects=True)
    texto = response.get_data(as_text=True)
    assert "Carrito de compras" in texto
    # El producto no debería aparecer
    assert f"Producto Limpiar {unique_id}" not in texto