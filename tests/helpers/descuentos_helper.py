# tests/helpers/descuentos_helper.py

from appweb.descuentos import CalculadorDescuento


def datos_cantidad_limite():
    """Retorna datos para pruebas de límite de cantidad"""
    return [
        (-1, None, True),      # justo debajo - inválido
        (0, 0.00, False),      # límite inferior - válido
        (1, 10.00, False),     # justo arriba - válido
        (999999, 9999990.00, False),  # valor alto - válido
        (1000000, 10000000.00, False), # valor muy alto - válido
    ]


def datos_precio_limite():
    """Retorna datos para pruebas de límite de precio"""
    return [
        (-0.01, None, True),   # justo debajo - inválido
        (0, 0.00, False),      # límite inferior (0) - válido
        (0.01, 0.05, False),   # justo arriba - válido
        (999999.99, 4999999.95, False),  # valor alto - válido
        (1000000.00, 5000000.00, False), # valor muy alto - válido
    ]


def datos_porcentaje_limite():
    """
    Retorna datos para pruebas de límite de porcentaje.
    Para cada múltiplo de 5 entre 5 y 90 se prueban 3 valores:
    - justo debajo (inválido)
    - el límite exacto (válido)
    - justo arriba (inválido)
    """
    porcentajes_validos = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
    resultados = []
    
    for p in porcentajes_validos:
        resultados.append((p - 1, None, True))   # inválido
        resultados.append((p, 100 - p, False))   # válido
        resultados.append((p + 1, None, True))   # inválido
    
    return resultados


def datos_porcentaje_validos():
    """Retorna datos para pruebas de porcentajes válidos"""
    return [
        (5, 100, 1, 95.00),
        (10, 100, 1, 90.00),
        (15, 100, 2, 170.00),
        (20, 50, 2, 80.00),
        (25, 200, 1, 150.00),
        (30, 100, 1, 70.00),
        (35, 100, 1, 65.00),
        (40, 100, 1, 60.00),
        (45, 100, 1, 55.00),
        (50, 100, 1, 50.00),
        (55, 100, 1, 45.00),
        (60, 100, 1, 40.00),
        (65, 100, 1, 35.00),
        (70, 100, 1, 30.00),
        (75, 100, 1, 25.00),
        (80, 100, 1, 20.00),
        (85, 100, 1, 15.00),
        (90, 100, 1, 10.00),
    ]


def datos_porcentaje_invalidos():
    """Retorna datos para pruebas de porcentajes inválidos"""
    return [
        (0, "0% no es válido"),
        (3, "3% no es múltiplo de 5"),
        (4, "4% es menor a 5%"),
        (7, "7% no es múltiplo de 5"),
        (92, "92% excede 90%"),
        (95, "95% excede 90%"),
        (100, "100% excede 90%"),
    ]


def datos_promocion_2x1():
    """Datos para pruebas de promoción 2x1 (para PE)"""
    return [
        (0, 10, 0.00),
        (1, 10, 10.00),
        (2, 10, 10.00),
        (3, 10, 20.00),
        (4, 10, 20.00),
        (5, 10, 30.00),
        (10, 10, 50.00),
        (100, 10, 500.00),
    ]


def datos_promocion_2x1_vl():
    """
    Datos para pruebas de valor límite de 2x1 (para VL)
    Solo cantidad y esperado (precio fijo 10.00)
    """
    return [
        (0, 0.00),   # Límite: cero unidades
        (1, 10.00),  # Unidades impares (1)
        (2, 10.00),  # Unidades pares exactas (2)
        (3, 20.00),  # Unidades impares con resto (3)
    ]


def datos_promocion_3x2():
    """Datos para pruebas de promoción 3x2 (para PE)"""
    return [
        (0, 10, 0.00),
        (1, 10, 10.00),
        (2, 10, 20.00),
        (3, 10, 20.00),
        (4, 10, 30.00),
        (5, 10, 40.00),
        (6, 10, 40.00),
        (9, 10, 60.00),
        (10, 10, 70.00),
    ]


def datos_promocion_3x2_vl():
    """
    Datos para pruebas de valor límite de 3x2 (para VL)
    Solo cantidad y esperado (precio fijo 10.00)
    """
    return [
        (0, 0.00),
        (1, 10.00),
        (2, 20.00),
        (3, 20.00),
        (4, 30.00),
    ]


def datos_promocion_4x3():
    """Datos para pruebas de promoción 4x3 (para PE)"""
    return [
        (0, 10, 0.00),
        (1, 10, 10.00),
        (2, 10, 20.00),
        (3, 10, 30.00),
        (4, 10, 30.00),
        (5, 10, 40.00),
        (6, 10, 50.00),
        (7, 10, 60.00),
        (8, 10, 60.00),
        (12, 10, 90.00),
    ]


def datos_promocion_4x3_vl():
    """
    Datos para pruebas de valor límite de 4x3 (para VL)
    Solo cantidad y esperado (precio fijo 10.00)
    """
    return [
        (0, 0.00),
        (1, 10.00),
        (2, 20.00),
        (3, 30.00),
        (4, 30.00),
        (5, 40.00),
    ]


def datos_promocion_5x4():
    """Datos para pruebas de promoción 5x4 (para PE)"""
    return [
        (0, 10, 0.00),
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
        (15, 10, 120.00),
    ]


def datos_promocion_5x4_vl():
    """
    Datos para pruebas de valor límite de 5x4 (para VL)
    Solo cantidad y esperado (precio fijo 10.00)
    """
    return [
        (0, 0.00),
        (1, 10.00),
        (2, 20.00),
        (3, 30.00),
        (4, 40.00),
        (5, 40.00),
        (6, 50.00),
    ]


def datos_tipos_descuento_validos():
    """Tipos de descuento válidos"""
    return [
        ("ninguno", 0, 5, 10.00, 50.00),
        ("porcentaje", 5, 1, 100.00, 95.00),
        ("2x1", 0, 2, 10.00, 10.00),
        ("3x2", 0, 3, 10.00, 20.00),
        ("4x3", 0, 4, 10.00, 30.00),
        ("5x4", 0, 5, 10.00, 40.00),
    ]


def datos_promociones_fijas_con_valor_invalido():
    """Datos para pruebas de promociones fijas con valor inválido"""
    return [
        ("2x1", 1),
        ("2x1", 5),
        ("3x2", 10),
        ("4x3", 100),
        ("5x4", -1),
        ("ninguno", 50),
    ]


def datos_descripciones():
    """Datos para pruebas de descripciones de descuento"""
    return [
        ("ninguno", 0, "Sin descuento"),
        ("ninguno", 50, "Sin descuento"),
        ("porcentaje", 5, "5% de descuento"),
        ("porcentaje", 10, "10% de descuento"),
        ("porcentaje", 15, "15% de descuento"),
        ("porcentaje", 20, "20% de descuento"),
        ("porcentaje", 25, "25% de descuento"),
        ("porcentaje", 30, "30% de descuento"),
        ("porcentaje", 35, "35% de descuento"),
        ("porcentaje", 40, "40% de descuento"),
        ("porcentaje", 45, "45% de descuento"),
        ("porcentaje", 50, "50% de descuento"),
        ("porcentaje", 55, "55% de descuento"),
        ("porcentaje", 60, "60% de descuento"),
        ("porcentaje", 65, "65% de descuento"),
        ("porcentaje", 70, "70% de descuento"),
        ("porcentaje", 75, "75% de descuento"),
        ("porcentaje", 80, "80% de descuento"),
        ("porcentaje", 85, "85% de descuento"),
        ("porcentaje", 90, "90% de descuento"),
        ("porcentaje", 0, "Sin descuento"),
        ("2x1", 0, "Lleva 2 paga 1"),
        ("2x1", 999, "Lleva 2 paga 1"),
        ("3x2", 0, "Lleva 3 paga 2"),
        ("4x3", 0, "Lleva 4 paga 3"),
        ("5x4", 0, "Lleva 5 paga 4"),
    ]


def datos_parametros_invalidos():
    """Datos para pruebas de parámetros inválidos generales"""
    return [
        ("tipo_nulo", None, 0, 5, 10.00, "el tipo de descuento no puede ser nulo"),
        ("tipo_no_texto", 123, 0, 5, 10.00, "el tipo de descuento debe ser texto"),
        ("valor_nulo", "porcentaje", None, 1, 100.00, "el valor del descuento no puede ser nulo"),
        ("valor_no_numerico", "porcentaje", "abc", 1, 100.00, "no es un número válido"),
        ("cantidad_nula", "ninguno", 0, None, 10.00, "la cantidad no puede ser nula"),
        ("cantidad_negativa", "ninguno", 0, -5, 10.00, "la cantidad no puede ser negativa"),
        ("precio_nulo", "ninguno", 0, 5, None, "el precio unitario no puede ser nulo"),
        ("precio_negativo", "ninguno", 0, 5, -10.00, "el precio unitario no puede ser negativo"),
    ]