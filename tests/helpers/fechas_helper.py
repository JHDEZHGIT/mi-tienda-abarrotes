# tests/helpers/fechas_helper.py

from datetime import date, timedelta


def fecha_hace_anios(anios):
    hoy = date.today()
    try:
        fecha = hoy.replace(year=hoy.year - anios)
    except ValueError:
        fecha = hoy.replace(month=2, day=28, year=hoy.year - anios)
    return str(fecha)


def fecha_hace_18_anios():
    return fecha_hace_anios(18)


def fecha_hace_30_anios():
    return fecha_hace_anios(30)


def fecha_hace_65_anios():
    return fecha_hace_anios(65)


def fechas_valores_limite_edad():
    """Retorna fechas para valores límite de edad"""
    return [
        (fecha_hace_17_anios(), False),   # Menor de 18 - inválido
        (fecha_hace_18_anios(), True),    # Justo 18 - válido
        (fecha_hace_19_anios(), True),    # 19 - válido
        (fecha_hace_64_anios(), True),    # 64 - válido
        (fecha_hace_65_anios(), True),    # 65 - válido
        (fecha_hace_66_anios(), False),   # Mayor de 65 - inválido
    ]


def fechas_invalidas():
    """Retorna fechas inválidas para pruebas"""
    return [
        "",
        "   ",
        "2024-13-01",
        "2024-01-32",
        "fecha_invalida",
        "01/01/2024",
    ]


def telefono_valores_limite():
    """Retorna valores de teléfono para pruebas de valores límite"""
    return [
        ("1234567", False),      # 7 dígitos - inválido
        ("12345678", True),      # 8 dígitos - válido
        ("123456789", True),     # 9 dígitos - válido
        ("123456789012345", True),  # 15 dígitos - válido
        ("1234567890123456", False), # 16 dígitos - inválido
    ]