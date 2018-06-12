from ast import literal_eval
from collections import Iterable
from functools import partial

from django.db.models import Count, F
from rest_framework import status
from shapely.geometry import Point as SPoint
from shapely.geometry import Polygon as SPolygon

from greenka.helpers import get_range, obtain_polygon_borders
from tree.models import Tree
from polygon.models import Polygon


class TreeFilterException(Exception):
    """Filter class to handle filter exceptions"""

    def __init__(self, message, status=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status = status
        super(TreeFilterException, self).__init__()


def chain_filter_approved(request, queryset):
    approved = request.GET.get('approved')
    if approved is None:
        return queryset
    if approved == 'true':
        approved = True
    elif approved == 'false':
        approved = False
    else:
        raise TreeFilterException('Failed to parse `approved`.'
                                  ' Only `true` or `false` are allowed.')
    return queryset.filter(approved=approved)


def chain_filter_radius(request, queryset):
    """Return queryset filtered by distance from point

    request params:
        -`center`: <float,float>
        -`radius`: <float>
    """
    print('2')
    center = request.GET.get('center')
    radius = request.GET.get('radius')
    if center and radius:
        try:
            lat, lng, radius = map(float, (*center.split(','), radius, ))
        except Exception:
            raise TreeFilterException('Could not parse distance (`center`, `radius`) arguments.')
    elif center or radius:
        raise TreeFilterException('Request should have both `center` and `radius` params.')
    else:
        return queryset
    return get_range(queryset, lat, lng, radius)


def chain_filter_type(request, queryset):
    """Filter by tree type."""
    tree_type = request.GET.get('type')
    if not tree_type:
        return queryset

    try:
        tree_type = literal_eval(tree_type)
        print(tree_type)
        if not isinstance(tree_type, Iterable) or isinstance(tree_type, str):
            raise ValueError()
    except ValueError:
        raise TreeFilterException('Failed to parse `type` argument.'
                                  'Use array/list [1, 2, 3] format.')
    return queryset.filter(tree_type__in=tree_type)


def chain_filter_sort(request, queryset):
    """Filter by tree sort."""
    tree_sort = request.GET.get('sort')
    if not tree_sort:
        return queryset

    try:
        tree_sort = literal_eval(tree_sort)
        if not isinstance(tree_sort, Iterable) or isinstance(tree_sort, str):
            raise ValueError()
        tree_sort = map(int, tree_sort)
    except ValueError:
        raise TreeFilterException('Failed to parse `sort` argument.'
                                  'Use array/list [1, 2, 3] format.')
    return queryset.filter(tree_sort__in=tree_sort)


def chain_filter_state(request, queryset):
    """Filter by tree state."""
    tree_state = request.GET.get('state')
    if not tree_state:
        return queryset

    try:
        tree_state = literal_eval(tree_state)
        if not isinstance(tree_state, Iterable):
            raise ValueError()
        tree_state = set(map(int, tree_state))
        if tree_state - set(Tree.STATE_IDS):
            raise TreeFilterException('Invalid states: %s' % (tree_state, ))

    except ValueError:
        raise TreeFilterException('Failed to parse `sort` argument.'
                                  'Use array/list [1, 2, 3] format.')
    return queryset.filter(tree_state__in=tree_state)



def chain_filter_confirms(request, queryset):
    """Filter by confirms amount.

    If single value `int` filtered by confirm amount greater than this value.
    If `int`,`int` provided - [min,max] will be used."""
    confirm_value = request.GET.get('confirms')
    if not confirm_value:
        return queryset

    try:
        if ',' in confirm_value:
            min_confirms, max_confirms = map(int, confirm_value.split(','))
        else:
            min_confirms, max_confirms = int(confirm_value), None
        queryset = (queryset.annotate(confirmed=Count('confirms'))
                            .filter(confirmed__gte=min_confirms))

        if max_confirms:
            queryset = queryset.filter(confirmed__lte=max_confirms)
    except ValueError:
        raise TreeFilterException('Failed to parse `confirms`.'
                                  ' Use `int` or `int`,`int` formats.')


def chain_filter_polygon(request, queryset):
    """Filter queryset by polygon borders.

    This filter is FINAL, must be used as last.
    """
    print('final')
    if not request.GET.get('polygon'):
        return queryset

    polygon = None
    try:
        polygon = Polygon.objects.get(pk=request.GET.get('polygon'))
    except Polygon.DoesNotExist:
        raise TreeFilterException('Polygon not found.', status.HTTP_404_NOT_FOUND)
    borders = obtain_polygon_borders(polygon)
    trees = queryset.filter(latitude__lte=borders['lat_max'],
                            latitude__gte=borders['lat_min'],
                            longitude__lte=borders['lng_max'],
                            longitude__gte=borders['lng_min'])
    # filter trees to match polygon.
    filter_poly = SPolygon([(p.latitude, p.longitude) for p in polygon.points.all()])
    def filter_func(tree):
        """Inner function to filter tree by geo coordinates."""
        return filter_poly.intersects(SPoint(tree.latitude, tree.longitude))
    return filter(filter_func, trees)


# tuple with filters
TREE_CHAIN_FILTERS = (
    chain_filter_approved,
    chain_filter_confirms,
    chain_filter_state,
    chain_filter_sort,
    chain_filter_type,
    chain_filter_radius,
    chain_filter_polygon,

)


def chain_filter_it(request, queryset, index=0):
    """Recurrent function to filter given queryset."""
    if index == len(TREE_CHAIN_FILTERS):
        return queryset
    return chain_filter_it(request,
                           TREE_CHAIN_FILTERS[index](request, queryset),
                           index+1)
