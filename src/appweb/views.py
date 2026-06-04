# src/appweb/views.py

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from appweb.models import (
    Producto,
    Venta,
    Usuario,
    AltaProductoException,
    NombreProductoException,
    PrecioProductoException,
    StockProductoException,
    TipoDescuentoException,
    DescuentoValorException,
    VentaException,
    DBException,
    pgdb
)


from appweb.empleados import (
    Empleado,
    AltaEmpleadoException,
    NombreEmpleadoException,
    EmailEmpleadoException,
    UsernameEmpleadoException,
    PasswordEmpleadoException
)

from appweb.descuentos import CalculadorDescuento


# ============================================
# VALIDAR SESION
# ============================================

def validar_sesion():

    if "usuario" not in session:

        flash(
            "No se ha iniciado sesión",
            "danger"
        )

        return False

    return True


# ============================================
# VALIDAR ADMIN
# ============================================

def validar_admin():

    if not validar_sesion():
        return False

    if session.get("rol") != "admin":

        flash(
            "Acceso denegado. Se requieren permisos de administrador",
            "danger"
        )

        return False

    return True


# ============================================
# REGISTRAR RUTAS
# ============================================

def registrar_rutas(app):


    # ========================================
    # LOGIN
    # ========================================

    @app.route("/", methods=["GET", "POST"])
    @app.route("/login", methods=["GET", "POST"])
    def login_home():

        if request.method == "POST":

            username = request.form.get("username")
            password = request.form.get("password")

            # Validaciones de campos vacíos
            if not username or not username.strip():
                flash("El nombre de usuario es requerido", "danger")
                return render_template("login.html"), 401

            if not password or not password.strip():
                flash("La contraseña es requerida", "danger")
                return render_template("login.html"), 401

            # Primero intentar como administrador/cliente de usuarios
            usuario = Usuario.verificar_credenciales(username, password)

            if usuario:
                session["usuario"] = usuario.username
                session["user_id"] = usuario.id
                session["rol"] = usuario.rol
                session.permanent = True

                flash(
                    f"Bienvenido {username}",
                    "success"
                )

                return redirect(
                    url_for("inicio_home")
                )

            # Si no es usuario, intentar como empleado (vendedor o admin)
            empleado = Empleado.verificar_credenciales(username, password)

            if empleado:
                session["usuario"] = empleado.username
                session["user_id"] = empleado.id
                session["empleado_id"] = empleado.id
                session["nombre_empleado"] = empleado.obtener_nombre_completo()
                
                if empleado.rol == 'admin':
                    session["rol"] = 'admin'
                    flash(
                        f"Bienvenido administrador {empleado.obtener_nombre_completo()}",
                        "success"
                    )
                else:
                    session["rol"] = 'vendedor'
                    flash(
                        f"Bienvenido vendedor {empleado.obtener_nombre_completo()}",
                        "success"
                    )
                
                session.permanent = True

                return redirect(
                    url_for("inicio_home")
                )

            flash(
                "Credenciales incorrectas",
                "danger"
            )

            return render_template(
                "login.html"
            ), 401

        return render_template(
            "login.html"
        )


    # ========================================
    # LOGOUT
    # ========================================

    @app.route("/logout")
    def logout():

        session.clear()

        flash(
            "Has cerrado sesión correctamente",
            "success"
        )

        return redirect(
            url_for("login_home")
        )


    # ========================================
    # INICIO
    # ========================================

    @app.route("/inicio")
    def inicio_home():

        if not validar_sesion():

            return redirect(
                url_for("login_home")
            )

        return render_template(
            "inicio.html"
        )


    # ========================================
    # PRODUCTOS (SOLO ADMIN)
    # ========================================

    @app.route("/productos")
    def productos():

        if not validar_admin():

            return redirect(
                url_for("login_home")
            )

        resultados = Producto.consultar_todo()

        return render_template(
            "productos.html",
            productos=resultados
        )


    # ========================================
    # AGREGAR PRODUCTO
    # ========================================
    @app.route("/agregar_producto", methods=["POST"])
    def agregar_producto():

        if not validar_admin():
            return redirect(url_for("login_home"))

        try:
            nombre = request.form.get("nombre")
            precio_str = request.form.get("precio")
            stock_str = request.form.get("stock")
            tipo_descuento = request.form.get("tipo_descuento", "ninguno")
            descuento_valor_str = request.form.get("descuento_valor", 0)

            # ========================================
            # VALIDACIONES DE NOMBRE
            # ========================================
            
            if nombre is None:
                flash("El nombre del producto es requerido", "danger")
                return redirect(url_for("productos"))
            
            if isinstance(nombre, bool):
                flash("El nombre del producto no puede ser un valor booleano", "danger")
                return redirect(url_for("productos"))
            
            if not isinstance(nombre, str):
                flash("El nombre del producto debe ser texto", "danger")
                return redirect(url_for("productos"))
            
            if nombre.strip() == "":
                flash("El nombre del producto no puede estar vacío", "danger")
                return redirect(url_for("productos"))
            
            if len(nombre) > 100:
                flash("El nombre del producto no puede exceder los 100 caracteres", "danger")
                return redirect(url_for("productos"))

            # ========================================
            # VALIDACIONES DE PRECIO
            # ========================================
            
            try:
                precio = float(precio_str) if precio_str else 0
            except (ValueError, TypeError):
                flash("El precio debe ser un número válido", "danger")
                return redirect(url_for("productos"))

            # ========================================
            # VALIDACIONES DE STOCK
            # ========================================
            
            try:
                stock = int(stock_str) if stock_str else 0
            except (ValueError, TypeError):
                flash("El stock debe ser un número entero válido", "danger")
                return redirect(url_for("productos"))

            # ========================================
            # VALIDACIONES DE DESCUENTO
            # ========================================
            
            try:
                descuento_valor = int(descuento_valor_str) if descuento_valor_str else 0
            except (ValueError, TypeError):
                descuento_valor = 0

            nuevo_producto = Producto(
                nombre=nombre.strip(),
                precio=precio,
                stock=stock,
                aplica_promocion=None,
                tipo_descuento=tipo_descuento,
                descuento_valor=descuento_valor
            )

            nuevo_producto.insertar()

            flash(
                f"Producto '{nombre.strip()}' agregado correctamente",
                "success"
            )

        except NombreProductoException as e:
            flash(str(e), "danger")
        except PrecioProductoException as e:
            flash(str(e), "danger")
        except StockProductoException as e:
            flash(str(e), "danger")
        except TipoDescuentoException as e:
            flash(str(e), "danger")
        except DescuentoValorException as e:
            flash(str(e), "danger")
        except AltaProductoException as e:
            flash(str(e), "danger")

        return redirect(url_for("productos"))


    # ========================================
    # ELIMINAR PRODUCTO
    # ========================================
    @app.route("/eliminar_producto/<int:id>")
    def eliminar_producto(id):

        if not validar_admin():
            return redirect(url_for("login_home"))

        try:

            producto = Producto.consultar_por_id(id)

            if not producto:

                flash(
                    "Producto no encontrado",
                    "danger"
                )
                return redirect(url_for("productos"))

            producto.eliminar()

            flash(
                f"Producto '{producto.nombre}' eliminado correctamente",
                "success"
            )

        except DBException as e:

            flash(str(e), "warning")

        except Exception as e:

            flash(f"Error inesperado al eliminar el producto: {str(e)}", "danger")

        return redirect(url_for("productos"))


    # ========================================
    # EDITAR PRODUCTO (FORMULARIO)
    # ========================================
    @app.route("/editar_producto/<int:id>")
    def editar_producto(id):

        if not validar_admin():
            return redirect(url_for("login_home"))

        producto = Producto.consultar_por_id(id)

        if not producto:

            flash(
                "Producto no encontrado",
                "danger"
            )

            return redirect(url_for("productos"))

        return render_template(
            "editar_producto.html",
            producto=producto
        )


    # ========================================
    # ACTUALIZAR PRODUCTO
    # ========================================
    @app.route("/actualizar_producto", methods=["POST"])
    def actualizar_producto():

        if not validar_admin():
            return redirect(url_for("login_home"))

        try:
            id_prod_str = request.form.get("id")
            nombre = request.form.get("nombre")
            precio_str = request.form.get("precio")
            stock_str = request.form.get("stock")
            tipo_descuento = request.form.get("tipo_descuento", "ninguno")
            descuento_valor_str = request.form.get("descuento_valor", 0)

            # ========================================
            # VALIDACIONES DE ID
            # ========================================
            
            try:
                id_prod = int(id_prod_str) if id_prod_str else 0
            except (ValueError, TypeError):
                flash("Identificador de producto inválido", "danger")
                return redirect(url_for("productos"))

            # ========================================
            # VALIDACIONES DE NOMBRE
            # ========================================
            
            if nombre is None:
                flash("El nombre del producto es requerido", "danger")
                return redirect(url_for("productos"))
            
            if isinstance(nombre, bool):
                flash("El nombre del producto no puede ser un valor booleano", "danger")
                return redirect(url_for("productos"))
            
            if not isinstance(nombre, str):
                flash("El nombre del producto debe ser texto", "danger")
                return redirect(url_for("productos"))
            
            if nombre.strip() == "":
                flash("El nombre del producto no puede estar vacío", "danger")
                return redirect(url_for("productos"))
            
            if len(nombre) > 100:
                flash("El nombre del producto no puede exceder los 100 caracteres", "danger")
                return redirect(url_for("productos"))

            # ========================================
            # VALIDACIONES DE PRECIO
            # ========================================
            
            try:
                precio = float(precio_str) if precio_str else 0
            except (ValueError, TypeError):
                flash("El precio debe ser un número válido", "danger")
                return redirect(url_for("productos"))

            # ========================================
            # VALIDACIONES DE STOCK
            # ========================================
            
            try:
                stock = int(stock_str) if stock_str else 0
            except (ValueError, TypeError):
                flash("El stock debe ser un número entero válido", "danger")
                return redirect(url_for("productos"))

            # ========================================
            # VALIDACIONES DE DESCUENTO
            # ========================================
            
            try:
                descuento_valor = int(descuento_valor_str) if descuento_valor_str else 0
            except (ValueError, TypeError):
                descuento_valor = 0

            producto = Producto(
                id=id_prod,
                nombre=nombre.strip(),
                precio=precio,
                stock=stock,
                aplica_promocion=None,
                tipo_descuento=tipo_descuento,
                descuento_valor=descuento_valor
            )

            producto.actualizar()

            flash(
                "Producto actualizado con éxito",
                "success"
            )

        except NombreProductoException as e:
            flash(str(e), "danger")
        except PrecioProductoException as e:
            flash(str(e), "danger")
        except StockProductoException as e:
            flash(str(e), "danger")
        except TipoDescuentoException as e:
            flash(str(e), "danger")
        except DescuentoValorException as e:
            flash(str(e), "danger")
        except DBException as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"Error inesperado: {str(e)}", "danger")

        return redirect(url_for("productos"))


    # ========================================
    # INCREMENTAR STOCK
    # ========================================

    @app.route("/incrementar_stock/<int:id>", methods=["GET", "POST"])
    def incrementar_stock(id):

        if not validar_admin():
            return redirect(url_for("login_home"))

        # Validar que id sea válido
        try:
            id = int(id)
        except (ValueError, TypeError):
            flash("Identificador de producto inválido", "danger")
            return redirect(url_for("productos"))

        producto = Producto.consultar_por_id(id)

        if not producto:
            flash("Producto no encontrado", "danger")
            return redirect(url_for("productos"))

        if request.method == "POST":
            cantidad_str = request.form.get("cantidad", "0")
            
            # Validación de tipo para cantidad
            try:
                cantidad = int(cantidad_str)
            except (ValueError, TypeError):
                flash("La cantidad debe ser un número entero válido", "danger")
                return render_template("incrementar_stock.html", producto=producto)
            
            if cantidad <= 0:
                flash("La cantidad debe ser mayor que cero", "danger")
                return render_template("incrementar_stock.html", producto=producto)
            
            if cantidad > 10000:
                flash("La cantidad no puede exceder las 10,000 unidades por operación", "danger")
                return render_template("incrementar_stock.html", producto=producto)

            try:
                with pgdb.get_cursor() as cur:
                    cur.execute(
                        "UPDATE productos SET stock = stock + %s WHERE id = %s",
                        (cantidad, id)
                    )
                nuevo_stock = producto.stock + cantidad
                flash(f"Stock incrementado en {cantidad} unidades. Nuevo stock: {nuevo_stock}", "success")
                return redirect(url_for("productos"))

            except Exception as e:
                flash(f"Error al incrementar stock: {str(e)}", "danger")

        return render_template("incrementar_stock.html", producto=producto)

    # ========================================
    # REPORTE DE STOCK (SOLO ADMIN)
    # ========================================

    @app.route("/reporte_stock")
    def reporte_stock():

        if not validar_admin():
            return redirect(url_for("login_home"))

        productos = Producto.consultar_reporte_stock()

        return render_template(
            "reporte_stock.html",
            productos=productos
        )


    # ========================================
    # VENTAS (PANTALLA DE VENTA)
    # ========================================

    @app.route("/ventas")
    def ventas():
        print(f"DEBUG - Session en ventas: {dict(session)}")
        
        if not validar_sesion():
            print("DEBUG - Sesión inválida, redirigiendo a login")
            return redirect(url_for("login_home"))

        productos = Producto.consultar_todo()

        return render_template(
            "ventas.html",
            productos=productos
        )


    # ========================================
    # AGREGAR AL CARRITO
    # ========================================

    @app.route("/agregar_carrito", methods=["POST"])
    def agregar_carrito():

        if not validar_sesion():
            return redirect(url_for("login_home"))

        producto_id_str = request.form.get("producto_id")
        cantidad_str = request.form.get("cantidad")

        # Validaciones de tipo
        try:
            producto_id = int(producto_id_str) if producto_id_str else 0
        except (ValueError, TypeError):
            flash("Identificador de producto inválido", "danger")
            return redirect(url_for("ventas"))

        try:
            cantidad = int(cantidad_str) if cantidad_str else 0
        except (ValueError, TypeError):
            flash("La cantidad debe ser un número entero válido", "danger")
            return redirect(url_for("ventas"))

        if cantidad <= 0:
            flash("La cantidad debe ser mayor que cero", "danger")
            return redirect(url_for("ventas"))

        producto = Producto.consultar_por_id(producto_id)

        if not producto:
            flash("Producto no encontrado", "danger")
            return redirect(url_for("ventas"))

        if 'carrito' not in session:
            session['carrito'] = []

        # Verificar si el producto ya está en el carrito
        item_existente = None
        for item in session['carrito']:
            if item['id'] == producto_id:
                item_existente = item
                break

        # Calcular la nueva cantidad total
        cantidad_actual = item_existente['cantidad'] if item_existente else 0
        nueva_cantidad = cantidad_actual + cantidad

        # Validar stock
        if producto.stock < nueva_cantidad:
            stock_restante = producto.stock - cantidad_actual
            if stock_restante <= 0:
                flash(f"No hay stock disponible de '{producto.nombre}'. Ya tienes {cantidad_actual} unidades en tu carrito, que es todo el stock disponible.", "warning")
            else:
                flash(f"Solo puedes agregar {stock_restante} unidades más de '{producto.nombre}'. Ya tienes {cantidad_actual} en tu carrito.", "warning")
            return redirect(url_for("ventas"))

        # Calcular el total aplicando la promoción sobre la cantidad TOTAL
        total = CalculadorDescuento.calcular_total(
            producto.tipo_descuento,
            producto.descuento_valor,
            nueva_cantidad,
            producto.precio
        )

        # Actualizar o agregar el item en el carrito
        if item_existente:
            # Actualizar item existente
            item_existente['cantidad'] = nueva_cantidad
            item_existente['subtotal'] = total
        else:
            # Agregar nuevo item
            session['carrito'].append({
                'id': producto.id,
                'nombre': producto.nombre,
                'cantidad': nueva_cantidad,
                'precio': producto.precio,
                'tipo_descuento': producto.tipo_descuento,
                'descuento_valor': producto.descuento_valor,
                'subtotal': total
            })

        session.modified = True

        # Mensaje de confirmación
        descripcion = CalculadorDescuento.obtener_descripcion(producto.tipo_descuento, producto.descuento_valor)
        
        # Calcular ahorro para mostrar mensaje más informativo
        subtotal_sin_descuento = nueva_cantidad * producto.precio
        ahorro = subtotal_sin_descuento - total
        
        if descripcion != 'Sin descuento':
            if ahorro > 0:
                flash(f"Agregado {cantidad} x {producto.nombre}. Total en carrito: {nueva_cantidad} unidades. Promoción aplicada: {descripcion}. Ahorro: ${ahorro:.2f}", "success")
            else:
                flash(f"Agregado {cantidad} x {producto.nombre}. Total en carrito: {nueva_cantidad} unidades. Promoción aplicada: {descripcion}", "success")
        else:
            flash(f"Agregado {cantidad} x {producto.nombre}. Total en carrito: {nueva_cantidad} unidades", "success")

        return redirect(url_for("ventas"))


    # ========================================
    # VER CARRITO
    # ========================================

    @app.route("/carrito")
    def ver_carrito():
        print(f"DEBUG - Session en carrito: {dict(session)}")
        
        if not validar_sesion():
            print("DEBUG - Sesión inválida, redirigiendo a login")
            return redirect(url_for("login_home"))

        carrito = session.get('carrito', [])
        
        # Recalcular subtotales por si hubo cambios
        for item in carrito:
            producto = Producto.consultar_por_id(item['id'])
            if producto:
                nuevo_total = CalculadorDescuento.calcular_total(
                    producto.tipo_descuento,
                    producto.descuento_valor,
                    item['cantidad'],
                    producto.precio
                )
                item['subtotal'] = nuevo_total
        
        total = sum(item['subtotal'] for item in carrito)
        session.modified = True

        return render_template(
            "carrito.html",
            carrito=carrito,
            total=total
        )


    # ========================================
    # PROCESAR COMPRA
    # ========================================

    @app.route("/procesar_compra", methods=["POST"])
    def procesar_compra():

        if not validar_sesion():
            return redirect(url_for("login_home"))

        carrito = session.get('carrito', [])

        if not carrito:
            flash("El carrito está vacío", "warning")
            return redirect(url_for("ventas"))

        # Validar stock disponible para todos los items del carrito
        for item in carrito:
            if 'id' not in item or 'cantidad' not in item or 'nombre' not in item:
                flash("Error en la estructura del carrito", "danger")
                return redirect(url_for("ventas"))

            try:
                producto_id = int(item['id'])
                cantidad_solicitada = int(item['cantidad'])
            except (ValueError, TypeError):
                flash(f"Error en los datos del producto '{item.get('nombre', 'desconocido')}'", "danger")
                return redirect(url_for("ventas"))

            # Validar rango de cantidad
            if cantidad_solicitada <= 0:
                flash(f"Cantidad inválida para el producto '{item.get('nombre', 'desconocido')}'", "danger")
                return redirect(url_for("ventas"))
            
            if cantidad_solicitada > 999999:
                flash(f"La cantidad para '{item.get('nombre', 'desconocido')}' es demasiado grande", "danger")
                return redirect(url_for("ventas"))

            producto = Producto.consultar_por_id(producto_id)
            if not producto:
                flash(f"Producto '{item['nombre']}' no encontrado", "danger")
                return redirect(url_for("ventas"))

            if producto.stock < cantidad_solicitada:
                flash(f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, Solicitado: {cantidad_solicitada}", "danger")
                return redirect(url_for("ventas"))

        try:
            empleado_id = None
            if session.get('empleado_id'):
                empleado_id = session.get('empleado_id')
            elif session.get('rol') == 'vendedor':
                empleado_id = session.get('user_id')

            ventas_registradas = []

            for item in carrito:
                venta = Venta(
                    producto_id=item['id'],
                    cantidad=item['cantidad'],
                    total=item['subtotal']
                )
                venta_id = venta.registrar()
                ventas_registradas.append(venta_id)

                if empleado_id:
                    with pgdb.get_cursor() as cur:
                        cur.execute(
                            "UPDATE ventas SET empleado_id = %s WHERE id = %s",
                            (empleado_id, venta.id)
                        )

            session.pop('carrito', None)

            flash("Venta completada con éxito", "success")

            if ventas_registradas:
                return redirect(url_for("ticket", venta_id=ventas_registradas[-1]))

        except VentaException as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"Error inesperado: {str(e)}", "danger")

        return redirect(url_for("ventas"))


    # ========================================
    # TICKET DE VENTA
    # ========================================

    @app.route("/ticket/<int:venta_id>")
    def ticket(venta_id):

        if not validar_sesion():
            return redirect(url_for("login_home"))

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT 
                    ventas.id,
                    ventas.cantidad,
                    ventas.total,
                    ventas.fecha,
                    productos.nombre as producto_nombre,
                    productos.precio,
                    empleados.nombre || ' ' || empleados.apellido_paterno as vendedor_nombre
                FROM ventas
                JOIN productos ON ventas.producto_id = productos.id
                LEFT JOIN empleados ON ventas.empleado_id = empleados.id
                WHERE ventas.id = %s
                """,
                (venta_id,)
            )

            venta = cur.fetchone()

            if not venta:
                flash("Venta no encontrada", "danger")
                return redirect(url_for("ventas"))

            # Los índices de la tupla venta son:
            # 0: id, 1: cantidad, 2: total, 3: fecha, 4: producto_nombre, 5: precio, 6: vendedor_nombre
            venta_id = venta[0]
            cantidad = venta[1]
            total = venta[2]
            fecha = venta[3]
            producto_nombre = venta[4]
            precio = venta[5]
            vendedor_nombre = venta[6] if venta[6] else 'Administrador'

            # Obtener todos los items de la venta (si hay múltiples productos en la misma venta)
            cur.execute(
                """
                SELECT 
                    productos.nombre,
                    ventas.cantidad,
                    ventas.total
                FROM ventas
                JOIN productos ON ventas.producto_id = productos.id
                WHERE ventas.id = %s
                """,
                (venta_id,)
            )

            items = cur.fetchall()

        return render_template(
            "ticket.html",
            venta_id=venta_id,
            items=items,
            fecha=fecha,
            total=total,
            vendedor=vendedor_nombre
        )


    # ========================================
    # LIMPIAR CARRITO
    # ========================================

    @app.route("/limpiar_carrito")
    def limpiar_carrito():

        if not validar_sesion():
            return redirect(url_for("login_home"))

        session.pop('carrito', None)

        flash(
            "Carrito vaciado",
            "info"
        )

        return redirect(url_for("ventas"))


    # ========================================
    # HISTORIAL DE VENTAS (SOLO ADMIN)
    # ========================================

    @app.route("/historial")
    def historial():

        if not validar_admin():
            return redirect(url_for("login_home"))

        with pgdb.get_cursor() as cur:

            cur.execute(
                """
                SELECT
                    ventas.id,
                    productos.nombre,
                    ventas.cantidad,
                    ventas.total,
                    ventas.fecha,
                    COALESCE(empleados.nombre || ' ' || empleados.apellido_paterno, 'Administrador') as vendedor
                FROM ventas
                JOIN productos ON ventas.producto_id = productos.id
                LEFT JOIN empleados ON ventas.empleado_id = empleados.id
                ORDER BY ventas.id DESC
                """
            )

            resultados = []

            for row in cur.fetchall():

                venta = {
                    'id': row[0],
                    'nombre_producto': row[1],
                    'cantidad': row[2],
                    'total': float(row[3]) if row[3] else 0,
                    'fecha': row[4],
                    'vendedor': row[5]
                }

                resultados.append(venta)

            total_general = sum(v['total'] for v in resultados)

        return render_template(
            "historial.html",
            ventas=resultados,
            total=total_general
        )


    # ========================================
    # GESTION DE EMPLEADOS (SOLO ADMIN)
    # ========================================

    @app.route("/empleados")
    def empleados():

        if not validar_admin():
            return redirect(url_for("login_home"))

        lista_empleados = Empleado.consultar_todos(solo_activos=False)

        return render_template(
            "empleados.html",
            empleados=lista_empleados
        )


    # ========================================
    # AGREGAR EMPLEADO
    # ========================================

    @app.route("/agregar_empleado", methods=["GET", "POST"])
    def agregar_empleado():

        if not validar_admin():
            return redirect(url_for("login_home"))

        if request.method == "POST":

            try:
                # Validaciones básicas de campos requeridos
                if not request.form.get("nombre") or not request.form.get("nombre").strip():
                    flash("El nombre es requerido", "danger")
                    return render_template("empleado_form.html", empleado=None)

                if not request.form.get("apellido_paterno") or not request.form.get("apellido_paterno").strip():
                    flash("El apellido paterno es requerido", "danger")
                    return render_template("empleado_form.html", empleado=None)

                if not request.form.get("email") or not request.form.get("email").strip():
                    flash("El correo electrónico es requerido", "danger")
                    return render_template("empleado_form.html", empleado=None)

                if not request.form.get("username") or not request.form.get("username").strip():
                    flash("El nombre de usuario es requerido", "danger")
                    return render_template("empleado_form.html", empleado=None)

                nuevo_empleado = Empleado(
                    nombre=request.form.get("nombre").strip(),
                    apellido_paterno=request.form.get("apellido_paterno").strip(),
                    apellido_materno=request.form.get("apellido_materno").strip() if request.form.get("apellido_materno") else None,
                    email=request.form.get("email").strip(),
                    telefono=request.form.get("telefono").strip() if request.form.get("telefono") else None,
                    fecha_contratacion=request.form.get("fecha_contratacion") or None,
                    username=request.form.get("username").strip(),
                    password=request.form.get("password") if request.form.get("password") else "vendedor123",
                    rol=request.form.get("rol", "vendedor")
                )

                nuevo_empleado.insertar()

                flash(
                    f"Empleado '{nuevo_empleado.obtener_nombre_completo()}' agregado correctamente",
                    "success"
                )

                return redirect(url_for("empleados"))

            except NombreEmpleadoException as e:
                flash(str(e), "danger")
            except EmailEmpleadoException as e:
                flash(str(e), "danger")
            except UsernameEmpleadoException as e:
                flash(str(e), "danger")
            except PasswordEmpleadoException as e:
                flash(str(e), "danger")
            except AltaEmpleadoException as e:
                flash(str(e), "danger")

        return render_template("empleado_form.html", empleado=None)


    # ========================================
    # EDITAR EMPLEADO
    # ========================================

    @app.route("/editar_empleado/<int:id>", methods=["GET", "POST"])
    def editar_empleado(id):

        if not validar_admin():
            return redirect(url_for("login_home"))

        empleado = Empleado.consultar_por_id(id)

        if not empleado:
            flash("Empleado no encontrado", "danger")
            return redirect(url_for("empleados"))

        if request.method == "POST":

            try:
                # No incluir password en la actualización
                empleado.nombre = request.form.get("nombre").strip()
                empleado.apellido_paterno = request.form.get("apellido_paterno").strip()
                empleado.apellido_materno = request.form.get("apellido_materno").strip() if request.form.get("apellido_materno") else None
                empleado.email = request.form.get("email").strip()
                empleado.telefono = request.form.get("telefono").strip() if request.form.get("telefono") else None
                empleado.fecha_contratacion = request.form.get("fecha_contratacion") or None
                empleado.username = request.form.get("username").strip()
                empleado.rol = request.form.get("rol", "vendedor")
                # La contraseña NO se actualiza aquí

                empleado.actualizar()

                flash(
                    f"Empleado '{empleado.obtener_nombre_completo()}' actualizado correctamente",
                    "success"
                )

                return redirect(url_for("empleados"))

            except NombreEmpleadoException as e:
                flash(str(e), "danger")
            except EmailEmpleadoException as e:
                flash(str(e), "danger")
            except UsernameEmpleadoException as e:
                flash(str(e), "danger")
            except AltaEmpleadoException as e:
                flash(str(e), "danger")

        return render_template("empleado_form.html", empleado=empleado)


    # ========================================
    # CAMBIAR CONTRASEÑA DE EMPLEADO
    # ========================================

    @app.route("/cambiar_password_empleado/<int:id>", methods=["POST"])
    def cambiar_password_empleado(id):

        if not validar_admin():
            return redirect(url_for("login_home"))

        try:
            empleado_id = int(id)
        except (ValueError, TypeError):
            flash("Identificador de empleado inválido", "danger")
            return redirect(url_for("empleados"))

        from appweb.empleados import Empleado, PasswordEmpleadoException, AltaEmpleadoException

        empleado = Empleado.consultar_por_id(empleado_id)

        if not empleado:
            flash("Empleado no encontrado", "danger")
            return redirect(url_for("empleados"))

        nueva_password = request.form.get("nueva_password")

        if nueva_password is None:
            flash("La nueva contraseña es requerida", "danger")
            return redirect(url_for("empleados"))

        if not isinstance(nueva_password, str):
            flash("La contraseña debe ser texto", "danger")
            return redirect(url_for("empleados"))

        nueva_password = nueva_password.strip()

        if not nueva_password:
            flash("La nueva contraseña es requerida", "danger")
            return redirect(url_for("empleados"))

        if len(nueva_password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "danger")
            return redirect(url_for("empleados"))

        if len(nueva_password) > 30:
            flash("La contraseña no puede exceder los 30 caracteres", "danger")
            return redirect(url_for("empleados"))

        try:
            empleado.actualizar_password(nueva_password)
            flash(f"Contraseña actualizada correctamente para '{empleado.obtener_nombre_completo()}'", "success")
        except PasswordEmpleadoException as e:
            flash(str(e), "danger")
        except AltaEmpleadoException as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"Error inesperado: {str(e)}", "danger")

        return redirect(url_for("empleados"))


    # ========================================
    # ELIMINAR (DESACTIVAR) EMPLEADO
    # ========================================

    @app.route("/eliminar_empleado/<int:id>")
    def eliminar_empleado(id):

        if not validar_admin():
            return redirect(url_for("login_home"))

        try:
            empleado_id = int(id)
        except (ValueError, TypeError):
            flash("Identificador de empleado inválido", "danger")
            return redirect(url_for("empleados"))

        empleado = Empleado.consultar_por_id(empleado_id)

        if not empleado:
            flash("Empleado no encontrado", "danger")
            return redirect(url_for("empleados"))

        try:
            empleado.eliminar()
            flash(
                f"Empleado '{empleado.obtener_nombre_completo()}' ha sido desactivado",
                "warning"
            )
        except AltaEmpleadoException as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"Error inesperado: {str(e)}", "danger")

        return redirect(url_for("empleados"))


    # ========================================
    # ACTIVAR EMPLEADO
    # ========================================

    @app.route("/activar_empleado/<int:id>")
    def activar_empleado(id):

        if not validar_admin():
            return redirect(url_for("login_home"))

        try:
            empleado_id = int(id)
        except (ValueError, TypeError):
            flash("Identificador de empleado inválido", "danger")
            return redirect(url_for("empleados"))

        empleado = Empleado.consultar_por_id(empleado_id)

        if not empleado:
            flash("Empleado no encontrado", "danger")
            return redirect(url_for("empleados"))

        try:
            empleado.activar()
            flash(
                f"Empleado '{empleado.obtener_nombre_completo()}' ha sido activado",
                "success"
            )
        except AltaEmpleadoException as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"Error inesperado: {str(e)}", "danger")

        return redirect(url_for("empleados"))


    # ========================================
    # ERROR 404
    # ========================================
    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        # No mostrar flash si el usuario está autenticado como vendedor
        # y está navegando por páginas válidas (el error viene de intentos previos)
        
        # Verificar si la solicitud es para un archivo estático
        if request.path.startswith('/static/'):
            return "Archivo no encontrado", 404
        
        # Para vendedores, no mostrar el mensaje de error (es molesto)
        if session.get('rol') == 'vendedor':
            # Redirigir sin flash
            return redirect(url_for("inicio_home"))
        
        # Para otros usuarios, mostrar el mensaje
        flash("La página solicitada no existe", "danger")
        return redirect(url_for("login_home"))