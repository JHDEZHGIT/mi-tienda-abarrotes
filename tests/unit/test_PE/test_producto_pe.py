# tests/unit/pe/test_producto_pe.py

import pytest
import secrets

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

# =========================================================
# PRUEBA 27: CONSULTAR PRODUCTO POR NOMBRE EXACTO
# CUBRE: Líneas de Producto.consultar_por_nombre (models.py)
# =========================================================
def test_consultar_producto_por_nombre_exacto(producto_prueba):
    """
    Prueba de partición de equivalencia: busca un producto por nombre exacto.
    """
    from appweb.models import Producto
    
    producto_obj = Producto.consultar_por_id(producto_prueba)
    resultado = Producto.consultar_por_nombre(producto_obj.nombre)
    
    assert len(resultado) >= 1
    assert resultado[0].nombre == producto_obj.nombre


# =========================================================
# PRUEBA 28: CONSULTAR PRODUCTO POR NOMBRE PARCIAL
# CUBRE: Líneas de Producto.consultar_por_nombre (models.py)
# =========================================================
def test_consultar_producto_por_nombre_parcial(producto_prueba):
    """
    Prueba de partición de equivalencia: busca productos por nombre parcial.
    """
    from appweb.models import Producto
    
    producto_obj = Producto.consultar_por_id(producto_prueba)
    nombre_parcial = producto_obj.nombre[:3]
    resultado = Producto.consultar_por_nombre(nombre_parcial)
    
    assert len(resultado) >= 1


# =========================================================
# PRUEBA 29: CONSULTAR PRODUCTO POR NOMBRE INEXISTENTE
# CUBRE: Líneas de Producto.consultar_por_nombre (models.py)
# =========================================================
def test_consultar_producto_por_nombre_inexistente():
    """
    Prueba de valores límite: busca un nombre que no existe en la BD.
    """
    from appweb.models import Producto
    
    nombre_inexistente = f"PRODUCTO_INEXISTENTE_{secrets.token_hex(8)}"
    resultado = Producto.consultar_por_nombre(nombre_inexistente)
    
    assert resultado == []


# PRUEBA 32: OBTENER DESCRIPCIÓN DE PRODUCTO SIN DESCUENTO
# CUBRE: Líneas de Producto.obtener_descripcion_descuento (models.py)
# =========================================================
def test_obtener_descripcion_descuento_ninguno(producto_prueba):
    """
    Prueba de partición de equivalencia: producto sin descuento.
    NOTA: producto_prueba es un ID, hay que consultar el objeto primero.
    """
    from appweb.models import Producto
    
    # Obtener el objeto Producto desde el ID
    producto = Producto.consultar_por_id(producto_prueba)
    
    producto.tipo_descuento = "ninguno"
    producto.valor_descuento = 0
    descripcion = producto.obtener_descripcion_descuento()
    assert descripcion == "Sin descuento"


# =========================================================
# PRUEBA 33: OBTENER DESCRIPCIÓN DE PRODUCTO CON PORCENTAJE
# CUBRE: Líneas de Producto.obtener_descripcion_descuento (models.py)
# =========================================================
def test_obtener_descripcion_descuento_porcentaje(producto_con_descuento):
    """
    Prueba de partición de equivalencia: producto con descuento porcentual.
    """
    from appweb.models import Producto
    
    producto = Producto.consultar_por_id(producto_con_descuento)
    descripcion = producto.obtener_descripcion_descuento()
    assert "% de descuento" in descripcion


# =========================================================
# PRUEBA 34: OBTENER DESCRIPCIÓN DE PRODUCTO CON PROMOCIÓN 2X1
# CUBRE: Líneas de Producto.obtener_descripcion_descuento (models.py)
# =========================================================
def test_obtener_descripcion_descuento_2x1(producto_2x1):
    """
    Prueba de partición de equivalencia: producto con promoción 2x1.
    """
    from appweb.models import Producto
    
    producto = Producto.consultar_por_id(producto_2x1)
    descripcion = producto.obtener_descripcion_descuento()
    assert "2x1" in descripcion or "paga 1" in descripcion