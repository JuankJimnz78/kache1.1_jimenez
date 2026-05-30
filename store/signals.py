from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.apps import apps


@receiver(pre_save, sender='store.Precio')
def capturar_precio_anterior(sender, instance, **kwargs):
    if instance.pk:
        try:
            viejo = sender.objects.get(pk=instance.pk)
            instance._precio_anterior = viejo.precio_actual
        except sender.DoesNotExist:
            instance._precio_anterior = None
    else:
        instance._precio_anterior = None


@receiver(post_save, sender='store.Precio')
def registrar_historial_precio(sender, instance, created, **kwargs):
    HistorialPrecio = apps.get_model('store', 'HistorialPrecio')
    if created:
        HistorialPrecio.objects.create(
            id_producto=instance.id_producto,
            id_sucursal=instance.id_sucursal,
            precio_registrado=instance.precio_actual,
        )
    else:
        precio_anterior = getattr(instance, '_precio_anterior', None)
        if precio_anterior is not None and precio_anterior != instance.precio_actual:
            HistorialPrecio.objects.create(
                id_producto=instance.id_producto,
                id_sucursal=instance.id_sucursal,
                precio_registrado=precio_anterior,
            )
