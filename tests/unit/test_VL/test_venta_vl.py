# tests/unit/test_VL/test_venta_vl.py

import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from appweb.models import Venta, VentaException, Producto


# =========================================================
# VALORES LIMITE - PRODUCTO ID
# =========================================================

def test_producto_id_vl_0():
    """Producto ID = 0 - es válido para crear la venta"""
    venta = Venta(producto_id=0, cantidad=1, total=10.00)
    assert venta.producto_id == 0


def test_producto_id_vl_1():
    """Producto ID = 1 (límite inferior de IDs positivos)"""
    venta = Venta(producto_id=1, cantidad=1, total=10.00)
    assert venta.producto_id == 1


def test_producto_id_vl_2():
    """Producto ID = 2 (justo arriba del límite)"""
    venta = Venta(producto_id=2, cantidad=1, total=10.00)
    assert venta.producto_id == 2


def test_producto_id_vl_negativo():
    """Producto ID negativo - es válido"""
    venta = Venta(producto_id=-1, cantidad=1, total=10.00)
    assert venta.producto_id == -1


# =========================================================
# VALORES LIMITE - CANTIDAD
# =========================================================

def test_cantidad_vl_menos1():
    with pytest.raises(VentaException):
        Venta(producto_id=1, cantidad=-1, total=10.00)


def test_cantidad_vl_0():
    with pytest.raises(VentaException):
        Venta(producto_id=1, cantidad=0, total=10.00)


def test_cantidad_vl_1():
    venta = Venta(producto_id=1, cantidad=1, total=10.00)
    assert venta.cantidad == 1


def test_cantidad_vl_999998():
    venta = Venta(producto_id=1, cantidad=999998, total=9999980.00)
    assert venta.cantidad == 999998


def test_cantidad_vl_999999():
    venta = Venta(producto_id=1, cantidad=999999, total=9999990.00)
    assert venta.cantidad == 999999


def test_cantidad_vl_1000000():
    with pytest.raises(VentaException):
        Venta(producto_id=1, cantidad=1000000, total=10000000.00)


# =========================================================
# VALORES LIMITE - TOTAL
# =========================================================

def test_total_vl_menos0_01():
    with pytest.raises(VentaException):
        Venta(producto_id=1, cantidad=1, total=-0.01)


def test_total_vl_0():
    venta = Venta(producto_id=1, cantidad=1, total=0.00)
    assert venta.total == 0.00


def test_total_vl_0_01():
    venta = Venta(producto_id=1, cantidad=1, total=0.01)
    assert venta.total == 0.01


def test_total_vl_999999_99():
    venta = Venta(producto_id=1, cantidad=1, total=999999.99)
    assert venta.total == 999999.99


def test_total_vl_1000000():
    venta = Venta(producto_id=1, cantidad=1, total=1000000.00)
    assert venta.total == 1000000.00


# =========================================================
# VALORES LIMITE - FECHA
# =========================================================

def test_fecha_vl_ayer():
    venta = Venta(
        producto_id=1, cantidad=1, total=10.00,
        fecha=datetime.now() - timedelta(days=1)
    )
    assert venta.fecha is not None


def test_fecha_vl_hoy():
    venta = Venta(
        producto_id=1, cantidad=1, total=10.00,
        fecha=datetime.now()
    )
    assert venta.fecha is not None


def test_fecha_vl_manana():
    venta = Venta(
        producto_id=1, cantidad=1, total=10.00,
        fecha=datetime.now() + timedelta(days=1)
    )
    assert venta.fecha is not None


def test_fecha_vl_1900():
    venta = Venta(
        producto_id=1, cantidad=1, total=10.00,
        fecha=datetime(1900, 1, 1)
    )
    assert venta.fecha is not None


# =========================================================
# VALORES LIMITE - TOTAL VENTAS
# =========================================================

def test_total_ventas_vl():
    total = Venta.total_ventas()
    assert total is not None
    assert isinstance(total, (float, Decimal))
    assert float(total) >= 0


# =========================================================
# VALORES LIMITE - COMBINACIONES
# =========================================================

@pytest.mark.parametrize("producto_id,cantidad,total,esperado_valido", [
    (1, 1, 0.01, True),
    (1, 1, 0.00, True),
    (1, 0, 10.00, False),
    (1, 999999, 9999999.99, True),
    (1, 1000000, 10.00, False),
    (0, 1, 10.00, True),
    (1, -1, 10.00, False),
    (1, 1, -0.01, False),
])
def test_venta_vl_combinaciones(producto_id, cantidad, total, esperado_valido):
    if esperado_valido:
        venta = Venta(
            producto_id=producto_id,
            cantidad=cantidad,
            total=total
        )
        assert venta.producto_id == producto_id
        assert venta.cantidad == cantidad
        assert venta.total == total
    else:
        with pytest.raises(VentaException):
            Venta(
                producto_id=producto_id,
                cantidad=cantidad,
                total=total
            )
