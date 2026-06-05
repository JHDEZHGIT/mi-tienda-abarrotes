# tests/unit/pe/test_producto_pe.py

import pytest

from appweb.models import (
    Producto,
    NombreProductoException,
    PrecioProductoException,
    StockProductoException
)


# PE NOMBRE VALIDOS
# =========================================================
def test_nombre_pe_validos():
    nombre = "Producto Test"  # T02

    producto = Producto(
        nombre=nombre,
        precio=14.50,
        stock=100
    )
    assert producto.nombre == nombre.strip()


# PE NOMBRE INVALIDOS
# =========================================================
@pytest.mark.parametrize("nombre", [
    "",           # T01
    "   ",        # T04
    1000,         # T05
    True,         # T06
    None,         # T07
    "b" * 256,    # T03
    "Producto@#$",  # T07a
    "Producto;",    # T07b
],
ids=[
    "T01_PE_nombre_vacio",
    "T04_PE_nombre_espacios",
    "T05_PE_nombre_int",
    "T06_PE_nombre_bool",
    "T07_PE_nombre_none",
    "T03_PE_nombre_mayor_255",
    "T07a_PE_nombre_caracteres_especiales",
    "T07b_PE_nombre_punto_coma"
])
def test_nombre_pe_invalidos(nombre):
    with pytest.raises(NombreProductoException) as error:
        Producto(
            nombre=nombre,
            precio=14.50,
            stock=100
        )
    assert isinstance(error.value, NombreProductoException)


# PE PRECIO INVALIDOS
# =========================================================
@pytest.mark.parametrize("precio", [
    None,      # T01
    "",        # T02
    "abc",     # T03
    -10,       # T04
    0,         # T05
    1000000,   # T06
],
ids=[
    "T01_PE_precio_none",
    "T02_PE_precio_vacio",
    "T03_PE_precio_texto",
    "T04_PE_precio_negativo",
    "T05_PE_precio_cero",
    "T06_PE_precio_excede_maximo"
])
def test_precio_pe_invalidos(precio):
    with pytest.raises(PrecioProductoException) as error:
        Producto(
            nombre="Producto Test",
            precio=precio,
            stock=100
        )
    assert isinstance(error.value, PrecioProductoException)


# PE STOCK INVALIDOS
# =========================================================
@pytest.mark.parametrize("stock", [
    None,       # T01
    "abc",      # T02
    -5,         # T03
    1000000,    # T04
],
ids=[
    "T01_PE_stock_none",
    "T02_PE_stock_texto",
    "T03_PE_stock_negativo",
    "T04_PE_stock_excede_maximo"
])
def test_stock_pe_invalidos(stock):
    with pytest.raises(StockProductoException) as error:
        Producto(
            nombre="Producto Test",
            precio=14.50,
            stock=stock
        )
    assert isinstance(error.value, StockProductoException)