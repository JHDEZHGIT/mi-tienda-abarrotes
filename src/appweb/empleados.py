# src/appweb/empleados.py

from appweb.postgres_db import pgdb
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime


# ============================================
# EXCEPCIONES
# ============================================

class AltaEmpleadoException(Exception):
    pass


class NombreEmpleadoException(Exception):
    pass


class EmailEmpleadoException(Exception):
    pass


class UsernameEmpleadoException(Exception):
    pass


class PasswordEmpleadoException(Exception):
    pass


class EmpleadoNoEncontradoException(Exception):
    pass


class TelefonoEmpleadoException(Exception):
    pass


class FechaEmpleadoException(Exception):
    pass


# ============================================
# EMPLEADO
# ============================================

class Empleado:

    # Longitudes máximas
    MAX_LONGITUD_NOMBRE = 100
    MAX_LONGITUD_EMAIL = 150
    MAX_LONGITUD_USERNAME = 50
    MIN_LONGITUD_PASSWORD = 6
    MAX_LONGITUD_PASSWORD = 30
    MIN_LONGITUD_TELEFONO = 8
    MAX_LONGITUD_TELEFONO = 15

    # Patrones de validación
    PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$")
    PATRON_EMAIL = re.compile(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$")
    PATRON_TELEFONO = re.compile(r"^[0-9]{8,15}$")
    PATRON_USERNAME = re.compile(r"^[a-z0-9_]+$")

    def __init__(
        self,
        id=None,
        nombre=None,
        apellido_paterno=None,
        apellido_materno=None,
        email=None,
        telefono=None,
        fecha_contratacion=None,
        activo=1,
        username=None,
        password=None,
        rol='vendedor'
    ):

        # ====================================
        # NOMBRE
        # ====================================

        if nombre is None or isinstance(nombre, bool) or not isinstance(nombre, str):
            raise NombreEmpleadoException("Error: el nombre del empleado no puede estar vacío")

        if not nombre.strip():
            raise NombreEmpleadoException("Error: el nombre del empleado no puede estar vacío")

        nombre = nombre.strip().title()

        if len(nombre) > self.MAX_LONGITUD_NOMBRE:
            raise NombreEmpleadoException(
                f"Error: el nombre del empleado no puede exceder los {self.MAX_LONGITUD_NOMBRE} caracteres"
            )

        if not self.PATRON_NOMBRE.match(nombre):
            raise NombreEmpleadoException(
                "Error: el nombre solo debe contener letras y espacios"
            )

        # ====================================
        # APELLIDO PATERNO
        # ====================================

        if apellido_paterno is None or isinstance(apellido_paterno, bool) or not isinstance(apellido_paterno, str):
            raise NombreEmpleadoException("Error: el apellido paterno no puede estar vacío")

        if not apellido_paterno.strip():
            raise NombreEmpleadoException("Error: el apellido paterno no puede estar vacío")

        apellido_paterno = apellido_paterno.strip().title()

        if len(apellido_paterno) > self.MAX_LONGITUD_NOMBRE:
            raise NombreEmpleadoException(
                f"Error: el apellido paterno no puede exceder los {self.MAX_LONGITUD_NOMBRE} caracteres"
            )

        if not self.PATRON_NOMBRE.match(apellido_paterno):
            raise NombreEmpleadoException(
                "Error: el apellido paterno solo debe contener letras y espacios"
            )

        # ====================================
        # APELLIDO MATERNO (opcional)
        # ====================================

        if apellido_materno:
            if not isinstance(apellido_materno, str):
                raise NombreEmpleadoException("Error: el apellido materno debe ser texto")

            apellido_materno = apellido_materno.strip().title()

            if len(apellido_materno) > self.MAX_LONGITUD_NOMBRE:
                raise NombreEmpleadoException(
                    f"Error: el apellido materno no puede exceder los {self.MAX_LONGITUD_NOMBRE} caracteres"
                )

            if not self.PATRON_NOMBRE.match(apellido_materno):
                raise NombreEmpleadoException(
                    "Error: el apellido materno solo debe contener letras y espacios"
                )

        # ====================================
        # EMAIL
        # ====================================

        if email is None or isinstance(email, bool) or not isinstance(email, str):
            raise EmailEmpleadoException("Error: el correo electrónico no puede estar vacío")

        if not email.strip():
            raise EmailEmpleadoException("Error: el correo electrónico no puede estar vacío")

        email = email.strip().lower()

        if len(email) > self.MAX_LONGITUD_EMAIL:
            raise EmailEmpleadoException(
                f"Error: el correo electrónico no puede exceder los {self.MAX_LONGITUD_EMAIL} caracteres"
            )

        # Validación mejorada de email
        if not self.PATRON_EMAIL.match(email):
            raise EmailEmpleadoException(
                "Error: formato de correo electrónico inválido. Ejemplo: nombre@dominio.com"
            )

        # Validación adicional: partes del email no vacías
        partes = email.split('@')
        if len(partes) != 2:
            raise EmailEmpleadoException("Error: formato de correo electrónico inválido")
        
        nombre_local, dominio = partes
        if not nombre_local or not dominio:
            raise EmailEmpleadoException("Error: formato de correo electrónico inválido")
        
        if '.' not in dominio:
            raise EmailEmpleadoException("Error: el dominio del correo debe contener un punto")

        # ====================================
        # TELÉFONO (opcional)
        # ====================================

        if telefono:
            if not isinstance(telefono, str):
                raise TelefonoEmpleadoException("Error: el teléfono debe ser texto")

            telefono = telefono.strip()

            if not self.PATRON_TELEFONO.match(telefono):
                raise TelefonoEmpleadoException(
                    f"Error: formato de teléfono inválido. Debe contener {self.MIN_LONGITUD_TELEFONO} a {self.MAX_LONGITUD_TELEFONO} dígitos numéricos"
                )

        # ====================================
        # FECHA DE CONTRATACIÓN
        # ====================================

        if fecha_contratacion:
            try:
                if isinstance(fecha_contratacion, str):
                    datetime.strptime(fecha_contratacion, '%Y-%m-%d')
                elif isinstance(fecha_contratacion, datetime):
                    fecha_contratacion = fecha_contratacion.strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                raise FechaEmpleadoException(
                    "Error: formato de fecha inválido. Use el formato AAAA-MM-DD"
                )

        # ====================================
        # USERNAME
        # ====================================

        if username is None or isinstance(username, bool) or not isinstance(username, str):
            raise UsernameEmpleadoException("Error: el nombre de usuario no puede estar vacío")

        if not username.strip():
            raise UsernameEmpleadoException("Error: el nombre de usuario no puede estar vacío")

        username = username.strip().lower()

        if len(username) > self.MAX_LONGITUD_USERNAME:
            raise UsernameEmpleadoException(
                f"Error: el nombre de usuario no puede exceder los {self.MAX_LONGITUD_USERNAME} caracteres"
            )

        if not self.PATRON_USERNAME.match(username):
            raise UsernameEmpleadoException(
                "Error: el nombre de usuario solo puede contener letras minúsculas, números y guión bajo"
            )

        # ====================================
        # PASSWORD
        # ====================================

        # ====================================
        # PASSWORD
        # ====================================

        if password is None:
            password = 'vendedor123'
        
        if not isinstance(password, str):
            raise PasswordEmpleadoException("Error: la contraseña debe ser texto")
        
        password = password.strip()
        
        if not password:
            raise PasswordEmpleadoException("Error: la contraseña no puede estar vacía")
        
        if len(password) < self.MIN_LONGITUD_PASSWORD:
            raise PasswordEmpleadoException(
                f"Error: la contraseña debe tener al menos {self.MIN_LONGITUD_PASSWORD} caracteres"
            )
        
        if len(password) > self.MAX_LONGITUD_PASSWORD:
            raise PasswordEmpleadoException(
                f"Error: la contraseña no puede exceder los {self.MAX_LONGITUD_PASSWORD} caracteres"
            )
        
        # ====================================
        # ROL
        # ====================================

        if rol is None:
            rol = 'vendedor'

        if rol not in ['vendedor', 'admin']:
            raise ValueError(f"Error: rol inválido. Opciones: vendedor, admin")

        # ====================================
        # ACTIVO
        # ====================================

        try:
            activo = int(activo) if activo is not None else 1
        except (ValueError, TypeError):
            activo = 1

        # ====================================
        # ASIGNACIÓN
        # ====================================

        self.id = id
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.email = email
        self.telefono = telefono
        self.fecha_contratacion = fecha_contratacion
        self.activo = activo
        self.username = username
        self.password = generate_password_hash(password)
        self.rol = rol

    def obtener_nombre_completo(self):
        """Retorna el nombre completo del empleado"""
        nombre_completo = f"{self.nombre} {self.apellido_paterno}"
        if self.apellido_materno:
            nombre_completo += f" {self.apellido_materno}"
        return nombre_completo

    # ========================================
    # INSERTAR
    # ========================================

    def insertar(self):

        try:

            with pgdb.get_cursor() as cur:

                cur.execute(
                    """
                    INSERT INTO empleados
                    (
                        nombre,
                        apellido_paterno,
                        apellido_materno,
                        email,
                        telefono,
                        fecha_contratacion,
                        activo,
                        username,
                        password,
                        rol
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        self.nombre,
                        self.apellido_paterno,
                        self.apellido_materno,
                        self.email,
                        self.telefono,
                        self.fecha_contratacion,
                        self.activo,
                        self.username,
                        self.password,
                        self.rol
                    )
                )

                self.id = cur.fetchone()[0]

            return self.id

        except Exception as e:
            error_msg = str(e).lower()
            if "email" in error_msg:
                raise EmailEmpleadoException(
                    f"Error: ya existe un empleado con el correo electrónico '{self.email}'"
                )
            elif "username" in error_msg:
                raise UsernameEmpleadoException(
                    f"Error: ya existe un empleado con el nombre de usuario '{self.username}'"
                )
            raise AltaEmpleadoException(f"Error al insertar el empleado: {str(e)}")

    # ========================================
    # ACTUALIZAR
    # ========================================

    def actualizar(self):

        try:

            with pgdb.get_cursor() as cur:

                cur.execute(
                    """
                    UPDATE empleados
                    SET nombre = %s,
                        apellido_paterno = %s,
                        apellido_materno = %s,
                        email = %s,
                        telefono = %s,
                        fecha_contratacion = %s,
                        activo = %s,
                        username = %s,
                        rol = %s
                    WHERE id = %s
                    """,
                    (
                        self.nombre,
                        self.apellido_paterno,
                        self.apellido_materno,
                        self.email,
                        self.telefono,
                        self.fecha_contratacion,
                        self.activo,
                        self.username,
                        self.rol,
                        self.id
                    )
                )

            return True

        except Exception as e:
            raise AltaEmpleadoException(f"Error al actualizar el empleado: {str(e)}")

    # ========================================
    # ACTUALIZAR CONTRASEÑA
    # ========================================

    def actualizar_password(self, nueva_password):

        if nueva_password is None:
            raise PasswordEmpleadoException("Error: la contraseña no puede estar vacía")
        
        if not isinstance(nueva_password, str):
            raise PasswordEmpleadoException("Error: la contraseña debe ser texto")
        
        nueva_password = nueva_password.strip()
        
        if not nueva_password:
            raise PasswordEmpleadoException("Error: la contraseña no puede estar vacía")
        
        if len(nueva_password) < self.MIN_LONGITUD_PASSWORD:
            raise PasswordEmpleadoException(
                f"Error: la contraseña debe tener al menos {self.MIN_LONGITUD_PASSWORD} caracteres"
            )
        
        if len(nueva_password) > self.MAX_LONGITUD_PASSWORD:
            raise PasswordEmpleadoException(
                f"Error: la contraseña no puede exceder los {self.MAX_LONGITUD_PASSWORD} caracteres"
            )

        try:
            from werkzeug.security import generate_password_hash
            
            nueva_password_hash = generate_password_hash(nueva_password)

            with pgdb.get_cursor() as cur:
                cur.execute(
                    "UPDATE empleados SET password = %s WHERE id = %s",
                    (nueva_password_hash, self.id)
                )

            self.password = nueva_password_hash
            
            return True

        except PasswordEmpleadoException:
            raise
        except Exception as e:
            raise AltaEmpleadoException(f"Error al actualizar la contraseña: {str(e)}")

    # ========================================
    # ELIMINAR (DESACTIVAR)
    # ========================================

    def eliminar(self):

        try:

            with pgdb.get_cursor() as cur:

                cur.execute(
                    "UPDATE empleados SET activo = 0 WHERE id = %s",
                    (self.id,)
                )

            return True

        except Exception as e:
            raise AltaEmpleadoException(f"Error al desactivar el empleado: {str(e)}")

    # ========================================
    # ACTIVAR
    # ========================================

    def activar(self):

        try:

            with pgdb.get_cursor() as cur:

                cur.execute(
                    "UPDATE empleados SET activo = 1 WHERE id = %s",
                    (self.id,)
                )

            return True

        except Exception as e:
            raise AltaEmpleadoException(f"Error al activar el empleado: {str(e)}")

    # ========================================
    # CONSULTAR TODOS
    # ========================================

    @classmethod
    def consultar_todos(cls, solo_activos=True):

        with pgdb.get_cursor() as cur:

            if solo_activos:
                cur.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        apellido_paterno,
                        apellido_materno,
                        email,
                        telefono,
                        fecha_contratacion,
                        activo,
                        username,
                        rol
                    FROM empleados
                    WHERE activo = 1
                    ORDER BY nombre, apellido_paterno
                    """
                )
            else:
                cur.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        apellido_paterno,
                        apellido_materno,
                        email,
                        telefono,
                        fecha_contratacion,
                        activo,
                        username,
                        rol
                    FROM empleados
                    ORDER BY activo DESC, nombre, apellido_paterno
                    """
                )

            resultados = []

            for row in cur.fetchall():

                emp = Empleado(
                    id=row[0],
                    nombre=row[1],
                    apellido_paterno=row[2],
                    apellido_materno=row[3],
                    email=row[4],
                    telefono=row[5],
                    fecha_contratacion=row[6],
                    activo=row[7],
                    username=row[8],
                    password=None,
                    rol=row[9]
                )

                resultados.append(emp)

            return resultados

    # ========================================
    # CONSULTAR POR ID
    # ========================================

    @classmethod
    def consultar_por_id(cls, empleado_id):

        if empleado_id is None:
            return None

        try:
            empleado_id = int(empleado_id)
        except (ValueError, TypeError):
            return None

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    nombre,
                    apellido_paterno,
                    apellido_materno,
                    email,
                    telefono,
                    fecha_contratacion,
                    activo,
                    username,
                    rol
                FROM empleados
                WHERE id = %s
                """,
                (empleado_id,)
            )

            row = cur.fetchone()

            if row:
                # Crear empleado sin pasar por __init__
                empleado = cls.__new__(cls)
                empleado.id = row[0]
                empleado.nombre = row[1]
                empleado.apellido_paterno = row[2]
                empleado.apellido_materno = row[3]
                empleado.email = row[4]
                empleado.telefono = row[5]
                empleado.fecha_contratacion = row[6]
                empleado.activo = row[7]
                empleado.username = row[8]
                empleado.password = None
                empleado.rol = row[9]
                return empleado

            return None

    # ========================================
    # VERIFICAR CREDENCIALES
    # ========================================

    @classmethod
    def verificar_credenciales(cls, username, password):

        from werkzeug.security import check_password_hash

        if username is None:
            return None
        
        if not isinstance(username, str):
            return None
        
        if not username.strip():
            return None
        
        if password is None:
            return None
        
        if not isinstance(password, str):
            return None
        
        if not password.strip():
            return None
        
        username = username.strip().lower()
        
        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    nombre,
                    apellido_paterno,
                    apellido_materno,
                    email,
                    telefono,
                    fecha_contratacion,
                    activo,
                    username,
                    password,
                    rol
                FROM empleados
                WHERE username = %s AND activo = 1
                """,
                (username,)
            )

            row = cur.fetchone()

            if row and check_password_hash(row[9], password):

                # Crear empleado sin pasar por __init__ para evitar validaciones del hash
                empleado = cls.__new__(cls)
                empleado.id = row[0]
                empleado.nombre = row[1]
                empleado.apellido_paterno = row[2]
                empleado.apellido_materno = row[3]
                empleado.email = row[4]
                empleado.telefono = row[5]
                empleado.fecha_contratacion = row[6]
                empleado.activo = row[7]
                empleado.username = row[8]
                empleado.password = row[9]  # El hash, no texto plano
                empleado.rol = row[10]
                return empleado

            return None