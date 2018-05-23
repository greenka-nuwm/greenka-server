from django.db.models import Func, F


class Sin(Func):
    function = 'SIN'


class Cos(Func):
    function = 'COS'


class Acos(Func):
    function = 'ACOS'


class Radians(Func):
    function = 'RADIANS'


DISTANCE_UNIT = 6371.0


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

    print("expr: ", query_expression)

    query = model.objects.annotate(distance=query_expression)
    print(dir(query[:][0]))
    print(query[:][0].distance)
    # query = query.filter(distance__range=(inner_border, outer_border))
    query = query.filter(distance__lt=outer_border)
    print(query[:])
    query = query.order_by('distance')
    print(query.query)
    print(query[:])

    return query