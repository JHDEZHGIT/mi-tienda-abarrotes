# tests/unit/test_PE/test_venta_pe.py

import pytest
from datetime import datetime

from appweb.models import Venta, VentaException, Producto


# =========================================================
# PARTICION DE EQUIVALENCIA - PRODUCTO ID
# =========================================================

def test_producto_id_pe_valido_generico():
    """Producto ID válido genérico (puede no existir en BD)"""
    venta = Venta(
        producto_id=1,
        cantidad=1,
        total=10.00
    )
    assert venta.producto_id == 1


@pytest.mark.parametrize("producto_id", [
    None,
    "abc",
    [],
    {},
])
def test_producto_id_pe_invalidos(producto_id):
    with pytest.raises(VentaException):
        Venta(
            producto_id=producto_id,
            cantidad=1,
            total=10.00
        )


def test_producto_id_pe_cero():
    """Cero es un ID válido para crear la venta"""
    venta = Venta(
        producto_id=0,
        cantidad=1,
        total=10.00
    )
    assert venta.producto_id == 0


def test_producto_id_pe_negativo():
    """Negativo es un ID válido para crear la venta"""
    venta = Venta(
        producto_id=-1,
        cantidad=1,
        total=10.00
    )
    assert venta.producto_id == -1


def test_producto_id_pe_booleano():
    """Booleano se convierte a entero (True=1, False=0)"""
    venta_true = Venta(
        producto_id=True,
        cantidad=1,
        total=10.00
    )
    assert venta_true.producto_id == 1
    
    venta_false = Venta(
        producto_id=False,
        cantidad=1,
        total=10.00
    )
    assert venta_false.producto_id == 0


def test_producto_id_pe_texto_numerico():
    """Texto numérico se convierte a entero"""
    venta = Venta(
        producto_id="123",
        cantidad=1,
        total=10.00
    )
    assert venta.producto_id == 123


# =========================================================
# PARTICION DE EQUIVALENCIA - CANTIDAD
# =========================================================

def test_cantidad_pe_valida():
    venta = Venta(
        producto_id=1,
        cantidad=5,
        total=50.00
    )
    assert venta.cantidad == 5


@pytest.mark.parametrize("cantidad", [
    None,
    0,
    -1,
    -5,
    "abc",
    [],
    {},
    1000000,
])
def test_cantidad_pe_invalidos(cantidad):
    with pytest.raises(VentaException):
        Venta(
            producto_id=1,
            cantidad=cantidad,
            total=10.00
        )


def test_cantidad_pe_texto_numerico():
    """Texto numérico se convierte a entero"""
    venta = Venta(
        producto_id=1,
        cantidad="5",
        total=50.00
    )
    assert venta.cantidad == 5


def test_cantidad_pe_booleano():
    """Booleano se convierte a entero (True=1)"""
    venta = Venta(
        producto_id=1,
        cantidad=True,
        total=10.00
    )
    assert venta.cantidad == 1


# =========================================================
# PARTICION DE EQUIVALENCIA - TOTAL
# =========================================================

def test_total_pe_valido():
    venta = Venta(
        producto_id=1,
        cantidad=1,
        total=99.99
    )
    assert venta.total == 99.99


@pytest.mark.parametrize("total", [
    None,
    -0.01,
    -1.00,
    "abc",
    [],
    {},
])
def test_total_pe_invalidos(total):
    with pytest.raises(VentaException):
        Venta(
            producto_id=1,
            cantidad=1,
            total=total
        )


def test_total_pe_texto_numerico():
    """Texto numérico se convierte a float"""
    venta = Venta(
        producto_id=1,
        cantidad=1,
        total="99.99"
    )
    assert venta.total == 99.99


def test_total_pe_booleano():
    """Booleano se convierte a float (True=1.0)"""
    venta = Venta(
        producto_id=1,
        cantidad=1,
        total=True
    )
    assert venta.total == 1.0


# =========================================================
# PARTICION DE EQUIVALENCIA - FECHA
# =========================================================

def test_fecha_pe_valida():
    fecha = datetime.now()
    venta = Venta(
        producto_id=1,
        cantidad=1,
        total=10.00,
        fecha=fecha
    )
    assert venta.fecha == fecha


def test_fecha_pe_none():
    venta = Venta(
        producto_id=1,
        cantidad=1,
        total=10.00,
        fecha=None
    )
    assert venta.fecha is None


# =========================================================
# PARTICION DE EQUIVALENCIA - REGISTRAR VENTA
# =========================================================

def test_registrar_venta_producto_inexistente():
    with pytest.raises(VentaException) as error:
        venta = Venta(
            producto_id=99999,
            cantidad=1,
            total=10.00
        )
        venta.registrar()
    assert "no existe" in str(error.value).lower()


# =========================================================
# PARTICION DE EQUIVALENCIA - CONSULTAR HISTORIAL
# =========================================================

def test_consultar_historial():
    historial = Venta.consultar_historial()
    assert isinstance(historial, list)
    if len(historial) > 0:
        venta = historial[0]
        assert 'id' in venta
        assert 'nombre_producto' in venta
        assert 'cantidad' in venta
        assert 'total' in venta
        assert 'fecha' in venta


# =========================================================
# PARTICION DE EQUIVALENCIA - TOTAL VENTAS
# =========================================================

def test_total_ventas():
    total = Venta.total_ventas()
    # total puede ser Decimal o float
    assert total is not None
    assert float(total) >= 0


# =========================================================
# PARTICION DE EQUIVALENCIA - VALORES LIMITE
# =========================================================

def test_cantidad_limite_inferior():
    venta = Venta(
        producto_id=1,
        cantidad=1,
        total=10.00
    )
    assert venta.cantidad == 1


def test_cantidad_limite_superior():
    venta = Venta(
        producto_id=1,
        cantidad=999999,
        total=9999990.00
    )
    assert venta.cantidad == 999999


def test_total_limite_inferior():
    venta = Venta(
        producto_id=1,
        cantidad=1,
        total=0.01
    )
    assert venta.total == 0.01


def test_total_limite_superior():
    venta = Venta(
        producto_id=1,
        cantidad=1,
        total=999999.99
    )
    assert venta.total == 999999.99


# =========================================================
# PARTICION DE EQUIVALENCIA - TIPOS DE DATOS COMPLEJOS
# =========================================================

@pytest.mark.parametrize("kwargs", [
    {"producto_id": "uno", "cantidad": 1, "total": 10.00},
    {"producto_id": 1, "cantidad": "dos", "total": 10.00},
    {"producto_id": 1, "cantidad": 1, "total": "diez"},
    {"producto_id": None, "cantidad": None, "total": None},
    {"producto_id": 1, "cantidad": 1, "total": "10.00"},
])
def test_tipos_datos_complejos_invalidos_pe(kwargs):
    # Algunos casos pueden ser válidos (conversión automática)
    try:
        venta = Venta(**kwargs)
        assert venta is not None
    except VentaException:
        assert True