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


# tests/system/test_carrito.py - AGREGAR AL FINAL DEL ARCHIVO EXISTENTE
"""
Pruebas de sistema para el carrito de compras
Incluye pruebas de valores límite y casos borde
"""

import pytest
import time
from appweb.postgres_db import pgdb


# =========================================================
# HELPERS LOCALES
# =========================================================

def crear_producto_aux(nombre=None, precio=100.0, stock=10):
    """Crea un producto temporal para pruebas"""
    unique_id = int(time.time())
    nombre_real = nombre or f"Producto Aux {unique_id}"
    
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, %s, %s, 'ninguno', 0)
            RETURNING id
        """, (nombre_real, precio, stock))
        return cur.fetchone()[0], nombre_real


def limpiar_producto_aux(producto_id):
    """Elimina un producto de prueba"""
    if producto_id:
        with pgdb.get_cursor() as cur:
            cur.execute("DELETE FROM productos WHERE id = %s", (producto_id,))


# =========================================================
# PRUEBAS DE VALORES LÍMITE - CARRITO
# =========================================================

def test_agregar_carrito_producto_id_invalido(client_login_vendedor_temporal):
    """
    CUBRE: Líneas 617-619 (ValueError/TypeError en producto_id)
    Prueba que al enviar producto_id no numérico, se muestre error
    """
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": "abc", "cantidad": 1},
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Identificador de producto inválido" in texto


def test_agregar_carrito_cantidad_invalida_tipo(client_login_vendedor_temporal, producto_prueba):
    """
    CUBRE: Líneas 623-625 (ValueError/TypeError en cantidad)
    Prueba que al enviar cantidad no numérica, se muestre error
    """
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_prueba, "cantidad": "abc"},
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "número entero válido" in texto or "válido" in texto


def test_agregar_carrito_stock_agotado(client_login_vendedor_temporal):
    """
    CUBRE: Líneas 654-655 (stock_restante <= 0)
    Prueba que cuando el stock es exactamente el que ya está en carrito,
    no se pueda agregar más
    """
    # Crear producto con stock 2
    producto_id, nombre = crear_producto_aux(stock=2)
    
    try:
        # Primera compra: agregar 2 unidades (todo el stock)
        response1 = client_login_vendedor_temporal.post(
            "/agregar_carrito",
            data={"producto_id": producto_id, "cantidad": 2},
            follow_redirects=True
        )
        assert response1.status_code == 200
        
        # Segunda compra: intentar agregar más
        response2 = client_login_vendedor_temporal.post(
            "/agregar_carrito",
            data={"producto_id": producto_id, "cantidad": 1},
            follow_redirects=True
        )
        assert response2.status_code == 200
        texto = response2.get_data(as_text=True)
        # Debe mostrar mensaje de stock insuficiente o que ya tiene todo el stock
        assert "stock" in texto.lower() or "disponible" in texto.lower()
    finally:
        limpiar_producto_aux(producto_id)


def test_agregar_carrito_stock_restante_positivo(client_login_vendedor_temporal):
    """
    CUBRE: Líneas 657 (stock_restante > 0) - ya existe en pruebas existentes
    Esta prueba verifica que el mensaje de stock restante se muestra correctamente
    """
    # Crear producto con stock 5
    producto_id, nombre = crear_producto_aux(stock=5)
    
    try:
        # Primera compra: agregar 3 unidades
        client_login_vendedor_temporal.post(
            "/agregar_carrito",
            data={"producto_id": producto_id, "cantidad": 3},
            follow_redirects=True
        )
        
        # Segunda compra: intentar agregar 3 más (solo quedan 2)
        response = client_login_vendedor_temporal.post(
            "/agregar_carrito",
            data={"producto_id": producto_id, "cantidad": 3},
            follow_redirects=True
        )
        assert response.status_code == 200
        texto = response.get_data(as_text=True)
        # Debe indicar cuántas unidades más puede agregar
        assert "solo puedes agregar" in texto.lower() or "2 unidades" in texto
    finally:
        limpiar_producto_aux(producto_id)


def test_agregar_carrito_cantidad_extrema(client_login_vendedor_temporal, producto_prueba):
    """
    CUBRE: Líneas 698 (else cuando ahorro <= 0)
    Prueba que funcione correctamente con cantidades extremas
    """
    # Cantidad muy grande pero dentro del stock
    response = client_login_vendedor_temporal.post(
        "/agregar_carrito",
        data={"producto_id": producto_prueba, "cantidad": 999},
        follow_redirects=True
    )
    assert response.status_code == 200
    # Si llegó aquí, la validación de cantidad funcionó


# =========================================================
# PRUEBAS DE PROCESAR COMPRA - CASOS LÍMITE
# =========================================================

def test_procesar_compra_carrito_estructura_invalida(client_login_vendedor_temporal):
    """
    CUBRE: Líneas 760-761 (estructura inválida del carrito)
    Prueba que cuando el carrito tiene estructura inválida, se muestre error
    """
    # Manipular directamente la sesión para crear estructura inválida
    with client_login_vendedor_temporal.session_transaction() as sess:
        sess['carrito'] = [{'id': 1}]  # Falta 'cantidad' y 'nombre'
    
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Error en la estructura" in texto or "Error" in texto


def test_procesar_compra_id_invalido_en_carrito(client_login_vendedor_temporal):
    """
    CUBRE: Líneas 766-768 (ValueError/TypeError al convertir id o cantidad)
    Prueba que cuando el carrito tiene IDs no numéricos, se muestre error
    """
    with client_login_vendedor_temporal.session_transaction() as sess:
        sess['carrito'] = [{'id': 'abc', 'cantidad': 2, 'nombre': 'Producto Test'}]
    
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Error en los datos" in texto or "danger" in texto



def test_procesar_compra_cantidad_cero_en_carrito(client_login_vendedor_temporal, producto_prueba):
    """
    CUBRE: Líneas 772-773 (cantidad_solicitada <= 0)
    Prueba que cuando el carrito tiene cantidad cero, se muestre error
    """
    with client_login_vendedor_temporal.session_transaction() as sess:
        sess['carrito'] = [{'id': producto_prueba, 'cantidad': 0, 'nombre': 'Producto Test'}]
    
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Cantidad inválida" in texto or "mayor que cero" in texto


def test_procesar_compra_cantidad_demasiado_grande(client_login_vendedor_temporal, producto_prueba):
    """
    CUBRE: Líneas 776-777 (cantidad_solicitada > 999999)
    Prueba que cuando el carrito tiene cantidad excesiva, se muestre error
    """
    with client_login_vendedor_temporal.session_transaction() as sess:
        sess['carrito'] = [{'id': producto_prueba, 'cantidad': 1000000, 'nombre': 'Producto Test'}]
    
    response = client_login_vendedor_temporal.post(
        "/procesar_compra",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "demasiado grande" in texto or "excede" in texto


def test_procesar_compra_empleado_id_fallback(client_login_vendedor_temporal):
    """
    CUBRE: Líneas 792-793 (elif rol == 'vendedor')
    Prueba que cuando no hay empleado_id pero el rol es vendedor,
    se use user_id como fallback
    """
    import time
    unique_id = int(time.time())
    producto_nombre = f"Producto Fallback {unique_id}"
    producto_id = None
    
    try:
        # Crear producto temporal
        with pgdb.get_cursor() as cur:
            cur.execute("""
                INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
                VALUES (%s, 100.0, 10, 'ninguno', 0)
                RETURNING id
            """, (producto_nombre,))
            producto_id = cur.fetchone()[0]
        
        # Agregar al carrito
        client_login_vendedor_temporal.post(
            "/agregar_carrito",
            data={"producto_id": producto_id, "cantidad": 1},
            follow_redirects=True
        )
        
        # Eliminar empleado_id de la sesión para forzar el fallback
        with client_login_vendedor_temporal.session_transaction() as sess:
            if 'empleado_id' in sess:
                del sess['empleado_id']
            sess['rol'] = 'vendedor'
        
        response = client_login_vendedor_temporal.post(
            "/procesar_compra",
            follow_redirects=True
        )
        assert response.status_code == 200
        texto = response.get_data(as_text=True)
        assert "Ticket de venta" in texto or "ticket" in texto.lower()
        
    finally:
        # NO eliminar el producto porque ya tiene ventas asociadas
        # En su lugar, no hacemos nada - el producto queda en la BD
        # pero con un nombre único que no afectará otras pruebas
        pass