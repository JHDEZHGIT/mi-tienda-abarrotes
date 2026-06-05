# tests/unit/test_VL/test_producto_vl.py

import pytest

from appweb.models import (
    Producto,
    NombreProductoException,
    PrecioProductoException,
    StockProductoException
)


# =========================================================
# VALORES LIMITE - NOMBRE
# =========================================================

@pytest.mark.parametrize("nombre,valido,longitud_esperada", [
    ("", False, None),           # Justo debajo (0)
    ("a", True, 1),              # Límite inferior (1)
    ("ab", True, 2),             # Justo arriba (2)
    ("a" * 254, True, 254),      # Justo debajo (254)
    ("a" * 255, True, 255),      # Límite superior (255)
    ("a" * 256, False, None),    # Justo arriba (256)
])
def test_nombre_vl(nombre, valido, longitud_esperada):
    if valido:
        producto = Producto(nombre=nombre, precio=10.00, stock=10)
        assert len(producto.nombre) == longitud_esperada
    else:
        with pytest.raises(NombreProductoException):
            Producto(nombre=nombre, precio=10.00, stock=10)


# =========================================================
# VALORES LIMITE - PRECIO
# =========================================================

@pytest.mark.parametrize("precio,valido,esperado", [
    (-0.01, False, None),        # Negativo
    (0, False, None),            # Cero
    (0.009, True, 0.01),         # Se redondea a 0.01
    (0.01, True, 0.01),          # Límite inferior
    (0.02, True, 0.02),          # Justo arriba
    (999999.98, True, 999999.98), # Justo debajo
    (999999.99, True, 999999.99), # Límite superior
    (1000000.00, False, None),   # Justo arriba
])
def test_precio_vl(precio, valido, esperado):
    if valido:
        producto = Producto(nombre="Test", precio=precio, stock=10)
        assert producto.precio == esperado
    else:
        with pytest.raises(PrecioProductoException):
            Producto(nombre="Test", precio=precio, stock=10)


# =========================================================
# VALORES LIMITE - STOCK
# =========================================================

@pytest.mark.parametrize("stock,valido,esperado", [
    (-1, False, None),           # Negativo
    (0, True, 0),                # Límite inferior
    (1, True, 1),                # Justo arriba
    (999998, True, 999998),      # Justo debajo
    (999999, True, 999999),      # Límite superior
    (1000000, False, None),      # Justo arriba
])
def test_stock_vl(stock, valido, esperado):
    if valido:
        producto = Producto(nombre="Test", precio=10.00, stock=stock)
        assert producto.stock == esperado
    else:
        with pytest.raises(StockProductoException):
            Producto(nombre="Test", precio=10.00, stock=stock)