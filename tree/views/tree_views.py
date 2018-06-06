from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from tree.serializers import TreeSerializer
from tree.models import Tree
from tree.filters import chain_filter_it, TreeFilterException


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
def get_trees(request):
    """# Main function to fetch trees.

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
    """
    try:
        result = chain_filter_it(request, Tree.objects.all())
    except TreeFilterException as error:
        return Response({'message': error.message},
                        status=error.status)
    serializer = TreeSerializer(result, many=True)
    return Response(serializer.data)


class TreeAddView(generics.CreateAPIView):
    """Create new tree on map."""
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TreeDetailsReadOnlyView(generics.RetrieveAPIView):
    queryset = Tree.objects.filter(active__exact=True)
    serializer_class = TreeSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        return super(TreeDetailsReadOnlyView, self).retrieve(request, pk, *args, **kwargs)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
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
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAdminUser, ))
def set_approve_tree(request, pk):
    """Set approved state of target tree. Use `approved` JSON param."""
    tree = get_object_or_404(Tree, pk=pk)
    tree.approved = request.data.get('approved', False)
    tree.save()
    return Response({'approved': tree.approved})


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
def get_tree_states(request):
    """Return all possible states of tree."""
    result = [{'id': pk, 'name': name}
              for pk, name in zip(Tree.STATE_IDS, Tree.STATE_STRS)]
    return Response(result)