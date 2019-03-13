from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from django.shortcuts import get_object_or_404

from greenka.helpers import default_auth_classes
from tree.serializers import TreeSerializer, TreeGETSerializer, TreeGETShortSerializer
from tree.models import Tree
from tree.filters import chain_filter_it, TreeFilterException
from tree.permissions import IsAdminTreeOwnerOrReadOnly


class TreeView(generics.ListCreateAPIView):
    """# Main function to fetch trees.

    get:

    __To filter by distance__, use both params `radius:float`
    and `center:float,float`.

    __To filter by approved state__, just use `approved:bool`!

    __To filter by polygon__, you can use
    `polygon:int` with ID of polygon.

    __To filter by type__, use `type:array(int)` to fetch all trees
    with type ID in given array.

    __To filter by sort__, use `type:array(int)` to fetch all trees
    with sort ID in given array.

    __To filter by confirm amount__, use `confirms` with two formats:
    single `int` to set minimum amount of confirms,
    and `int`,`int` to specify min and max.

    __To filter by state__, use `state:array(int)`.


    post:
    Create new tree on map.
    """
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, )

    def post(self, request, *args, **kwargs):
        if not IsAuthenticated().has_permission(request, self):
            raise NotAuthenticated()
        return super(TreeView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not IsAdminUser().has_permission(request, self):
                queryset = queryset.filter(is_active=True)
            result = chain_filter_it(request, queryset)
        except TreeFilterException as error:
            return Response({'message': error.message},
                            status=error.status)
        serializer = TreeGETShortSerializer(result, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TreeDetailsReadOnlyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tree.objects.filter(is_active=True)
    permission_classes = (IsAdminTreeOwnerOrReadOnly, )
    authentication_classes = (TokenAuthentication, SessionAuthentication, )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TreeGETSerializer
        return TreeSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        return super(TreeDetailsReadOnlyView, self).retrieve(request, pk, *args, **kwargs)


@api_view(['POST'])
@default_auth_classes
@permission_classes((IsAuthenticated, ))
def confirm_tree(request, pk):
    try:
        tree = Tree.objects.get(pk=pk)
    except Exception:
        return Response({'error': 'Wrong tree ID.'},
                        status=status.HTTP_400_BAD_REQUEST)

    added = False
    if tree.confirms.filter(pk=request.user.pk).exists():
        tree.confirms.remove(request.user)
    else:
        added = True
        tree.confirms.add(request.user)
    return Response({'added': added, 'removed': not added,
                     'confirms': tree.confirms.all().count()},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@default_auth_classes
@permission_classes((IsAdminUser, ))
def set_approve_tree(request, pk):
    """Set approved state of target tree. Use `approved` JSON param."""
    tree = get_object_or_404(Tree, pk=pk)
    tree.approved = request.data.get('approved', False)
    tree.save()
    return Response({'approved': tree.approved})


@api_view(['GET'])
@default_auth_classes
def get_tree_states(request):
    """Return all possible states of tree."""
    result = [{'id': pk, 'name': name}
              for pk, name in zip(Tree.STATE_IDS, Tree.STATE_STRS)]
    return Response(result)


@api_view(['POST'])
@default_auth_classes
@permission_classes((IsAuthenticated, ))
def add_fav_tree(request, pk):
    import pdb; pdb.set_trace()
    try:
        fav_trees = request.user.favourite_trees.all()
        tree = Tree.objects.all().filter(favourite_treespk=pk)
    except Exception:
        return Response({'error': 'Wrong tree ID.'},
                        status=status.HTTP_400_BAD_REQUEST)

    added = False
    if tree.confirms.filter(pk=request.user.pk).exists():
        tree.confirms.remove(request.user)
    else:
        added = True
        tree.confirms.add(request.user)
    return Response({'added': added, 'removed': not added,
                     'confirms': tree.confirms.all().count()},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
@default_auth_classes
def get_fav_trees(request):
    """Return all possible states of tree."""

    fav_trees = request.user.favourite_trees.all()
    return Response(result)
