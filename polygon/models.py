from django.db import models


class Polygon(models.Model):
    name = models.CharField(unique=True, max_length=128)
    description = models.TextField()

    class Meta:
        db_table = 'polygon'

class PolyPoint(models.Model):
    poly = models.ForeignKey('Polygon', related_name='points', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'polygon_point'