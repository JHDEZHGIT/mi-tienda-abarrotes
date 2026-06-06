# src/appweb/descuentos.py

class CalculadorDescuento:
    """Clase para calcular descuentos según el tipo de promoción"""

    # Tipos de descuento válidos
    TIPOS_VALIDOS = ['ninguno', 'porcentaje', '2x1', '3x2', '4x3', '5x4']
    
    # Porcentajes válidos (múltiplos de 5 entre 5 y 90)
    PORCENTAJES_VALIDOS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]

    @staticmethod
    def _validar_parametros(tipo, valor, cantidad, precio_unitario):
        """
        Valida los parámetros de entrada para el cálculo de descuentos

        Parámetros:
            tipo: tipo de descuento
            valor: valor del descuento
            cantidad: cantidad de unidades
            precio_unitario: precio por unidad

        Lanza:
            ValueError: si algún parámetro es inválido

        Retorna:
            tuple: (cantidad_validada, precio_validada, valor_validada)
        """

        # Validar tipo
        if tipo is None:
            raise ValueError("Error: el tipo de descuento no puede ser nulo")

        if not isinstance(tipo, str):
            raise ValueError("Error: el tipo de descuento debe ser texto")

        if tipo not in CalculadorDescuento.TIPOS_VALIDOS:
            raise ValueError(
                f"Error: tipo de descuento '{tipo}' inválido. "
                f"Opciones válidas: {', '.join(CalculadorDescuento.TIPOS_VALIDOS)}"
            )

        # Validar valor (porcentaje)
        if valor is None:
            raise ValueError("Error: el valor del descuento no puede ser nulo")

        try:
            valor_numerico = float(valor)
        except (ValueError, TypeError):
            raise ValueError(f"Error: el valor '{valor}' no es un número válido")

        if tipo == 'porcentaje':
            if valor_numerico < 5:
                raise ValueError("Error: el porcentaje de descuento no puede ser menor a 5%")
            if valor_numerico > 90:
                raise ValueError("Error: el porcentaje de descuento no puede exceder el 90%")
            # Validar que sea múltiplo de 5
            if valor_numerico % 5 != 0:
                raise ValueError(f"Error: el porcentaje de descuento debe ser múltiplo de 5. Valor ingresado: {valor_numerico}%")
        else:
            if valor_numerico != 0:
                raise ValueError("Error: para promociones fijas el valor debe ser 0")

        # Validar cantidad
        if cantidad is None:
            raise ValueError("Error: la cantidad no puede ser nula")

        try:
            cantidad_numerica = int(cantidad)
        except (ValueError, TypeError):
            raise ValueError(f"Error: la cantidad '{cantidad}' no es un número entero válido")

        if cantidad_numerica < 0:
            raise ValueError("Error: la cantidad no puede ser negativa")

        # Validar precio unitario
        if precio_unitario is None:
            raise ValueError("Error: el precio unitario no puede ser nulo")

        try:
            precio_numerico = float(precio_unitario)
        except (ValueError, TypeError):
            raise ValueError(f"Error: el precio '{precio_unitario}' no es un número válido")

        if precio_numerico < 0:
            raise ValueError("Error: el precio unitario no puede ser negativo")

        return cantidad_numerica, precio_numerico, valor_numerico

    @staticmethod
    def calcular_total(tipo, valor, cantidad, precio_unitario):
        """
        Calcula el total a pagar aplicando el descuento correspondiente

        Parámetros:
            tipo: tipo de descuento (ninguno, porcentaje, 2x1, 3x2, 4x3, 5x4)
            valor: valor del descuento (porcentaje o 0 para promociones)
            cantidad: cantidad de unidades
            precio_unitario: precio por unidad

        Retorna:
            float: total a pagar

        Lanza:
            ValueError: si los parámetros son inválidos
        """

        # Validar parámetros
        cantidad_val, precio_val, valor_val = CalculadorDescuento._validar_parametros(
            tipo, valor, cantidad, precio_unitario
        )

        # Calcular según el tipo de descuento
        if tipo == 'ninguno':
            return round(cantidad_val * precio_val, 2)

        elif tipo == 'porcentaje':
            subtotal = cantidad_val * precio_val
            descuento = subtotal * (valor_val / 100)
            return round(subtotal - descuento, 2)

        elif tipo == '2x1':
            pares = cantidad_val // 2
            unidades = cantidad_val % 2
            return round((pares * precio_val) + (unidades * precio_val), 2)

        elif tipo == '3x2':
            grupos = cantidad_val // 3
            unidades = cantidad_val % 3
            return round((grupos * 2 * precio_val) + (unidades * precio_val), 2)

        elif tipo == '4x3':
            grupos = cantidad_val // 4
            unidades = cantidad_val % 4
            return round((grupos * 3 * precio_val) + (unidades * precio_val), 2)

        elif tipo == '5x4':
            grupos = cantidad_val // 5
            unidades = cantidad_val % 5
            return round((grupos * 4 * precio_val) + (unidades * precio_val), 2)

        # else:
        #     # Este caso no debería ocurrir por la validación previa
        #     return round(cantidad_val * precio_val, 2)

    @staticmethod
    def obtener_descripcion(tipo, valor):
        """
        Obtiene la descripción legible del descuento

        Parámetros:
            tipo: tipo de descuento
            valor: valor del descuento (porcentaje)

        Retorna:
            str: descripción del descuento
        """

        # Validar tipo
        if tipo is None:
            return 'Sin descuento'

        if not isinstance(tipo, str):
            return 'Sin descuento'

        # Validar valor para porcentaje
        valor_numerico = 0
        if tipo == 'porcentaje':
            try:
                valor_numerico = float(valor) if valor is not None else 0
            except (ValueError, TypeError):
                valor_numerico = 0

        # Retornar descripción según el tipo
        if tipo == 'ninguno':
            return 'Sin descuento'
        elif tipo == 'porcentaje':
            if valor_numerico > 0:
                return f'{int(valor_numerico)}% de descuento'
            else:
                return 'Sin descuento'
        elif tipo == '2x1':
            return 'Lleva 2 paga 1'
        elif tipo == '3x2':
            return 'Lleva 3 paga 2'
        elif tipo == '4x3':
            return 'Lleva 4 paga 3'
        elif tipo == '5x4':
            return 'Lleva 5 paga 4'
        else:
            return 'Sin descuento'


# # ============================================
# # FUNCIONES DE AYUDA
# # ============================================

# def calcular_precio_con_descuento(precio_original, porcentaje):
#     """
#     Calcula el precio final aplicando un porcentaje de descuento

#     Parámetros:
#         precio_original: precio original del producto
#         porcentaje: porcentaje de descuento a aplicar

#     Retorna:
#         float: precio con descuento aplicado
#     """
#     try:
#         precio = float(precio_original)
#         desc = float(porcentaje)
#     except (ValueError, TypeError):
#         return precio_original

#     if desc <= 0:
#         return round(precio, 2)
#     if desc >= 100:
#         return 0.0

#     descuento = precio * (desc / 100)
#     return round(precio - descuento, 2)


# def calcular_descuento_2x1(cantidad, precio_unitario):
#     """
#     Calcula el total aplicando la promoción 2x1

#     Parámetros:
#         cantidad: cantidad de unidades
#         precio_unitario: precio por unidad

#     Retorna:
#         float: total a pagar con promoción 2x1
#     """
#     try:
#         cant = int(cantidad)
#         precio = float(precio_unitario)
#     except (ValueError, TypeError):
#         return 0.0

#     if cant <= 0:
#         return 0.0

#     pares = cant // 2
#     unidades = cant % 2
#     return round((pares * precio) + (unidades * precio), 2)


# def calcular_descuento_3x2(cantidad, precio_unitario):
#     """
#     Calcula el total aplicando la promoción 3x2

#     Parámetros:
#         cantidad: cantidad de unidades
#         precio_unitario: precio por unidad

#     Retorna:
#         float: total a pagar con promoción 3x2
#     """
#     try:
#         cant = int(cantidad)
#         precio = float(precio_unitario)
#     except (ValueError, TypeError):
#         return 0.0

#     if cant <= 0:
#         return 0.0

#     grupos = cant // 3
#     unidades = cant % 3
#     return round((grupos * 2 * precio) + (unidades * precio), 2)


# def calcular_descuento_4x3(cantidad, precio_unitario):
#     """
#     Calcula el total aplicando la promoción 4x3

#     Parámetros:
#         cantidad: cantidad de unidades
#         precio_unitario: precio por unidad

#     Retorna:
#         float: total a pagar con promoción 4x3
#     """
#     try:
#         cant = int(cantidad)
#         precio = float(precio_unitario)
#     except (ValueError, TypeError):
#         return 0.0

#     if cant <= 0:
#         return 0.0

#     grupos = cant // 4
#     unidades = cant % 4
#     return round((grupos * 3 * precio) + (unidades * precio), 2)


# def calcular_descuento_5x4(cantidad, precio_unitario):
#     """
#     Calcula el total aplicando la promoción 5x4

#     Parámetros:
#         cantidad: cantidad de unidades
#         precio_unitario: precio por unidad

#     Retorna:
#         float: total a pagar con promoción 5x4
#     """
#     try:
#         cant = int(cantidad)
#         precio = float(precio_unitario)
#     except (ValueError, TypeError):
#         return 0.0

#     if cant <= 0:
#         return 0.0

#     grupos = cant // 5
#     unidades = cant % 5
#     return round((grupos * 4 * precio) + (unidades * precio), 2)