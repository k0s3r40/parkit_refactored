from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models


class Camera(models.Model):
    class Meta:
        verbose_name = _('Камера')
        verbose_name_plural = _('Камери')

    uid = models.UUIDField(primary_key=True, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('ширина'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('дължина'))
    rotation = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('ротация спрямо север'))
    url = models.URLField(blank=False, null=False, verbose_name=_('линк'))
    parking_mask = models.MultiPolygonField()
    violator_mask = models.MultiPolygonField()
    max_cap = models.PositiveIntegerField(default=0)
    current_cap = models.IntegerField(default=0)
