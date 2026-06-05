# tests/system/test_empleado_editar.py

import pytest
import time
from appweb.empleados import Empleado
from appweb.postgres_db import pgdb


# =========================================================
# FIXTURE PARA CREAR EMPLEADO TEMPORAL
# =========================================================
@pytest.fixture
def empleado_temporal():
    """Crea un empleado temporal para pruebas de edición"""
    from appweb.empleados import Empleado
    
    unique_id = int(time.time())
    username = f"temp_edit_{unique_id}"
    email = f"temp_edit_{unique_id}@example.com"
    
    nuevo_empleado = Empleado(
        nombre="Temp",
        apellido_paterno="Edit",
        apellido_materno="Test",
        email=email,
        telefono="5512345678",
        username=username,
        password="test123",
        rol="vendedor"
    )
    nuevo_empleado.insertar()
    
    yield nuevo_empleado
    
    # Limpiar después de la prueba
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE id = %s", (nuevo_empleado.id,))


# =========================================================
# EDITAR EMPLEADO EXITOSO - CORREGIDO
# =========================================================
def test_editar_empleado_exitoso(client_login_admin, empleado_temporal):
    """Editar un empleado existente debe ser exitoso"""
    unique_id = int(time.time())
    nuevo_email = f"editado_{unique_id}@example.com"
    
    response = client_login_admin.post(
        f"/editar_empleado/{empleado_temporal.id}",
        data={
            "nombre": "Nombre Editado",
            "apellido_paterno": "ApellidoEditado",
            "apellido_materno": "MaternoEditado",
            "email": nuevo_email,  # Email único
            "telefono": "5512345678",
            "fecha_contratacion": "2024-01-01",
            "username": empleado_temporal.username,  # Mantener mismo username
            "rol": empleado_temporal.rol
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "actualizado correctamente" in texto.lower()


# =========================================================
# EDITAR EMPLEADO INEXISTENTE
# =========================================================
def test_editar_empleado_inexistente(client_login_admin):
    response = client_login_admin.get(
        "/editar_empleado/9999",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Empleado no encontrado" in texto


# =========================================================
# EDITAR EMPLEADO SIN PERMISOS (VENDEDOR) - CORREGIDO
# =========================================================
def test_editar_empleado_sin_permisos(client_login_vendedor_temporal, empleado_temporal):
    """Vendedor no debe poder editar empleados"""
    response = client_login_vendedor_temporal.get(
        f"/editar_empleado/{empleado_temporal.id}",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Acceso denegado" in texto or "permisos" in texto


# =========================================================
# CAMBIAR CONTRASEÑA EMPLEADO EXITOSO - CORREGIDO
# =========================================================
def test_cambiar_password_empleado_exitoso(client_login_admin, empleado_temporal):
    """Cambiar contraseña de un empleado debe ser exitoso"""
    response = client_login_admin.post(
        f"/cambiar_password_empleado/{empleado_temporal.id}",
        data={"nueva_password": "nuevapass123"},
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Contraseña actualizada correctamente" in texto or "actualizada" in texto.lower()


# =========================================================
# CAMBIAR CONTRASEÑA EMPLEADO CON PASSWORD CORTA
# =========================================================
def test_cambiar_password_empleado_corta(client_login_admin, empleado_temporal):
    """Password corta debe ser rechazada"""
    response = client_login_admin.post(
        f"/cambiar_password_empleado/{empleado_temporal.id}",
        data={"nueva_password": "123"},
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "6 caracteres" in texto or "menos de 6" in texto


# =========================================================
# CAMBIAR CONTRASEÑA EMPLEADO INEXISTENTE
# =========================================================
def test_cambiar_password_empleado_inexistente(client_login_admin):
    response = client_login_admin.post(
        "/cambiar_password_empleado/9999",
        data={"nueva_password": "nuevapass123"},
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Empleado no encontrado" in texto or "no encontrado" in texto