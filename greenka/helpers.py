import os
import os.path
from uuid import uuid4

from django.db.models import F, Func, Max, Min
from django.core.exceptions import ValidationError
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes

from greenka import settings


IMAGE_SAVE_FORMAT = "%(salt)s_%(pk)s_%(name)s"

DISTANCE_UNIT = 6371.0


class Sin(Func):
    function = 'SIN'


class Cos(Func):
    function = 'COS'


class Acos(Func):
    function = 'ACOS'


class Radians(Func):
    function = 'RADIANS'


def get_range(queryset, latitude, longitude, outer_border, inner_border=0):
    """Return range query.

    :params:
        -`queryset`: Queryset object.
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

    query = queryset.annotate(distance=query_expression)
    query = query.filter(distance__range=(inner_border, outer_border))
    query = query.filter(distance__lt=outer_border)
    query = query.order_by('distance')

    return query


def __base_save_image(path, img_obj):
    """Base procedure to save uploaded image on disk."""
    if img_obj.content_type.startswith('image/'):
        try:
            with open(path, 'wb') as out_file:
                out_file.write(img_obj.read())
        except FileNotFoundError:
            os.makedirs(os.path.dirname(path))
            __base_save_image(path, img_obj)
    else:
        raise ValueError("Only image accepted.")


def save_user_image(img_obj, user_obj):
    """Save image for user profile

    :Parameters:
        - `img_obj`: Object of image to save.
        - `user_obj`: Image owner.

    :Return:
        Image URL if success or None on fail.
    """
    if img_obj.size > settings.MAX_USER_IMAGE_SIZE:
        raise ValidationError('image size more than %s' % (settings.MAX_USER_IMAGE_SIZE, ))
    url = os.path.join(
        settings.USER_IMAGE_SAVE_PATH,
        IMAGE_SAVE_FORMAT % {'salt': uuid4(), 'pk': user_obj.pk, 'name': img_obj.name})
    __base_save_image(url, img_obj)
    return url


def save_tree_image(img_obj, tree_obj):
    if img_obj.size > settings.MAX_TREE_IMAGE_SIZE:
        raise ValidationError('image size more than %s' % (settings.MAX_TREE_IMAGE_SIZE, ))
    url = os.path.join(
        settings.TREE_IMAGE_SAVE_PATH,
        IMAGE_SAVE_FORMAT % {'salt': uuid4(), 'pk': tree_obj.pk, 'name': img_obj.name})
    __base_save_image(url, img_obj)
    return url


def save_problem_image(img_obj, problem_obj):
    if img_obj.size > settings.MAX_PROBLEM_IMAGE_SIZE:
        raise ValidationError('image size more than %s' % (settings.MAX_PROBLEM_IMAGE_SIZE, ))
    url = os.path.join(
        settings.PROBLEM_IMAGE_SAVE_PATH,
        IMAGE_SAVE_FORMAT % {'salt': uuid4(), 'pk': problem_obj.pk, 'name': img_obj.name})
    __base_save_image(url, img_obj)
    return url


def save_feedback_image(img_obj, feedback_obj):
    if img_obj.size > settings.MAX_FEEDBACK_IMAGE_SIZE:
        raise ValidationError('image size more than %s' % (settings.MAX_FEEDBACK_IMAGE_SIZE, ))
    url = os.path.join(
        settings.FEEDBACK_IMAGE_SAVE_PATH,
        IMAGE_SAVE_FORMAT % {'salt': uuid4(), 'pk': feedback_obj.pk, 'name': img_obj.name})
    __base_save_image(url, img_obj)
    return url


def obtain_polygon_borders(polygon):
    """Return polygon bounds."""
    return polygon.points.aggregate(
        lat_min=Min('latitude'),
        lat_max=Max('latitude'),
        lng_min=Min('longitude'),
        lng_max=Max('longitude'),)


def default_auth_classes(func):
    """Default authentication classes decorator"""
    return authentication_classes((TokenAuthentication, SessionAuthentication, ))(func)

