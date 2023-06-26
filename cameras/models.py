from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models


class Camera(models.Model):
    class Meta:
        verbose_name = _('Камера')
        verbose_name_plural = _('Камери')

    class Zone(TextChoices):
        BLUE = 'blue'
        GREEN = 'green'

    uid = models.UUIDField(primary_key=True, unique=True)
    name = models.CharField(blank=True, null=True, verbose_name=_('име'))
    address = models.CharField(blank=True, null=True, verbose_name=('адрес'))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('ширина'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('дължина'))
    url = models.URLField(blank=False, null=False, verbose_name=_('линк'))
    parking_mask = models.MultiPolygonField(blank=True, null=True)
    violator_mask = models.MultiPolygonField(blank=True, null=True)
    max_cap = models.PositiveIntegerField(default=0)
    current_cap = models.IntegerField(default=0)
    zone = models.CharField(choices=Zone.choices, max_length=244)
