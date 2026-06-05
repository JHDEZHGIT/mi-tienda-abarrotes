# tests/helpers/endpoints_helper.py

# Textos comunes en las páginas
TEXTO_LOGIN = "Iniciar sesión"
TEXTO_INICIO_SESION = "Inicio de Sesión"
TEXTO_SIN_SESION = "No se ha iniciado sesión"


def rutas_protegidas():
    """Retorna lista de rutas protegidas que requieren autenticación"""
    return [
        ("/inicio", "Página de inicio"),
        ("/ventas", "Pantalla de ventas"),
        ("/carrito", "Carrito de compras"),
        ("/productos", "Gestión de productos"),
        ("/empleados", "Gestión de empleados"),
        ("/historial", "Historial de ventas"),
        ("/reporte_stock", "Reporte de stock"),
    ]


def rutas_admin():
    """Retorna rutas accesibles por administrador con sus textos esperados"""
    return [
        ("/inicio", "Tienda de Abarrotes"),
        ("/ventas", "Punto de venta"),  # Corregido: el título real es "Punto de venta"
        ("/carrito", "Carrito de compras"),
        ("/productos", "Gestión de productos"),
        ("/empleados", "Gestión de empleados"),
        ("/historial", "Historial de ventas"),
        ("/reporte_stock", "Reporte de inventario"),
    ]


def rutas_vendedor():
    """Retorna rutas accesibles por vendedor con sus textos esperados"""
    return [
        ("/inicio", "Tienda de Abarrotes"),
        ("/ventas", "Punto de venta"),  # Corregido: el título real es "Punto de venta"
        ("/carrito", "Carrito de compras"),
    ]


def rutas_publicas():
    """Retorna rutas públicas que no requieren autenticación"""
    return [
        ("/", "Tienda de Abarrotes"),
        ("/login", "Iniciar sesión"),
    ]


def datos_usuario_admin():
    """Retorna datos de usuario administrador para pruebas"""
    return {
        "username": "admin",
        "password": "admin",
        "rol": "admin"
    }


def datos_usuario_vendedor():
    """Retorna datos de usuario vendedor para pruebas"""
    return {
        "username": "tello",
        "password": "vendedor123",
        "rol": "vendedor",
        "nombre": "Ángel Antonio Tello Montes De Oca"
    }