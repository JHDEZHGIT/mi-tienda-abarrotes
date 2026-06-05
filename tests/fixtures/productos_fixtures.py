# tests/fixtures/productos_fixtures.py
"""
Fixtures para crear productos de prueba en la base de datos
"""

import pytest
from appweb.models import pgdb


@pytest.fixture
def producto_prueba():
    """Fixture que crea un producto temporal y lo limpia después"""
    producto_id = None
    
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES ('Producto Test', 100.0, 50, 'ninguno', 0)
            RETURNING id
        """)
        producto_id = cur.fetchone()[0]
    
    yield producto_id
    
    # Limpiar después de la prueba
    if producto_id:
        with pgdb.get_cursor() as cur:
            cur.execute("DELETE FROM productos WHERE id = %s", (producto_id,))


@pytest.fixture
def producto_con_descuento():
    """Fixture que crea un producto con descuento porcentual"""
    producto_id = None
    
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES ('Producto Descuento', 100.0, 50, 'porcentaje', 10)
            RETURNING id
        """)
        producto_id = cur.fetchone()[0]
    
    yield producto_id
    
    if producto_id:
        with pgdb.get_cursor() as cur:
            cur.execute("DELETE FROM productos WHERE id = %s", (producto_id,))


@pytest.fixture
def producto_2x1():
    """Fixture que crea un producto con promoción 2x1"""
    producto_id = None
    
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES ('Producto 2x1', 50.0, 20, '2x1', 0)
            RETURNING id
        """)
        producto_id = cur.fetchone()[0]
    
    yield producto_id
    
    if producto_id:
        with pgdb.get_cursor() as cur:
            cur.execute("DELETE FROM productos WHERE id = %s", (producto_id,))


@pytest.fixture
def producto_stock_limite():
    """Fixture que crea un producto con stock limitado"""
    producto_id = None
    
    with pgdb.get_cursor() as cur:
        cur.execute("""
            INSERT INTO productos (nombre, precio, stock, tipo_descuento, descuento_valor)
            VALUES ('Stock Limitado', 100.0, 5, 'ninguno', 0)
            RETURNING id
        """)
        producto_id = cur.fetchone()[0]
    
    yield producto_id
    
    if producto_id:
        with pgdb.get_cursor() as cur:
            cur.execute("DELETE FROM productos WHERE id = %s", (producto_id,))