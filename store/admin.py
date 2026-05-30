from django.contrib import admin
from store.models import Supermercado, Categoria, Producto, Sucursal, Precio, HistorialPrecio


@admin.register(Supermercado)
class SupermercadoAdmin(admin.ModelAdmin):
    list_display = ['id_supermercado', 'nombre', 'activo', 'sitio_web']
    list_filter = ['activo']
    search_fields = ['nombre']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id_categoria', 'nombre', 'categoria_padre']
    list_filter = ['categoria_padre']
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id_producto', 'nombre', 'marca', 'unidad_medida', 'id_categoria']
    list_filter = ['unidad_medida', 'id_categoria']
    search_fields = ['nombre', 'marca', 'codigo_barras']


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['id_sucursal', 'nombre_sucursal', 'ciudad', 'id_supermercado', 'activo']
    list_filter = ['activo', 'ciudad', 'id_supermercado']
    search_fields = ['nombre_sucursal', 'ciudad', 'direccion']


@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ['id_precio', 'id_producto', 'id_sucursal', 'precio_actual', 'en_oferta', 'fecha_actualizacion']
    list_filter = ['en_oferta']
    search_fields = ['id_producto__nombre', 'id_sucursal__nombre_sucursal']


@admin.register(HistorialPrecio)
class HistorialPrecioAdmin(admin.ModelAdmin):
    list_display = ['id_historial', 'id_producto', 'id_sucursal', 'precio_registrado', 'fecha_registro']
    list_filter = ['fecha_registro']
    search_fields = ['id_producto__nombre', 'id_sucursal__nombre_sucursal']
    readonly_fields = ['fecha_registro']
