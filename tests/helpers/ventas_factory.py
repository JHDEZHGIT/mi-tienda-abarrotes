# tests/helpers/ventas_factory.py

from tests.helpers.fechas_helper import fecha_hace_anios


# VENTA VALIDA
# =========================================================
def venta_valida(producto_id=1, cantidad=2, total=None):
    if total is None:
        total = cantidad * 14.50  # Precio aproximado
    return {
        "producto_id": producto_id,
        "cantidad": cantidad,
        "total": total
    }


# VENTA CANTIDAD CERO
# =========================================================
def venta_cantidad_cero():
    return {
        "producto_id": 1,
        "cantidad": 0,
        "total": 0
    }


# VENTA CANTIDAD NEGATIVA
# =========================================================
def venta_cantidad_negativa():
    return {
        "producto_id": 1,
        "cantidad": -5,
        "total": -50.00
    }


# VENTA PRODUCTO INEXISTENTE
# =========================================================
def venta_producto_inexistente():
    return {
        "producto_id": 9999,
        "cantidad": 2,
        "total": 100.00
    }


# VENTA TOTAL NEGATIVO
# =========================================================
def venta_total_negativo():
    return {
        "producto_id": 1,
        "cantidad": 2,
        "total": -29.00
    }


# VENTA TOTAL INVALIDO (NO NUMERICO)
# =========================================================
def venta_total_no_numerico():
    return {
        "producto_id": 1,
        "cantidad": 2,
        "total": "NO_NUMERO"
    }


# VENTA CON MULTIPLES PRODUCTOS (para simular carrito)
# =========================================================
def carrito_con_multiple_productos():
    return [
        {"id": 1, "nombre": "Producto 1", "cantidad": 2, "precio": 14.50, "subtotal": 29.00},
        {"id": 2, "nombre": "Producto 2", "cantidad": 1, "precio": 34.50, "subtotal": 34.50},
        {"id": 3, "nombre": "Producto 3", "cantidad": 3, "precio": 35.00, "subtotal": 105.00}
    ]


# VENTA CARRO VACIO
# =========================================================
def carrito_vacio():
    return []


# VENTA CON DESCUENTO PORCENTAJE
# =========================================================
def venta_con_descuento_porcentaje():
    return {
        "producto_id": 1,
        "cantidad": 2,
        "precio": 100.00,
        "tipo_descuento": "porcentaje",
        "descuento_valor": 20,
        "total_esperado": 160.00
    }


# VENTA CON DESCUENTO 2X1
# =========================================================
def venta_con_descuento_2x1():
    return {
        "producto_id": 1,
        "cantidad": 4,
        "precio": 10.00,
        "tipo_descuento": "2x1",
        "total_esperado": 20.00
    }


# VENTA CON DESCUENTO 3X2
# =========================================================
def venta_con_descuento_3x2():
    return {
        "producto_id": 1,
        "cantidad": 6,
        "precio": 10.00,
        "tipo_descuento": "3x2",
        "total_esperado": 40.00
    }


# VENTA CON DESCUENTO 4X3
# =========================================================
def venta_con_descuento_4x3():
    return {
        "producto_id": 1,
        "cantidad": 8,
        "precio": 10.00,
        "tipo_descuento": "4x3",
        "total_esperado": 60.00
    }


# VENTA CON DESCUENTO 5X4
# =========================================================
def venta_con_descuento_5x4():
    return {
        "producto_id": 1,
        "cantidad": 10,
        "precio": 10.00,
        "tipo_descuento": "5x4",
        "total_esperado": 80.00
    }