# tests/unit/test_VL/test_descuento_vl.py

import pytest

from appweb.descuentos import CalculadorDescuento
from tests.helpers.descuentos_helper import (
    datos_cantidad_limite,
    datos_precio_limite,
    datos_porcentaje_limite,
    datos_promocion_2x1_vl,
    datos_promocion_3x2_vl,
    datos_promocion_4x3_vl,
    datos_promocion_5x4_vl,
    datos_tipos_descuento_validos,
    datos_descripciones,
)


# =========================================================
# VALORES LIMITE - CANTIDAD
# =========================================================

@pytest.mark.parametrize("cantidad,esperado,debe_fallar", datos_cantidad_limite())
def test_cantidad_limite(cantidad, esperado, debe_fallar):
    if debe_fallar:
        with pytest.raises(ValueError):
            CalculadorDescuento.calcular_total("ninguno", 0, cantidad, 10.00)
    else:
        total = CalculadorDescuento.calcular_total("ninguno", 0, cantidad, 10.00)
        assert total == esperado


# =========================================================
# VALORES LIMITE - PRECIO UNITARIO
# =========================================================

@pytest.mark.parametrize("precio,esperado,debe_fallar", datos_precio_limite())
def test_precio_limite(precio, esperado, debe_fallar):
    if debe_fallar:
        with pytest.raises(ValueError):
            CalculadorDescuento.calcular_total("ninguno", 0, 5, precio)
    else:
        total = CalculadorDescuento.calcular_total("ninguno", 0, 5, precio)
        assert total == esperado


# =========================================================
# VALORES LIMITE - PORCENTAJE
# =========================================================

@pytest.mark.parametrize("porcentaje,esperado,debe_fallar", datos_porcentaje_limite())
def test_porcentaje_limite(porcentaje, esperado, debe_fallar):
    if debe_fallar:
        with pytest.raises(ValueError):
            CalculadorDescuento.calcular_total("porcentaje", porcentaje, 1, 100.00)
    else:
        total = CalculadorDescuento.calcular_total("porcentaje", porcentaje, 1, 100.00)
        assert total == esperado


# =========================================================
# VALORES LIMITE - PROMOCION 2X1
# =========================================================

@pytest.mark.parametrize("cantidad,esperado", datos_promocion_2x1_vl())
def test_promocion_2x1_limite(cantidad, esperado):
    total = CalculadorDescuento.calcular_total("2x1", 0, cantidad, 10.00)
    assert total == esperado


# =========================================================
# VALORES LIMITE - PROMOCION 3X2
# =========================================================

@pytest.mark.parametrize("cantidad,esperado", datos_promocion_3x2_vl())
def test_promocion_3x2_limite(cantidad, esperado):
    total = CalculadorDescuento.calcular_total("3x2", 0, cantidad, 10.00)
    assert total == esperado


# =========================================================
# VALORES LIMITE - PROMOCION 4X3
# =========================================================

@pytest.mark.parametrize("cantidad,esperado", datos_promocion_4x3_vl())
def test_promocion_4x3_limite(cantidad, esperado):
    total = CalculadorDescuento.calcular_total("4x3", 0, cantidad, 10.00)
    assert total == esperado


# =========================================================
# VALORES LIMITE - PROMOCION 5X4
# =========================================================

@pytest.mark.parametrize("cantidad,esperado", datos_promocion_5x4_vl())
def test_promocion_5x4_limite(cantidad, esperado):
    total = CalculadorDescuento.calcular_total("5x4", 0, cantidad, 10.00)
    assert total == esperado


# =========================================================
# VALORES LIMITE - TIPOS DE DESCUENTO VALIDOS
# =========================================================

@pytest.mark.parametrize("tipo,valor,cantidad,precio,esperado", datos_tipos_descuento_validos())
def test_tipo_descuento_limite(tipo, valor, cantidad, precio, esperado):
    total = CalculadorDescuento.calcular_total(tipo, valor, cantidad, precio)
    assert total == esperado


# =========================================================
# VALORES LIMITE - TIPOS DE DESCUENTO INVALIDOS
# =========================================================

def test_tipo_descuento_vacio():
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("", 0, 5, 10.00)


def test_tipo_descuento_invalido():
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("invalido", 0, 5, 10.00)


# =========================================================
# VALORES LIMITE - DESCRIPCIONES
# =========================================================

@pytest.mark.parametrize("tipo,valor,esperado", datos_descripciones())
def test_descripcion_limite(tipo, valor, esperado):
    desc = CalculadorDescuento.obtener_descripcion(tipo, valor)
    assert desc == esperado