# tests/helpers/carrito_helper.py

"""
Helpers para pruebas de carrito
"""

import time
from appweb.postgres_db import pgdb


def crear_producto_carrito(nombre=None, precio=100.0, stock=10):
    """Crea un producto temporal para pruebas de carrito"""
    unique_id = int(time.time())
    nombre_real = nombre or f"Producto Carrito {unique_id}"
    
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES (%s, %s, %s, 'ninguno', 0)
            RETURNING id
        """, (nombre_real, precio, stock))
        producto_id = cur.fetchone()[0]
    
    return producto_id, nombre_real


def limpiar_producto_carrito(producto_id):
    """Elimina un producto de prueba"""
    if producto_id:
        with pgdb.get_cursor() as cur:
            cur.execute("DELETE FROM productos WHERE id = %s", (producto_id,))