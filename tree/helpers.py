from django.db.models import Func, F, Max, Min
import os

IMAGE_SAVE_FORMAT = "%(pk)s_%(name)s"

DISTANCE_UNIT = 6371.0


class Sin(Func):
    function = 'SIN'


class Cos(Func):
    function = 'COS'


class Acos(Func):
    function = 'ACOS'


class Radians(Func):
    function = 'RADIANS'


def get_range(model, latitude, longitude, outer_border, inner_border=0):
    """Return range query.

    :params:
        -`model`: Model class.
        -`latitude`: center latitude.
        -`longitude`: center longitude.
        -`outer_border`: maximum filtered range.
        -`inner_border`: minimum filtered range.

    :return:
        Query object, ready to fetch data from.
    """

    query_expression = DISTANCE_UNIT * Acos(
        Cos(Radians(latitude)) * Cos(Radians(F('latitude'))) *
        Cos(Radians(F('longitude')) - Radians(longitude)) +
        Sin(Radians(latitude)) * Sin(Radians(F('latitude'))))

    query = model.objects.annotate(distance=query_expression)
    query = query.filter(distance__range=(inner_border, outer_border))
    query = query.filter(distance__lt=outer_border)
    query = query.order_by('distance')

    return query


def save_image(img_obj, tree_obj):
    url = os.path.join("img", IMAGE_SAVE_FORMAT % {'pk': tree_obj.pk, 'name': img_obj.name})
    if img_obj.content_type.startswith('image/'):
        with open(url, 'wb') as out_file:
            out_file.write(img_obj.read())
        return url
    else:
        raise ValueError("Only image accepted.")


def obtain_polygon_borders(polygon):
    """Return polygon bounds."""
    return polygon.points.aggregate(
        lat_min=Min('latitude'),
        lat_max=Max('latitude'),
        lng_min=Min('longitude'),
        lng_max=Max('longitude'),)
