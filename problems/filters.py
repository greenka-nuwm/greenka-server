from ast import literal_eval
from collections import Iterable

from rest_framework import status
from warnings import warn

from greenka.helpers import get_range


class ProblemFilterException(Exception):
    """Filter error exception."""

    def __init__(self, message, status=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status = status
        super(ProblemFilterException, self).__init__(self)


def chain_filter_active(request, queryset):
    """Filter by `is_active` param in request"""
    is_active = request.GET.get('is_active')
    if is_active is None:
        return queryset
    if is_active == 'true':
        is_active = True
    elif is_active == 'false':
        is_active = False
    else:
        raise ProblemFilterException('Failed to parse `is_active`'
                                     'Only `true` of `false` are allowed.')
    return queryset.filter(is_active=is_active)


def chain_filter_radius(request, queryset):
    """Filter Problem points by distance."""
    center = request.GET.get('center')
    radius = request.GET.get('radius')
    if center and radius:
        try:
            lat, lng, radius = map(float, (*center.split(','), radius, ))
        except Exception:
            raise ProblemFilterException('Could not parse distance (`center`, `radius`) arguments.')
    elif center or radius:
        raise ProblemFilterException('Request should have both `catner` and `radius` arguments.')
    else:
        return queryset
    return get_range(queryset, lat, lng, radius)


def chain_filter_problem_type(request, queryset):
    problem_type = request.GET.get('type')
    if not problem_type
        return queryset

    try:
        problem_type = literal_eval(problem_type)
        if isinstance(problem_type, int):
            problem_type = [problem_type, ]
        if not isinstance(problem_type, Iterable):
            raise ValueError()
        problem_type = set(map(int, problem_type))
    except ValueError:
        raise ProblemFilterException('Failed to parse `type` argument.'
                                     'Use array/list [1, 2, 3] format.')
    return queryset.filter(problem_type__in=problem_type)


def chain_filter_problem_state(request, queryset):
    problem_state = request.GET.get('state')
    if not problem_state
        return queryset

    try:
        problem_state = literal_eval(problem_state)
        if isinstance(problem_state, int):
            problem_state = [problem_state, ]
        if not isinstance(problem_state, Iterable):
            raise ValueError()
        problem_state = set(map(int, problem_state))
    except ValueError:
        raise ProblemFilterException('Failed to parse `state` argument.'
                                     'Use array/list [1, 2, 3] format.')
    return queryset.filter(problem_state_in=problem_state)


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


def chain_filter_creation_time(request, queryset):
    warn('TODO %s filtering' % (chain_filter_creation_time.__name__),
         RuntimeWarning)
    return queryset


def chain_filter_modification_time(request, queryset):
    warn('TODO %s filtering' % (chain_filter_modification_time.__name__),
         RuntimeWarning)
    return queryset


def chain_filter_polygon(request, queryset):
    warn('TODO %s filtering' % (chain_filter_polygon.__name__),
         RuntimeWarning)
    return queryset


FILTER_CHAIN = (

    chain_filter_active,
    chain_filter_approved,

    chain_filter_problem_state,
    chain_filter_problem_type,

    chain_filter_creation_time,
    chain_filter_modification_time,

    chain_filter_confirms,

    chain_filter_radius,
    chain_filter_polygon,
)


def chain_filter_it(request, queryset, index=0):
    """Run through chain of filters and filter queryset with them."""
    for chain_filter in FILTER_CHAIN:
        queryset = chain_filter(request, queryset)
    return queryset