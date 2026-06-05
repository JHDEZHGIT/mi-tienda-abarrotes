# tests/system/test_alta_empleado.py

import pytest
import time
from appweb.empleados import Empleado
from appweb.postgres_db import pgdb
from appweb.empleados import AltaEmpleadoException
from tests.helpers.empleados_factory import (
    empleado_valido,
    empleado_admin_valido,
    empleado_nombre_invalido,
    empleado_apellido_paterno_invalido,
    empleado_email_invalido,
    empleado_username_invalido,
    empleado_password_corta,
)


# =========================================================
# ALTA EMPLEADO EXITOSA
# =========================================================
def test_alta_empleado_exitosa(client_login_admin):
    from appweb.empleados import Empleado as EmpleadoModel
    
    # Usar datos únicos para evitar duplicados
    unique_id = int(time.time())
    datos = empleado_valido()
    datos["email"] = f"test_{unique_id}@example.com"
    datos["username"] = f"test_user_{unique_id}"
    
    total_antes = len(EmpleadoModel.consultar_todos())
    response = client_login_admin.post(
        "/agregar_empleado",
        data=datos,
        follow_redirects=True
    )
    total_despues = len(EmpleadoModel.consultar_todos())
    assert response.status_code == 200
    
    texto = response.get_data(as_text=True)
    assert "agregado correctamente" in texto.lower()
    assert total_despues == total_antes + 1
    
    # Limpiar: eliminar el empleado creado
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE username = %s", (datos["username"],))


# =========================================================
# ALTA EMPLEADO ADMIN EXITOSA
# =========================================================
def test_alta_empleado_admin_exitosa(client_login_admin):
    from appweb.empleados import Empleado as EmpleadoModel
    
    # Usar datos únicos para evitar duplicados
    unique_id = int(time.time())
    datos = empleado_admin_valido()
    datos["email"] = f"admin_test_{unique_id}@example.com"
    datos["username"] = f"admin_user_{unique_id}"
    
    total_antes = len(EmpleadoModel.consultar_todos())
    response = client_login_admin.post(
        "/agregar_empleado",
        data=datos,
        follow_redirects=True
    )
    total_despues = len(EmpleadoModel.consultar_todos())
    assert response.status_code == 200
    
    texto = response.get_data(as_text=True)
    assert "agregado correctamente" in texto.lower()
    assert total_despues == total_antes + 1
    
    # Limpiar: eliminar el empleado creado
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE username = %s", (datos["username"],))


# =========================================================
# ALTA EMPLEADO - CASOS INVALIDOS (PARAMETRIZADOS) - CORREGIDO
# =========================================================

@pytest.mark.parametrize("datos_empleado,mensaje_esperado", [
    (empleado_nombre_invalido(), "El nombre es requerido"),  # CORREGIDO
    (empleado_apellido_paterno_invalido(), "El apellido paterno es requerido"),  # CORREGIDO
    (empleado_email_invalido(), "formato de correo electrónico inválido"),
    (empleado_username_invalido(), "nombre de usuario solo puede contener letras minúsculas"),
    (empleado_password_corta(), "contraseña debe tener al menos 6 caracteres"),
])
def test_alta_empleado_campos_invalidos(client_login_admin, datos_empleado, mensaje_esperado):
    response = client_login_admin.post(
        "/agregar_empleado",
        data=datos_empleado,
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert mensaje_esperado in texto


# =========================================================
# ALTA EMPLEADO EXCEPTION DB
# =========================================================
def test_alta_empleado_exception_db(client_login_admin):
    from appweb.empleados import Empleado as EmpleadoModel
    
    original_insertar = EmpleadoModel.insertar

    def insertar_con_error(self):
        raise AltaEmpleadoException("Error al insertar empleado")
    
    EmpleadoModel.insertar = insertar_con_error
    
    try:
        unique_id = int(time.time())
        datos = empleado_valido()
        datos["email"] = f"error_test_{unique_id}@example.com"
        datos["username"] = f"error_user_{unique_id}"
        
        response = client_login_admin.post(
            "/agregar_empleado",
            data=datos,
            follow_redirects=True
        )
        assert response.status_code == 200
        texto = response.get_data(as_text=True)
        assert "Error al insertar empleado" in texto
    finally:
        EmpleadoModel.insertar = original_insertar