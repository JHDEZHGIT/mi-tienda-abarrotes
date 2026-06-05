# tests/system/test_descuento.py
"""
Pruebas de sistema para descuentos - SOLO código de producción
"""

import pytest
from appweb.descuentos import CalculadorDescuento
from tests.helpers.integration_helpers import (
    carrito_simulado,
    escenario_venta_mixta,
    datos_carrito_inicial,
)


# =========================================================
# 1. INTEGRACION: CARRITO CON MÚLTIPLES DESCUENTOS
# =========================================================

@pytest.mark.parametrize("productos,totales_individuales,total_esperado", 
                         datos_carrito_inicial())
def test_calcular_total_carrito_con_diferentes_descuentos(
    carrito_simulado, productos, totales_individuales, total_esperado
):
    """Prueba la integración de calcular_total() en un contexto de carrito"""
    for i, (nombre, precio, cantidad, tipo, valor) in enumerate(productos):
        total = carrito_simulado.agregar_producto(nombre, precio, cantidad, tipo, valor)
        assert total == totales_individuales[i]
    
    assert carrito_simulado.total_con_descuento == total_esperado


# =========================================================
# 2. INTEGRACION: GENERACIÓN DE TICKET
# =========================================================

def test_integracion_ticket_generacion(escenario_venta_mixta):
    """Prueba la integración completa para generar un ticket de venta"""
    assert escenario_venta_mixta.total_con_descuento > 0
    
    for producto in escenario_venta_mixta.productos:
        assert producto['total_con_descuento'] <= producto['subtotal_original']


# =========================================================
# 3. VALIDACIONES DEL SISTEMA
# =========================================================

def test_integracion_validaciones_porcentaje():
    """Prueba las validaciones de porcentaje en calcular_total()"""
    # Válidos
    CalculadorDescuento.calcular_total("porcentaje", 5, 1, 100.00)
    CalculadorDescuento.calcular_total("porcentaje", 50, 1, 100.00)
    CalculadorDescuento.calcular_total("porcentaje", 90, 1, 100.00)
    
    # Inválidos
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("porcentaje", 0, 1, 100.00)
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("porcentaje", 3, 1, 100.00)
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("porcentaje", 95, 1, 100.00)


def test_integracion_validaciones_cantidad():
    """Prueba las validaciones de cantidad en calcular_total()"""
    # Válidas
    CalculadorDescuento.calcular_total("ninguno", 0, 0, 10.00)
    CalculadorDescuento.calcular_total("ninguno", 0, 1, 10.00)
    CalculadorDescuento.calcular_total("ninguno", 0, 1000, 10.00)
    
    # Inválidas
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("ninguno", 0, -1, 10.00)
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("ninguno", 0, None, 10.00)


def test_integracion_validaciones_precio():
    """Prueba las validaciones de precio en calcular_total()"""
    # Válidos
    CalculadorDescuento.calcular_total("ninguno", 0, 1, 0.00)
    CalculadorDescuento.calcular_total("ninguno", 0, 1, 0.01)
    CalculadorDescuento.calcular_total("ninguno", 0, 1, 999999.99)
    
    # Inválidos
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("ninguno", 0, 1, -0.01)
    with pytest.raises(ValueError):
        CalculadorDescuento.calcular_total("ninguno", 0, 1, None)


def test_integracion_calculos_2x1():
    """Prueba los cálculos de promoción 2x1"""
    casos = [
        (1, 10, 10.00), (2, 10, 10.00), (3, 10, 20.00),
        (4, 10, 20.00), (5, 10, 30.00),
    ]
    for cantidad, precio, esperado in casos:
        total = CalculadorDescuento.calcular_total("2x1", 0, cantidad, precio)
        assert total == esperado


def test_integracion_calculos_3x2():
    """Prueba los cálculos de promoción 3x2"""
    casos = [
        (1, 10, 10.00), (2, 10, 20.00), (3, 10, 20.00),
        (4, 10, 30.00), (5, 10, 40.00), (6, 10, 40.00),
    ]
    for cantidad, precio, esperado in casos:
        total = CalculadorDescuento.calcular_total("3x2", 0, cantidad, precio)
        assert total == esperado