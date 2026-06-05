# tests/helpers/empleados_factory.py

from tests.helpers.fechas_helper import fecha_hace_30_anios


# EMPLEADO VALIDO (VENDEDOR)
# =========================================================
def empleado_valido():
    return {
        "nombre": "Juan",
        "apellido_paterno": "Perez",
        "apellido_materno": "Gomez",
        "email": "juan.perez@example.com",
        "telefono": "5512345678",
        "fecha_contratacion": fecha_hace_30_anios(),
        "username": "juan_perez",
        "password": "vendedor123",
        "rol": "vendedor"
    }


# EMPLEADO VALIDO ADMIN
# =========================================================
def empleado_admin_valido():
    return {
        "nombre": "Admin",
        "apellido_paterno": "Sistema",
        "apellido_materno": "",
        "email": "admin@example.com",
        "telefono": "5512345678",
        "fecha_contratacion": fecha_hace_30_anios(),
        "username": "admin_sistema",
        "password": "admin123",
        "rol": "admin"
    }


# EMPLEADO NOMBRE INVALIDO
# =========================================================
def empleado_nombre_invalido():
    data = empleado_valido()
    data["nombre"] = ""
    return data


# EMPLEADO APELLIDO_PATERNO INVALIDO
# =========================================================
def empleado_apellido_paterno_invalido():
    data = empleado_valido()
    data["apellido_paterno"] = ""
    return data


# EMPLEADO EMAIL INVALIDO
# =========================================================
def empleado_email_invalido():
    data = empleado_valido()
    data["email"] = "email_invalido"
    return data


# EMPLEADO USERNAME INVALIDO
# =========================================================
def empleado_username_invalido():
    data = empleado_valido()
    data["username"] = "usuario invalido!"
    return data


# EMPLEADO PASSWORD CORTA
# =========================================================
def empleado_password_corta():
    data = empleado_valido()
    data["password"] = "123"
    return data