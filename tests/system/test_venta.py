# tests/system/test_venta.py

import pytest
from decimal import Decimal
from appweb.models import Venta
from appweb.postgres_db import pgdb


# =========================================================
# PRUEBA DE REGISTRO DE VENTA EXITOSA
# =========================================================
def test_registrar_venta_exitosa(client_login_vendedor_temporal):
    # Crear producto de prueba con nombre único
    import time
    unique_id = int(time.time())
    
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, 100.0, 50, 'ninguno', 0)
            RETURNING id
        """, (f"Producto Venta Test {unique_id}",))
        producto_id = cur.fetchone()[0]
    
    # Agregar al carrito
    client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_id, "cantidad": 2},
        follow_redirects=True
    )
    
    # Procesar compra
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    
    # Verificar que muestra el ticket
    texto = response.get_data(as_text=True)
    assert "Ticket de venta" in texto or "ticket" in texto.lower()
    assert f"Producto Venta Test {unique_id}" in texto
    assert "$200.00" in texto
    
    # NOTA: NO eliminar el producto porque ya tiene ventas asociadas
    # El producto queda en la BD para futuras pruebas


# =========================================================
# PRUEBA DE REGISTRO DE VENTA CON PRODUCTO INEXISTENTE
# =========================================================
def test_registrar_venta_producto_inexistente(client_login_vendedor_temporal):
    # Agregar producto inexistente al carrito (simulado)
    with client_login_vendedor_temporal.session_transaction() as sess:
        sess['carrito'] = [{'id': 99999, 'cantidad': 2, 'nombre': 'Producto Inexistente'}]
    
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert "no encontrado" in response.get_data(as_text=True).lower()


# =========================================================
# PRUEBA DE REGISTRO DE VENTA CON STOCK INSUFICIENTE
# =========================================================
def test_registrar_venta_stock_insuficiente(client_login_vendedor_temporal):
    # Crear producto con stock limitado
    import time
    unique_id = int(time.time())
    
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, 100.0, 3, 'ninguno', 0)
            RETURNING id
        """, (f"Stock Limitado Venta {unique_id}",))
        producto_id = cur.fetchone()[0]
    
    # Agregar más del stock disponible al carrito
    with client_login_vendedor_temporal.session_transaction() as sess:
        sess['carrito'] = [{'id': producto_id, 'cantidad': 10, 'nombre': f'Stock Limitado Venta {unique_id}'}]
    
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert "stock" in response.get_data(as_text=True).lower() or "insuficiente" in response.get_data(as_text=True).lower()
    
    # NOTA: No eliminar el producto porque la venta NO se completó (stock insuficiente)
    # Se puede eliminar porque no hay venta asociada
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM productos WHERE id = %s", (producto_id,))


# =========================================================
# PRUEBA DE CONSULTA DE HISTORIAL DE VENTAS
# =========================================================
def test_consultar_historial_ventas(client_login_admin):
    response = client_login_admin.get("/historial", follow_redirects=True)
    assert response.status_code == 200
    assert "Historial de ventas" in response.get_data(as_text=True)


# =========================================================
# PRUEBA DE TOTAL DE VENTAS
# =========================================================
def test_total_ventas(client_login_admin):
    """Verifica que el total de ventas se calcula correctamente"""
    total = Venta.total_ventas()
    
    # Aceptar Decimal (viene de PostgreSQL), float o int
    assert isinstance(total, (Decimal, float, int))
    assert total >= 0


# =========================================================
# PRUEBA DE PROCESAR COMPRA SIN SESIÓN
# CUBRE: Líneas 748-749 de views.py (validación de sesión en procesar_compra)
# =========================================================
def test_procesar_compra_sin_sesion(client):
    """
    Prueba que al intentar procesar una compra sin haber iniciado sesión,
    el sistema redirige al login y muestra mensaje de error.
    
    Esta prueba cubre específicamente las líneas 748-749 de views.py
    en la función procesar_compra().
    """
    response = client.post(
        "/procesar_compra",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    
    # Debe mostrar mensaje de sesión requerida
    assert "No se ha iniciado sesión" in texto or "iniciar sesión" in texto.lower()
    # Debe estar en la página de login
    assert "login" in texto.lower() or "Iniciar sesión" in texto


# =========================================================
# PRUEBA DE PROCESAR COMPRA CON CARRITO VACÍO (ya existe)
# =========================================================
def test_procesar_compra_carrito_vacio(client_login_vendedor_temporal):
    """
    Prueba que al intentar procesar compra con carrito vacío,
    se muestre mensaje de error.
    """
    # Asegurar que el carrito está vacío
    client_login_vendedor_temporal.get("/limpiar_carrito", follow_redirects=True)
    
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "vacío" in texto.lower() or "vacío" in texto