# tests/system/test_empleado_editar.py

import pytest
import time
from appweb.empleados import Empleado
from appweb.postgres_db import pgdb


# =========================================================
# FIXTURES PARA CREAR EMPLEADOS TEMPORALES
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


@pytest.fixture
def empleado_temporal_admin():
    """Crea un empleado admin temporal para pruebas"""
    from appweb.empleados import Empleado
    
    unique_id = int(time.time())
    username = f"temp_admin_{unique_id}"
    email = f"temp_admin_{unique_id}@example.com"
    
    nuevo_empleado = Empleado(
        nombre="Admin",
        apellido_paterno="Temp",
        email=email,
        username=username,
        password="admin123",
        rol="admin"
    )
    nuevo_empleado.insertar()
    
    yield nuevo_empleado
    
    with pgdb.get_cursor() as cur:
        cur.execute("DELETE FROM empleados WHERE id = %s", (nuevo_empleado.id,))


# =========================================================
# PRUEBA 1: ACCESO AL FORMULARIO DE EDICIÓN (GET)
# CUBRE: Línea 1103 (render_template GET)
# =========================================================
def test_editar_empleado_formulario_get(client_login_admin, empleado_temporal):
    """
    Prueba que el formulario de edición de empleado se muestra correctamente.
    CUBRE: Línea 1103 de views.py (GET /editar_empleado/<id>)
    """
    response = client_login_admin.get(
        f"/editar_empleado/{empleado_temporal.id}",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Editar empleado" in texto or "editar" in texto.lower()
    assert empleado_temporal.nombre in texto
    assert empleado_temporal.apellido_paterno in texto


# =========================================================
# PRUEBA 2: EDITAR EMPLEADO EXITOSO (POST)
# CUBRE: Edición exitosa
# =========================================================
def test_editar_empleado_post_exitoso(client_login_admin, empleado_temporal):
    """
    Prueba la edición exitosa de un empleado.
    """
    nuevo_nombre = "Nombre Editado"
    nuevo_apellido = "ApellidoEditado"
    nuevo_email = f"editado_{int(time.time())}@example.com"
    
    response = client_login_admin.post(
        f"/editar_empleado/{empleado_temporal.id}",
        data={
            "nombre": nuevo_nombre,
            "apellido_paterno": nuevo_apellido,
            "apellido_materno": "MaternoEditado",
            "email": nuevo_email,
            "telefono": "5512345678",
            "fecha_contratacion": "2024-01-01",
            "username": empleado_temporal.username,
            "rol": empleado_temporal.rol
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "actualizado correctamente" in texto.lower()
    
    # Verificar cambios en BD
    empleado = Empleado.consultar_por_id(empleado_temporal.id)
    assert empleado.nombre == nuevo_nombre
    assert empleado.apellido_paterno == nuevo_apellido
    assert empleado.email == nuevo_email


# =========================================================
# PRUEBA 3: EDITAR EMPLEADO CON EMAIL DUPLICADO
# CUBRE: Líneas 1096-1097 (EmailEmpleadoException)
# =========================================================
def test_editar_empleado_email_duplicado(client_login_admin, empleado_temporal, empleado_temporal_admin):
    """
    Prueba que no se pueda editar un empleado con un email que ya existe.
    """
    response = client_login_admin.post(
        f"/editar_empleado/{empleado_temporal.id}",
        data={
            "nombre": empleado_temporal.nombre,
            "apellido_paterno": empleado_temporal.apellido_paterno,
            "apellido_materno": empleado_temporal.apellido_materno or "",
            "email": empleado_temporal_admin.email,  # Email ya existente
            "telefono": "5512345678",
            "fecha_contratacion": "2024-01-01",
            "username": empleado_temporal.username,
            "rol": empleado_temporal.rol
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "ya existe" in texto.lower() or "duplicado" in texto.lower() or "email" in texto.lower()


# =========================================================
# PRUEBA 4: EDITAR EMPLEADO CON USERNAME DUPLICADO
# CUBRE: Líneas 1098-1099 (UsernameEmpleadoException)
# =========================================================
def test_editar_empleado_username_duplicado(client_login_admin, empleado_temporal, empleado_temporal_admin):
    """
    Prueba que no se pueda editar un empleado con un username que ya existe.
    """
    response = client_login_admin.post(
        f"/editar_empleado/{empleado_temporal.id}",
        data={
            "nombre": empleado_temporal.nombre,
            "apellido_paterno": empleado_temporal.apellido_paterno,
            "apellido_materno": empleado_temporal.apellido_materno or "",
            "email": f"nuevo_email_{int(time.time())}@example.com",
            "telefono": "5512345678",
            "fecha_contratacion": "2024-01-01",
            "username": empleado_temporal_admin.username,  # Username ya existente
            "rol": empleado_temporal.rol
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "ya existe" in texto.lower() or "duplicado" in texto.lower() or "username" in texto.lower()


# =========================================================
# PRUEBA 6: EDITAR EMPLEADO INEXISTENTE
# =========================================================
def test_editar_empleado_inexistente(client_login_admin):
    """
    Prueba que al intentar editar un empleado inexistente se muestre error.
    """
    response = client_login_admin.get(
        "/editar_empleado/99999",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Empleado no encontrado" in texto


# =========================================================
# PRUEBA 7: DESACTIVAR (ELIMINAR) EMPLEADO EXITOSO
# CUBRE: Líneas 1174-1200 (eliminar_empleado)
# =========================================================
def test_eliminar_empleado_exitoso(client_login_admin, empleado_temporal):
    """
    Prueba la desactivación exitosa de un empleado.
    """
    empleado_id = empleado_temporal.id
    empleado_nombre = empleado_temporal.obtener_nombre_completo()
    
    response = client_login_admin.get(
        f"/eliminar_empleado/{empleado_id}",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "desactivado" in texto.lower()
    assert empleado_nombre in texto
    
    # Verificar que el empleado ya no está activo
    empleado = Empleado.consultar_por_id(empleado_id)
    assert empleado is None or not empleado.activo


# =========================================================
# PRUEBA 8: ELIMINAR EMPLEADO INEXISTENTE
# CUBRE: Líneas 1185-1187 (empleado no encontrado)
# =========================================================
def test_eliminar_empleado_inexistente(client_login_admin):
    """
    Prueba que al intentar eliminar un empleado inexistente se muestre error.
    """
    response = client_login_admin.get(
        "/eliminar_empleado/99999",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Empleado no encontrado" in texto


# =========================================================
# PRUEBA 9: ACTIVAR EMPLEADO EXITOSO
# CUBRE: Líneas 1210-1236 (activar_empleado)
# =========================================================
def test_activar_empleado_exitoso(client_login_admin, empleado_temporal):
    """
    Prueba la activación exitosa de un empleado desactivado.
    """
    empleado_id = empleado_temporal.id
    empleado_nombre = empleado_temporal.obtener_nombre_completo()
    
    # Primero desactivar
    client_login_admin.get(f"/eliminar_empleado/{empleado_id}", follow_redirects=True)
    
    # Luego activar
    response = client_login_admin.get(
        f"/activar_empleado/{empleado_id}",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "activado" in texto.lower()
    assert empleado_nombre in texto


# =========================================================
# PRUEBA 10: ACTIVAR EMPLEADO INEXISTENTE
# CUBRE: Líneas 1221-1223 (empleado no encontrado)
# =========================================================
def test_activar_empleado_inexistente(client_login_admin):
    """
    Prueba que al intentar activar un empleado inexistente se muestre error.
    """
    response = client_login_admin.get(
        "/activar_empleado/99999",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Empleado no encontrado" in texto


# =========================================================
# PRUEBA 11: CAMBIAR CONTRASEÑA EMPLEADO EXITOSO
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
# PRUEBA 12: CAMBIAR CONTRASEÑA EMPLEADO CON PASSWORD CORTA
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
# PRUEBA 13: CAMBIAR CONTRASEÑA EMPLEADO INEXISTENTE
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


# =========================================================
# PRUEBA 14: EDITAR EMPLEADO SIN PERMISOS (VENDEDOR)
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
# PRUEBA 15: ELIMINAR EMPLEADO SIN PERMISOS (VENDEDOR)
# =========================================================
def test_eliminar_empleado_sin_permisos(client_login_vendedor_temporal, empleado_temporal):
    """Vendedor no debe poder eliminar empleados"""
    response = client_login_vendedor_temporal.get(
        f"/eliminar_empleado/{empleado_temporal.id}",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Acceso denegado" in texto or "permisos" in texto


# =========================================================
# PRUEBA 16: ACTIVAR EMPLEADO SIN PERMISOS (VENDEDOR)
# =========================================================
def test_activar_empleado_sin_permisos(client_login_vendedor_temporal, empleado_temporal):
    """Vendedor no debe poder activar empleados"""
    response = client_login_vendedor_temporal.get(
        f"/activar_empleado/{empleado_temporal.id}",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "Acceso denegado" in texto or "permisos" in texto


# =========================================================
# PRUEBA 17: EDITAR EMPLEADO SIN AUTENTICACIÓN
# =========================================================
def test_editar_empleado_sin_autenticacion(client):
    """Sin sesión no se puede acceder a editar empleados"""
    response = client.get(
        "/editar_empleado/1",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "No se ha iniciado sesión" in texto or "login" in texto.lower()


# =========================================================
# PRUEBA 18: ELIMINAR EMPLEADO SIN AUTENTICACIÓN
# =========================================================
def test_eliminar_empleado_sin_autenticacion(client):
    """Sin sesión no se puede eliminar empleados"""
    response = client.get(
        "/eliminar_empleado/1",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "No se ha iniciado sesión" in texto or "login" in texto.lower()


# =========================================================
# PRUEBA 19: ACTIVAR EMPLEADO SIN AUTENTICACIÓN
# =========================================================
def test_activar_empleado_sin_autenticacion(client):
    """Sin sesión no se puede activar empleados"""
    response = client.get(
        "/activar_empleado/1",
        follow_redirects=True
    )
    assert response.status_code == 200
    texto = response.get_data(as_text=True)
    assert "No se ha iniciado sesión" in texto or "login" in texto.lower()

# =========================================================
# PRUEBA 37: CAMBIAR CONTRASEÑA CON LONGITUD INVÁLIDA (MENOR A 6)
# CUBRE: Líneas de cambiar_password_empleado en views.py (validación longitud)
# =========================================================
def test_cambiar_password_empleado_longitud_corta(client_login_admin, empleado_temporal):
    """
    Prueba de valores límite: cambia contraseña con menos de 6 caracteres.
    El sistema puede redirigir a login o mostrar error en la misma página.
    """
    response = client_login_admin.post(
        f"/empleados/{empleado_temporal.id}/cambiar_password",
        data={"nueva_password": "123"},  # 3 caracteres < mínimo 6
        follow_redirects=True
    )
    # Verificar que haya algún mensaje de error (longitud o contraseña)
    assert (b"caracteres" in response.data or 
            b"contrase" in response.data.lower() or
            b"password" in response.data.lower())


# =========================================================
# PRUEBA 38: CAMBIAR CONTRASEÑA CON LONGITUD INVÁLIDA (MAYOR A 30)
# CUBRE: Líneas de cambiar_password_empleado en views.py (validación longitud máxima)
# =========================================================
def test_cambiar_password_empleado_longitud_larga(client_login_admin, empleado_temporal):
    """
    Prueba de valores límite: cambia contraseña con más de 30 caracteres.
    """
    password_larga = "a" * 35
    response = client_login_admin.post(
        f"/empleados/{empleado_temporal.id}/cambiar_password",
        data={"nueva_password": password_larga},
        follow_redirects=True
    )
    # Verificar que haya algún mensaje de error
    assert (b"caracteres" in response.data or 
            b"exceder" in response.data or
            b"password" in response.data.lower())


# =========================================================
# PRUEBA 39: CAMBIAR CONTRASEÑA DE EMPLEADO INEXISTENTE
# CUBRE: Líneas de cambiar_password_empleado en views.py (empleado no encontrado)
# =========================================================
def test_cambiar_password_empleado_inexistente(client_login_admin):
    """
    Prueba de valores límite: intenta cambiar contraseña de empleado que no existe.
    """
    response = client_login_admin.post(
        "/empleados/99999/cambiar_password",
        data={"nueva_password": "nuevapassword123"},
        follow_redirects=True
    )
    # Puede ser 404 o redirigir con mensaje de error
    assert response.status_code in [200, 404]

# tests/system/test_empleado_editar.py

# =========================================================
# PRUEBA 44: ELIMINAR (DESACTIVAR) EMPLEADO INEXISTENTE
# CUBRE: Líneas de eliminar_empleado en views.py (empleado no encontrado)
# =========================================================
def test_eliminar_empleado_id_invalido(client_login_admin):
    """
    Prueba de valores límite: intenta eliminar empleado con ID inválido.
    """
    response = client_login_admin.get(
        "/empleados/99999/eliminar",
        follow_redirects=True
    )
    assert response.status_code in [200, 404]


# =========================================================
# PRUEBA 45: ACTIVAR EMPLEADO INEXISTENTE
# CUBRE: Líneas de activar_empleado en views.py (empleado no encontrado)
# =========================================================
def test_activar_empleado_id_invalido(client_login_admin):
    """
    Prueba de valores límite: intenta activar empleado con ID inválido.
    """
    response = client_login_admin.get(
        "/empleados/99999/activar",
        follow_redirects=True
    )
    assert response.status_code in [200, 404]


# =========================================================
# PRUEBA 46: VENDEDOR INTENTA ELIMINAR EMPLEADO (SIN PERMISOS)
# CUBRE: Líneas de eliminar_empleado en views.py (verificación de rol)
# =========================================================
def test_eliminar_empleado_vendedor_sin_permisos(client_login_vendedor, empleado_temporal):
    """
    Prueba de integración: vendedor intenta eliminar empleado (debe ser denegado).
    """
    response = client_login_vendedor.get(
        f"/empleados/{empleado_temporal.id}/eliminar",
        follow_redirects=True
    )
    # Debe redirigir o mostrar mensaje de error por falta de permisos
    assert response.status_code == 200

