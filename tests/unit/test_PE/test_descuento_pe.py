# tests/unit/test_PE/test_descuento_pe.py

import pytest

from appweb.descuentos import CalculadorDescuento


# =========================================================
# PARTICION DE EQUIVALENCIA - TIPO DESCUENTO
# =========================================================

def test_tipo_descuento_pe_valido_ninguno():
    total = CalculadorDescuento.calcular_total("ninguno", 0, 5, 10.00)
    assert total == 50.00


def test_tipo_descuento_pe_valido_porcentaje():
    # El porcentaje debe ser al menos 5 según la validación
    total = CalculadorDescuento.calcular_total("porcentaje", 5, 1, 100.00)
    assert total == 95.00


def test_tipo_descuento_pe_valido_2x1():
    total = CalculadorDescuento.calcular_total("2x1", 0, 2, 10.00)
    assert total == 10.00


def test_tipo_descuento_pe_valido_3x2():
    total = CalculadorDescuento.calcular_total("3x2", 0, 3, 10.00)
    assert total == 20.00


def test_tipo_descuento_pe_valido_4x3():
    total = CalculadorDescuento.calcular_total("4x3", 0, 4, 10.00)
    assert total == 30.00


def test_tipo_descuento_pe_valido_5x4():
    total = CalculadorDescuento.calcular_total("5x4", 0, 5, 10.00)
    assert total == 40.00


@pytest.mark.parametrize("tipo", [
    None,
    "",
    "descuento_invalido",
    "2X1",
    "PROMOCION",
    123,
    True,
])
def test_tipo_descuento_pe_invalidos(tipo):
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total(tipo, 0, 5, 10.00)


# =========================================================
# PARTICION DE EQUIVALENCIA - VALOR DESCUENTO (PORCENTAJE)
# =========================================================

# Valores válidos para porcentaje: 5, 10, 15... 90
@pytest.mark.parametrize("valor", [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90])
def test_valor_descuento_porcentaje_pe_validos(valor):
    total = CalculadorDescuento.calcular_total("porcentaje", valor, 1, 100.00)
    esperado = 100.00 - (100.00 * valor / 100)
    assert total == esperado


# Valores inválidos para porcentaje
@pytest.mark.parametrize("valor", [
    -1,
    -10,
    0,      # 0% no está en la lista de válidos
    1,
    2,
    3,
    4,
    95,
    100,
    101,
    200,
    None,
    "abc",
    "50%",
    True,
])
def test_valor_descuento_porcentaje_pe_invalidos(valor):
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("porcentaje", valor, 5, 10.00)


# =========================================================
# PARTICION DE EQUIVALENCIA - CANTIDAD
# =========================================================

def test_cantidad_pe_valida():
    total = CalculadorDescuento.calcular_total("ninguno", 0, 5, 10.00)
    assert total == 50.00


@pytest.mark.parametrize("cantidad", [
    -1,
    -5,
    None,
    "abc",
    [],
    {},
])
def test_cantidad_pe_invalidos(cantidad):
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("ninguno", 0, cantidad, 10.00)


def test_cantidad_pe_booleano():
    """Booleano True se convierte a 1 (válido)"""
    total = CalculadorDescuento.calcular_total("ninguno", 0, True, 10.00)
    assert total == 10.00


# =========================================================
# PARTICION DE EQUIVALENCIA - PRECIO UNITARIO
# =========================================================

def test_precio_unitario_pe_valido():
    total = CalculadorDescuento.calcular_total("ninguno", 0, 5, 10.00)
    assert total == 50.00


@pytest.mark.parametrize("precio", [
    -0.01,
    -1.00,
    None,
    "abc",
    [],
    {},
])
def test_precio_unitario_pe_invalidos(precio):
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("ninguno", 0, 5, precio)


def test_precio_unitario_pe_booleano():
    """Booleano True se convierte a 1.0 (válido)"""
    total = CalculadorDescuento.calcular_total("ninguno", 0, 5, True)
    assert total == 5.0


# =========================================================
# PARTICION DE EQUIVALENCIA - CALCULOS ESPECIFICOS
# =========================================================

@pytest.mark.parametrize("cantidad,precio,esperado", [
    (1, 10, 10.00),
    (2, 10, 10.00),
    (3, 10, 20.00),
    (4, 10, 20.00),
    (5, 10, 30.00),
    (6, 10, 30.00),
])
def test_calculo_2x1_pe(cantidad, precio, esperado):
    total = CalculadorDescuento.calcular_total("2x1", 0, cantidad, precio)
    assert total == esperado


@pytest.mark.parametrize("cantidad,precio,esperado", [
    (1, 10, 10.00),
    (2, 10, 20.00),
    (3, 10, 20.00),
    (4, 10, 30.00),
    (5, 10, 40.00),
    (6, 10, 40.00),
])
def test_calculo_3x2_pe(cantidad, precio, esperado):
    total = CalculadorDescuento.calcular_total("3x2", 0, cantidad, precio)
    assert total == esperado


@pytest.mark.parametrize("cantidad,precio,esperado", [
    (1, 10, 10.00),
    (2, 10, 20.00),
    (3, 10, 30.00),
    (4, 10, 30.00),
    (5, 10, 40.00),
    (6, 10, 50.00),
    (7, 10, 60.00),
    (8, 10, 60.00),
])
def test_calculo_4x3_pe(cantidad, precio, esperado):
    total = CalculadorDescuento.calcular_total("4x3", 0, cantidad, precio)
    assert total == esperado


@pytest.mark.parametrize("cantidad,precio,esperado", [
    (1, 10, 10.00),
    (2, 10, 20.00),
    (3, 10, 30.00),
    (4, 10, 40.00),
    (5, 10, 40.00),
    (6, 10, 50.00),
    (7, 10, 60.00),
    (8, 10, 70.00),
    (9, 10, 80.00),
    (10, 10, 80.00),
])
def test_calculo_5x4_pe(cantidad, precio, esperado):
    total = CalculadorDescuento.calcular_total("5x4", 0, cantidad, precio)
    assert total == esperado


@pytest.mark.parametrize("porcentaje,cantidad,precio,esperado", [
    (10, 1, 100, 90.00),
    (20, 2, 50, 80.00),
    (15, 3, 100, 255.00),
    (5, 5, 20, 95.00),
    (50, 1, 1000, 500.00),
])
def test_calculo_porcentaje_pe(porcentaje, cantidad, precio, esperado):
    total = CalculadorDescuento.calcular_total("porcentaje", porcentaje, cantidad, precio)
    assert total == esperado


# =========================================================
# PARTICION DE EQUIVALENCIA - OBTENER DESCRIPCION
# =========================================================

def test_obtener_descripcion_pe_ninguno():
    descripcion = CalculadorDescuento.obtener_descripcion("ninguno", 0)
    assert descripcion == "Sin descuento"


def test_obtener_descripcion_pe_porcentaje():
    descripcion = CalculadorDescuento.obtener_descripcion("porcentaje", 20)
    assert descripcion == "20% de descuento"


def test_obtener_descripcion_pe_2x1():
    descripcion = CalculadorDescuento.obtener_descripcion("2x1", 0)
    assert descripcion == "Lleva 2 paga 1"


def test_obtener_descripcion_pe_3x2():
    descripcion = CalculadorDescuento.obtener_descripcion("3x2", 0)
    assert descripcion == "Lleva 3 paga 2"


def test_obtener_descripcion_pe_4x3():
    descripcion = CalculadorDescuento.obtener_descripcion("4x3", 0)
    assert descripcion == "Lleva 4 paga 3"


def test_obtener_descripcion_pe_5x4():
    descripcion = CalculadorDescuento.obtener_descripcion("5x4", 0)
    assert descripcion == "Lleva 5 paga 4"


@pytest.mark.parametrize("tipo,valor", [
    (None, 0),
    ("tipo_invalido", 0),
    ("", 0),
    (123, 0),
    ("porcentaje", None),
    ("porcentaje", -10),
])
def test_obtener_descripcion_pe_invalidos(tipo, valor):
    descripcion = CalculadorDescuento.obtener_descripcion(tipo, valor)
    assert descripcion == "Sin descuento"

# PRUEBA 1: VALOR INVALIDO EN PROMOCION FIJA
# CUBRE: Línea 62 de descuentos.py
# =========================================================
def test_valor_invalido_en_promocion_fija():
    with pytest.raises(ValueError, match="para promociones fijas el valor debe ser 0"):
        CalculadorDescuento.calcular_total("2x1", 1, 2, 10.00)

# PRUEBA 2: VALOR NO NUMERICO EN DESCRIPCION
# CUBRE: Líneas 171-172 de descuentos.py
# =========================================================
def test_obtener_descripcion_valor_no_numerico():
    descripcion = CalculadorDescuento.obtener_descripcion("porcentaje", "abc")
    assert descripcion == "Sin descuento"

# =========================================================
# PRUEBAS PARA CUBRIR LÍNEAS FALTANTES DE descuentos.py
# =========================================================

def test_valor_invalido_en_promocion_fija():
    """
    CUBRE: Línea 62 de descuentos.py
    Prueba que una promoción fija con valor != 0 lance excepción
    """
    with pytest.raises(ValueError, match="para promociones fijas el valor debe ser 0"):
        CalculadorDescuento.calcular_total("2x1", 1, 2, 10.00)
    
    with pytest.raises(ValueError, match="para promociones fijas el valor debe ser 0"):
        CalculadorDescuento.calcular_total("3x2", 5, 3, 10.00)
    
    with pytest.raises(ValueError, match="para promociones fijas el valor debe ser 0"):
        CalculadorDescuento.calcular_total("4x3", 10, 4, 10.00)
    
    with pytest.raises(ValueError, match="para promociones fijas el valor debe ser 0"):
        CalculadorDescuento.calcular_total("5x4", 100, 5, 10.00)


def test_obtener_descripcion_valor_no_numerico():
    """
    CUBRE: Líneas 171-172 de descuentos.py
    Prueba que obtener_descripcion maneje valores no numéricos
    """
    descripcion = CalculadorDescuento.obtener_descripcion("porcentaje", "abc")
    assert descripcion == "Sin descuento"
    
    descripcion = CalculadorDescuento.obtener_descripcion("porcentaje", None)
    assert descripcion == "Sin descuento"
    
    descripcion = CalculadorDescuento.obtener_descripcion("porcentaje", [1, 2, 3])
    assert descripcion == "Sin descuento"