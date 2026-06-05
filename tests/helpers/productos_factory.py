# tests/helpers/productos_factory.py

# PRODUCTO VALIDO
# =========================================================
def producto_valido():
    return {
        "nombre": "Jugo de Manzana",
        "precio": 14.50,
        "stock": 100,
        "tipo_descuento": "ninguno",
        "descuento_valor": 0
    }


# PRODUCTO NOMBRE INVALIDO
# =========================================================
def producto_nombre_invalido():
    return {
        "nombre": "",
        "precio": 14.50,
        "stock": 100,
        "tipo_descuento": "ninguno",
        "descuento_valor": 0
    }


# PRODUCTO PRECIO INVALIDO
# =========================================================
def producto_precio_invalido():
    return {
        "nombre": "Producto Test",
        "precio": -10.00,
        "stock": 100,
        "tipo_descuento": "ninguno",
        "descuento_valor": 0
    }


# PRODUCTO STOCK INVALIDO
# =========================================================
def producto_stock_invalido():
    return {
        "nombre": "Producto Test",
        "precio": 10.00,
        "stock": -5,
        "tipo_descuento": "ninguno",
        "descuento_valor": 0
    }


# PRODUCTO PRECIO NO NUMERICO
# =========================================================
def producto_precio_no_numerico():
    return {
        "nombre": "Producto Test",
        "precio": "NO_NUMERO",
        "stock": 100,
        "tipo_descuento": "ninguno",
        "descuento_valor": 0
    }


# PRODUCTO STOCK NO NUMERICO
# =========================================================
def producto_stock_no_numerico():
    return {
        "nombre": "Producto Test",
        "precio": 10.00,
        "stock": "NO_NUMERO",
        "tipo_descuento": "ninguno",
        "descuento_valor": 0
    }


# PRODUCTO CON DESCUENTO PORCENTAJE
# =========================================================
def producto_descuento_porcentaje():
    return {
        "nombre": "Producto con Descuento",
        "precio": 100.00,
        "stock": 50,
        "tipo_descuento": "porcentaje",
        "descuento_valor": 20
    }


# PRODUCTO CON DESCUENTO 2X1
# =========================================================
def producto_descuento_2x1():
    return {
        "nombre": "Producto 2x1",
        "precio": 15.00,
        "stock": 100,
        "tipo_descuento": "2x1",
        "descuento_valor": 0
    }
# DATOS PARA PRUEBAS PARAMETRIZADAS
# =========================================================
def datos_productos_invalidos():
    """Retorna lista de tuplas (datos, mensaje_esperado) para pruebas parametrizadas"""
    return [
        (producto_nombre_invalido(), "nombre no puede estar vacío"),
        (producto_precio_invalido(), "precio debe ser mayor que cero"),
        (producto_precio_cero(), "precio debe ser mayor que cero"),
        (producto_stock_invalido(), "stock no puede ser negativo"),
        (producto_precio_no_numerico(), "precio debe ser un número válido"),
        (producto_stock_no_numerico(), "stock debe ser un número entero válido"),
    ]
