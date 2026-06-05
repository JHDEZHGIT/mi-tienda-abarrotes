# tests/system/test_ticket.py

import pytest
from appweb.models import Venta
from appweb.postgres_db import pgdb


# TICKET VENTA EXISTENTE - CORREGIDO
# =========================================================
def test_ticket_venta_existente(client_login_vendedor_temporal):
    # Crear una venta específica para la prueba
    import time
    unique_id = int(time.time())
    
    # Crear producto
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, 100.0, 50, 'ninguno', 0)
            RETURNING id
        """, (f"Producto Ticket Test {unique_id}",))
        producto_id = cur.fetchone()[0]
    
    # Agregar al carrito
    client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_id, "cantidad": 2},
        follow_redirects=True
    )
    
    # Procesar compra (esto redirige al ticket)
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Ticket de venta" in texto
    assert f"Producto Ticket Test {unique_id}" in texto
    assert "$200.00" in texto


# TICKET VENTA INEXISTENTE - CORREGIDO
# =========================================================
def test_ticket_venta_inexistente(client_login_admin):
    # Usar admin que siempre existe
    response = client_login_admin.get(
        "/ticket/99999",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Venta no encontrada" in texto or "no encontrada" in texto.lower()


# TICKET REQUIERE AUTENTICACION
# =========================================================
def test_ticket_sin_autenticacion(client):
    response = client.get("/ticket/1", follow_redirects=True)
    assert response.status_code == 200
    assert "No se ha iniciado sesión" in response.get_data(as_text=True)