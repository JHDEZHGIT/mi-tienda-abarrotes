# 🛒 Mi Tienda de Abarrotes - Sistema de Punto de Venta

Sistema de punto de venta (POS) para una tienda de abarrotes con gestión de productos, empleados, ventas y descuentos promocionales.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Pruebas](#pruebas)
- [Base de Datos](#base-de-datos)
- [Contribución](#contribución)

## ✨ Características

### Gestión de Productos
- ✅ CRUD completo de productos
- ✅ Control de stock (incremento manual)
- ✅ Reporte de stock bajo
- ✅ Sistema de descuentos por producto

### Tipos de Descuento Disponibles
| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| Porcentaje | 5% a 90% (múltiplos de 5) | 10% de descuento |
| 2x1 | Lleva 2 paga 1 | 2 unidades = paga 1 |
| 3x2 | Lleva 3 paga 2 | 3 unidades = paga 2 |
| 4x3 | Lleva 4 paga 3 | 4 unidades = paga 3 |
| 5x4 | Lleva 5 paga 4 | 5 unidades = paga 4 |

### Gestión de Empleados
- ✅ CRUD de empleados (vendedores y administradores)
- ✅ Autenticación y roles (admin / vendedor)
- ✅ Cambio de contraseña
- ✅ Activación/desactivación de cuentas

### Ventas
- ✅ Carrito de compras
- ✅ Aplicación automática de descuentos
- ✅ Generación de tickets
- ✅ Historial de ventas
- ✅ Reporte de ventas totales

## 🛠 Tecnologías

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.14+ | Lenguaje principal |
| Flask | 3.0+ | Framework web |
| PostgreSQL | 15+ | Base de datos |
| psycopg2 | 2.9+ | Adaptador PostgreSQL |
| pytest | 9.0+ | Framework de pruebas |
| pytest-cov | 7.1+ | Cobertura de pruebas |
| Bootstrap | 3.4+ | Estilos CSS |
| Werkzeug | 3.0+ | Seguridad (hashing de contraseñas) |

## 📁 Estructura del Proyecto
