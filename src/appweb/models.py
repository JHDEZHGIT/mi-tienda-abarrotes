# src/appweb/models.py

from appweb.postgres_db import pgdb
from datetime import datetime, date
import re


# ============================================
# EXCEPCIONES
# ============================================

class AltaProductoException(Exception):
    pass


class NombreProductoException(Exception):
    pass


class PrecioProductoException(Exception):
    pass


class StockProductoException(Exception):
    pass


class TipoDescuentoException(Exception):
    pass


class DescuentoValorException(Exception):
    pass


class VentaException(Exception):
    pass


class DBException(Exception):
    pass


class UsuarioException(Exception):
    pass


# ============================================
# PRODUCTO
# ============================================

class Producto:

    # Tipos de descuento válidos
    TIPOS_DESCUENTO_VALIDOS = ['ninguno', 'porcentaje', '2x1', '3x2', '4x3', '5x4']

    # Porcentajes válidos (5% a 90% con saltos de 5)
    PORCENTAJES_VALIDOS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]

    # Longitud máxima del nombre
    MAX_LONGITUD_NOMBRE = 255

    # Precio máximo permitido
    PRECIO_MAXIMO = 999999.99

    # Stock máximo permitido
    STOCK_MAXIMO = 999999

    def __init__(
        self,
        id=None,
        nombre=None,
        precio=None,
        stock=None,
        aplica_promocion=None,
        tipo_descuento='ninguno',
        descuento_valor=0
    ):

        # ====================================
        # NOMBRE
        # ====================================

        if (
            nombre is None
            or
            isinstance(nombre, bool)
            or
            not isinstance(nombre, str)
            or
            nombre.strip() == ""
        ):

            raise NombreProductoException(
                "Error: el nombre del producto no puede estar vacío"
            )

        nombre = nombre.strip()

        if len(nombre) > self.MAX_LONGITUD_NOMBRE:

            raise NombreProductoException(
                f"Error: el nombre del producto no puede exceder los {self.MAX_LONGITUD_NOMBRE} caracteres"
            )

        # Permitir letras, números, espacios, guiones y puntos
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s\-\.]+$", nombre):
            raise NombreProductoException(
                "Error: nombre inválido. Solo se permiten letras, números, espacios, guiones y puntos"
            )

        # ====================================
        # PRECIO
        # ====================================

        if precio is None:

            raise PrecioProductoException(
                "Error: el precio del producto no puede estar vacío"
            )

        precio = str(precio).strip()

        if precio == "":

            raise PrecioProductoException(
                "Error: el precio del producto no puede estar vacío"
            )

        precio = precio.replace(",", "")

        try:

            precio = float(precio)

        except (ValueError, TypeError):

            raise PrecioProductoException(
                "Error: el precio debe ser un número válido"
            )

        if precio <= 0:

            raise PrecioProductoException(
                "Error: el precio debe ser mayor que cero"
            )

        if precio > self.PRECIO_MAXIMO:

            raise PrecioProductoException(
                f"Error: el precio no puede exceder {self.PRECIO_MAXIMO:,.2f}"
            )

        # ====================================
        # STOCK
        # ====================================

        if stock is None:

            raise StockProductoException(
                "Error: el stock del producto no puede estar vacío"
            )

        try:

            stock = int(stock)

        except (ValueError, TypeError):

            raise StockProductoException(
                "Error: el stock debe ser un número entero válido"
            )

        if stock < 0:

            raise StockProductoException(
                "Error: el stock no puede ser negativo"
            )

        if stock > self.STOCK_MAXIMO:

            raise StockProductoException(
                f"Error: el stock no puede exceder {self.STOCK_MAXIMO:,} unidades"
            )

        # ====================================
        # TIPO DESCUENTO Y VALOR
        # ====================================

        # Para compatibilidad con versión anterior
        if aplica_promocion is not None and aplica_promocion == 1 and tipo_descuento == 'ninguno':
            tipo_descuento = '2x1'
            descuento_valor = 0

        if tipo_descuento is None:
            tipo_descuento = 'ninguno'

        if tipo_descuento not in self.TIPOS_DESCUENTO_VALIDOS:
            raise TipoDescuentoException(
                f"Error: tipo de descuento inválido. Opciones: {', '.join(self.TIPOS_DESCUENTO_VALIDOS)}"
            )

        try:
            descuento_valor = int(descuento_valor) if descuento_valor is not None else 0
        except (ValueError, TypeError):
            raise DescuentoValorException(
                "Error: el valor de descuento debe ser un número entero válido"
            )

        if tipo_descuento == 'porcentaje':
            if descuento_valor not in self.PORCENTAJES_VALIDOS:
                raise DescuentoValorException(
                    f"Error: porcentaje inválido. Debe ser uno de: {', '.join(map(str, self.PORCENTAJES_VALIDOS))}%"
                )
        else:
            if descuento_valor != 0:
                descuento_valor = 0

        # ====================================
        # ASIGNACIÓN
        # ====================================

        self.id = id
        self.nombre = nombre
        self.precio = round(precio, 2)
        self.stock = stock
        # aplica_promocion es 1 si hay descuento (excepto 'ninguno')
        self.aplica_promocion = 1 if tipo_descuento != 'ninguno' else 0
        self.tipo_descuento = tipo_descuento
        self.descuento_valor = descuento_valor

    def obtener_descripcion_descuento(self):
        """Retorna la descripción legible del descuento"""

        from appweb.descuentos import CalculadorDescuento
        return CalculadorDescuento.obtener_descripcion(self.tipo_descuento, self.descuento_valor)

    # ========================================
    # VALIDAR DUPLICADOS
    # ========================================
    
    @classmethod
    def existe_nombre(cls, nombre, id_excluir=None):
        """Verifica si ya existe un producto con el mismo nombre"""
        with pgdb.get_cursor() as cur:
            if id_excluir:
                cur.execute(
                    "SELECT id FROM productos WHERE nombre ILIKE %s AND id != %s",
                    (nombre.strip(), id_excluir)
                )
            else:
                cur.execute(
                    "SELECT id FROM productos WHERE nombre ILIKE %s",
                    (nombre.strip(),)
                )
            return cur.fetchone() is not None
    
    
    # ========================================
    # INSERTAR
    # ========================================

    def insertar(self):

        try:

            with pgdb.get_cursor() as cur:

                # Validar nombre único
                if Producto.existe_nombre(self.nombre):
                    raise AltaProductoException(
                        f"Ya existe un producto con el nombre '{self.nombre}'. "
                        "Use la opción de edición para incrementar el stock en lugar de crear uno nuevo."
                    )

                cur.execute(
                    """
                    INSERT INTO productos
                    (
                        nombre,
                        precio,
                        stock,
                        aplica_promocion,
                        tipo_descuento,
                        descuento_valor
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        self.nombre,
                        self.precio,
                        self.stock,
                        self.aplica_promocion,
                        self.tipo_descuento,
                        self.descuento_valor
                    )
                )

                self.id = cur.fetchone()[0]

            return self.id

        except AltaProductoException:
            raise

        except Exception as e:
            raise AltaProductoException(
                f"Error al insertar el producto: {str(e)}"
            )

    # ========================================
    # ACTUALIZAR
    # ========================================

    def actualizar(self):

        try:

            with pgdb.get_cursor() as cur:

                # Validar nombre único (excluyendo el producto actual)
                if Producto.existe_nombre(self.nombre, self.id):
                    raise DBException(
                        f"Ya existe otro producto con el nombre '{self.nombre}'. "
                        "Los nombres de producto deben ser únicos."
                    )

                cur.execute(
                    """
                    UPDATE productos
                    SET nombre = %s,
                        precio = %s,
                        stock = %s,
                        aplica_promocion = %s,
                        tipo_descuento = %s,
                        descuento_valor = %s
                    WHERE id = %s
                    """,
                    (
                        self.nombre,
                        self.precio,
                        self.stock,
                        self.aplica_promocion,
                        self.tipo_descuento,
                        self.descuento_valor,
                        self.id
                    )
                )

            return True

        except DBException:
            raise

        except Exception as e:
            raise DBException(
                f"Error al actualizar el producto: {str(e)}"
            )

    # ========================================
    # ELIMINAR
    # ========================================

    def eliminar(self):

        try:

            with pgdb.get_cursor() as cur:

                cur.execute(
                    "SELECT COUNT(*) FROM ventas WHERE producto_id = %s",
                    (self.id,)
                )
                ventas_count = cur.fetchone()[0]

                if ventas_count > 0:
                    raise DBException(
                        f"No se puede eliminar el producto porque tiene {ventas_count} venta(s) asociada(s). El historial de ventas no puede ser modificado."
                    )

                cur.execute(
                    "DELETE FROM productos WHERE id = %s",
                    (self.id,)
                )

            return True

        except DBException:
            raise

        except Exception as e:
            raise DBException(
                f"Error al eliminar el producto: {str(e)}"
            )

    # ========================================
    # CONSULTAR POR ID - CORREGIDO
    # ========================================

    @classmethod
    def consultar_por_id(cls, producto_id):
        """Consulta un producto por su ID"""
        
        if producto_id is None:
            return None
        
        try:
            producto_id = int(producto_id)
        except (ValueError, TypeError):
            return None
        
        with pgdb.get_cursor() as cur:
            cur.execute("""
                SELECT
                    id,
                    nombre,
                    precio,
                    stock,
                    COALESCE(aplica_promocion, 0) as aplica_promocion,
                    COALESCE(tipo_descuento, 'ninguno') as tipo_descuento,
                    COALESCE(descuento_valor, 0) as descuento_valor
                FROM productos
                WHERE id = %s
            """, (producto_id,))
            
            row = cur.fetchone()
            
            if row:
                return Producto(
                    id=row[0],
                    nombre=row[1],
                    precio=str(row[2]),
                    stock=row[3],
                    aplica_promocion=row[4],
                    tipo_descuento=row[5],
                    descuento_valor=row[6]
                )
            
            return None

    # ========================================
    # CONSULTAR TODO
    # ========================================

    @classmethod
    def consultar_todo(cls):

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    nombre,
                    precio,
                    stock,
                    COALESCE(aplica_promocion, 0) as aplica_promocion,
                    COALESCE(tipo_descuento, 'ninguno') as tipo_descuento,
                    COALESCE(descuento_valor, 0) as descuento_valor
                FROM productos
                ORDER BY id
                """
            )

            resultados = []

            for row in cur.fetchall():

                prod = Producto(
                    id=row[0],
                    nombre=row[1],
                    precio=str(row[2]),
                    stock=row[3],
                    aplica_promocion=row[4],
                    tipo_descuento=row[5],
                    descuento_valor=row[6]
                )

                resultados.append(prod)

            return resultados

    # ========================================
    # CONSULTAR POR NOMBRE
    # ========================================

    @classmethod
    def consultar_por_nombre(cls, nombre):

        if not nombre or not nombre.strip():
            return []

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    nombre,
                    precio,
                    stock,
                    COALESCE(aplica_promocion, 0) as aplica_promocion,
                    COALESCE(tipo_descuento, 'ninguno') as tipo_descuento,
                    COALESCE(descuento_valor, 0) as descuento_valor
                FROM productos
                WHERE nombre ILIKE %s
                ORDER BY nombre
                """,
                (f"%{nombre.strip()}%",)
            )

            resultados = []

            for row in cur.fetchall():

                prod = Producto(
                    id=row[0],
                    nombre=row[1],
                    precio=str(row[2]),
                    stock=row[3],
                    aplica_promocion=row[4],
                    tipo_descuento=row[5],
                    descuento_valor=row[6]
                )

                resultados.append(prod)

            return resultados

    # ========================================
    # CONSULTAR CON STOCK BAJO
    # ========================================

    @classmethod
    def consultar_stock_bajo(cls, limite=10):

        if limite < 1:
            limite = 10

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    nombre,
                    precio,
                    stock,
                    COALESCE(aplica_promocion, 0) as aplica_promocion,
                    COALESCE(tipo_descuento, 'ninguno') as tipo_descuento,
                    COALESCE(descuento_valor, 0) as descuento_valor
                FROM productos
                WHERE stock <= %s
                ORDER BY stock
                """,
                (limite,)
            )

            resultados = []

            for row in cur.fetchall():

                prod = Producto(
                    id=row[0],
                    nombre=row[1],
                    precio=str(row[2]),
                    stock=row[3],
                    aplica_promocion=row[4],
                    tipo_descuento=row[5],
                    descuento_valor=row[6]
                )

                resultados.append(prod)

            return resultados

    # ========================================
    # REPORTE DE STOCK (MENOR A MAYOR)
    # ========================================

    @classmethod
    def consultar_reporte_stock(cls):

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    nombre,
                    precio,
                    stock,
                    COALESCE(aplica_promocion, 0) as aplica_promocion,
                    COALESCE(tipo_descuento, 'ninguno') as tipo_descuento,
                    COALESCE(descuento_valor, 0) as descuento_valor
                FROM productos
                ORDER BY stock ASC
                """
            )

            resultados = []

            for row in cur.fetchall():

                prod = Producto(
                    id=row[0],
                    nombre=row[1],
                    precio=str(row[2]),
                    stock=row[3],
                    aplica_promocion=row[4],
                    tipo_descuento=row[5],
                    descuento_valor=row[6]
                )

                resultados.append(prod)

            return resultados


# ============================================
# VENTA
# ============================================

class Venta:

    # Cantidad máxima permitida por venta
    CANTIDAD_MAXIMA = 999999

    def __init__(
        self,
        id=None,
        producto_id=None,
        cantidad=None,
        total=None,
        fecha=None
    ):

        # ====================================
        # PRODUCTO ID
        # ====================================

        if producto_id is None:

            raise VentaException(
                "Error: producto no especificado"
            )

        try:

            producto_id = int(producto_id)

        except (ValueError, TypeError):

            raise VentaException(
                "Error: identificador de producto inválido"
            )

        # ====================================
        # CANTIDAD
        # ====================================

        if cantidad is None:

            raise VentaException(
                "Error: cantidad vacía"
            )

        try:

            cantidad = int(cantidad)

        except (ValueError, TypeError):

            raise VentaException(
                "Error: cantidad inválida"
            )

        if cantidad <= 0:

            raise VentaException(
                "Error: la cantidad debe ser mayor que cero"
            )

        if cantidad > self.CANTIDAD_MAXIMA:

            raise VentaException(
                f"Error: cantidad demasiado grande. Máximo {self.CANTIDAD_MAXIMA:,}"
            )

        # ====================================
        # TOTAL
        # ====================================

        if total is None:

            raise VentaException(
                "Error: total vacío"
            )

        try:

            total = float(total)

        except (ValueError, TypeError):

            raise VentaException(
                "Error: total inválido"
            )

        if total < 0:

            raise VentaException(
                "Error: el total no puede ser negativo"
            )

        # ====================================
        # ASIGNACIÓN
        # ====================================

        self.id = id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.total = round(total, 2)
        self.fecha = fecha

    # ========================================
    # REGISTRAR VENTA
    # ========================================

    def registrar(self):

        try:

            with pgdb.get_cursor() as cur:

                # Verificar que el producto existe y tiene stock suficiente
                cur.execute(
                    "SELECT stock, nombre FROM productos WHERE id = %s",
                    (self.producto_id,)
                )
                producto = cur.fetchone()

                if not producto:
                    raise VentaException(
                        f"El producto con ID {self.producto_id} no existe"
                    )

                stock_actual, nombre_producto = producto

                if stock_actual < self.cantidad:
                    raise VentaException(
                        f"Stock insuficiente para '{nombre_producto}'. "
                        f"Disponible: {stock_actual}, Solicitado: {self.cantidad}"
                    )

                cur.execute(
                    """
                    INSERT INTO ventas
                    (
                        producto_id,
                        cantidad,
                        total
                    )
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (
                        self.producto_id,
                        self.cantidad,
                        self.total
                    )
                )

                self.id = cur.fetchone()[0]

                cur.execute(
                    """
                    UPDATE productos
                    SET stock = stock - %s
                    WHERE id = %s
                    """,
                    (self.cantidad, self.producto_id)
                )

            return self.id

        except VentaException:
            raise

        except Exception as e:
            raise VentaException(
                f"Error al registrar la venta: {str(e)}"
            )

    # ========================================
    # CONSULTAR HISTORIAL
    # ========================================

    @classmethod
    def consultar_historial(cls):

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT
                    ventas.id,
                    productos.nombre,
                    ventas.cantidad,
                    ventas.total,
                    ventas.fecha
                FROM ventas
                JOIN productos ON ventas.producto_id = productos.id
                ORDER BY ventas.id DESC
                """
            )

            resultados = []

            for row in cur.fetchall():
                # Usar un diccionario para evitar problemas con el constructor de Venta
                venta_info = {
                    'id': row[0],
                    'nombre_producto': row[1],
                    'cantidad': row[2],
                    'total': float(row[3]) if row[3] else 0,
                    'fecha': row[4]
                }
                resultados.append(venta_info)

            return resultados

    # ========================================
    # TOTAL VENTAS
    # ========================================

    @classmethod
    def total_ventas(cls):

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT COALESCE(SUM(total), 0)
                FROM ventas
                """
            )

            return cur.fetchone()[0]


# ============================================
# USUARIO
# ============================================

class Usuario:

    # Longitud máxima del nombre de usuario
    MAX_LONGITUD_USERNAME = 100

    # Patrón para nombre de usuario (letras, números, guión bajo)
    PATRON_USERNAME = re.compile(r"^[A-Za-z0-9_]+$")

    # Roles válidos
    ROLES_VALIDOS = ["admin", "cliente"]

    def __init__(
        self,
        id=None,
        username=None,
        password=None,
        rol=None
    ):

        # ====================================
        # USERNAME
        # ====================================

        # Convertir a string si viene de otro tipo
        if username is not None and not isinstance(username, str):
            username = str(username)

        if (
            username is None
            or
            isinstance(username, bool)
            or
            not isinstance(username, str)
            or
            username.strip() == ""
        ):

            raise UsuarioException(
                "Error: el nombre de usuario no puede estar vacío"
            )

        username = username.strip().lower()  # Convertir a minúsculas aquí

        if len(username) > self.MAX_LONGITUD_USERNAME:

            raise UsuarioException(
                f"Error: el nombre de usuario no puede exceder los {self.MAX_LONGITUD_USERNAME} caracteres"
            )

        if not self.PATRON_USERNAME.match(username):

            raise UsuarioException(
                "Error: nombre de usuario inválido. Solo se permiten letras, números y guión bajo"
            )

        # ====================================
        # PASSWORD
        # ====================================

        if (
            password is None
            or
            not isinstance(password, str)
            or
            password.strip() == ""
        ):

            raise UsuarioException(
                "Error: la contraseña no puede estar vacía"
            )

        # ====================================
        # ROL
        # ====================================

        if rol is None:
            rol = "cliente"

        if rol not in self.ROLES_VALIDOS:

            raise UsuarioException(
                f"Error: rol inválido. Opciones: {', '.join(self.ROLES_VALIDOS)}"
            )

        # ====================================
        # ASIGNACIÓN
        # ====================================

        self.id = id
        self.username = username
        self.password = password
        self.rol = rol

    # ========================================
    # VERIFICAR CREDENCIALES
    # ========================================

    @classmethod
    def verificar_credenciales(cls, username, password):

        from werkzeug.security import check_password_hash

        if not username or not username.strip():
            return None

        if not password or not password.strip():
            return None

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT id, username, password, rol
                FROM usuarios
                WHERE username = %s
                """,
                (username.strip(),)
            )

            row = cur.fetchone()

            if row and check_password_hash(row[2], password):

                return Usuario(
                    id=row[0],
                    username=row[1],
                    password=row[2],
                    rol=row[3]
                )

            return None

    # ========================================
    # CONSULTAR POR ID
    # ========================================

    @classmethod
    def consultar_por_id(cls, user_id):

        if user_id is None:
            return None

        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return None

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT id, username, rol
                FROM usuarios
                WHERE id = %s
                """,
                (user_id,)
            )

            row = cur.fetchone()

            if row:
                # Crear usuario sin validación de password
                usuario = cls.__new__(cls)
                usuario.id = row[0]
                usuario.username = row[1]
                usuario.password = None  # No se carga la contraseña
                usuario.rol = row[2]
                return usuario

            return None