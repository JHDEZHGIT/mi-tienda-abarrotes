# tests/helpers/integration_helpers.py
"""
Helpers específicos para pruebas de integración de descuentos
SOLO contiene lo que realmente se usa en los tests
"""

import pytest
from appweb.descuentos import CalculadorDescuento


class ContextoVentaSimulado:
    """Simula un contexto de venta para pruebas de integración"""
    
    def __init__(self):
        self.productos = []
        self.total_original = 0.0
        self.total_con_descuento = 0.0
    
    def agregar_producto(self, nombre, precio, cantidad, tipo_descuento, valor_descuento):
        """Agrega un producto al carrito simulado"""
        subtotal_original = precio * cantidad
        total_con_descuento = CalculadorDescuento.calcular_total(
            tipo_descuento, valor_descuento, cantidad, precio
        )
        
        self.productos.append({
            'nombre': nombre,
            'precio': precio,
            'cantidad': cantidad,
            'tipo_descuento': tipo_descuento,
            'valor_descuento': valor_descuento,
            'subtotal_original': subtotal_original,
            'total_con_descuento': total_con_descuento
        })
        
        self.total_original += subtotal_original
        self.total_con_descuento += total_con_descuento
        
        return total_con_descuento


@pytest.fixture
def carrito_simulado():
    """Fixture que proporciona un carrito simulado para pruebas de integración"""
    return ContextoVentaSimulado()


@pytest.fixture
def escenario_venta_mixta():
    """
    Fixture que crea un escenario de venta con múltiples tipos de descuento
    """
    contexto = ContextoVentaSimulado()
    
    # Agregar productos con diferentes tipos de descuento
    contexto.agregar_producto("Manzanas", 10.0, 3, "2x1", 0)
    contexto.agregar_producto("Peras", 15.0, 2, "3x2", 0)
    contexto.agregar_producto("Plátanos", 8.0, 4, "4x3", 0)
    contexto.agregar_producto("Naranjas", 12.0, 5, "5x4", 0)
    contexto.agregar_producto("Uvas", 20.0, 2, "porcentaje", 10)
    contexto.agregar_producto("Sandía", 30.0, 1, "ninguno", 0)
    
    return contexto


def datos_carrito_inicial():
    """
    UN SOLO caso representativo para probar integración de carrito
    Incluye diferentes tipos de descuento: 2x1, 3x2 y porcentaje
    """
    return [
        (
            [  # Un caso completo que cubre todas las variantes
                ('Manzanas', 10.0, 3, "2x1", 0),
                ('Peras', 15.0, 2, "3x2", 0),
                ('Uvas', 20.0, 1, "porcentaje", 10),
            ],
            (20.0, 30.0, 18.0),  # Totales individuales
            68.0  # Total general
        ),
    ]