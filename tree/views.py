from shapely.geometry import Polygon as SPolygon, Point as SPoint
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions as exc
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db import IntegrityError

from tree.models import Tree, TreeImages, Polygon, PolyPoint
from tree import serializers as ser
from tree.helpers import get_range, save_image, obtain_polygon_borders
from tree import permissions as perm


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_trees(request):
    """Return all user created trees"""
    trees = Tree.objects.filter(owner__exact=request.user.id).all()
    serializer = ser.TreeSerializer(trees, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_user(request):
    """Return info about self"""
    serializer = ser.UserSerializer(request.user)
    return Response(serializer.data)


class TreeAddView(generics.CreateAPIView):
    queryset = Tree.objects.all()
    serializer_class = ser.TreeSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TreeListReadOnlyView(APIView):

    def get(self, request, lat, lng, distance, format=None):
        query = get_range(Tree, lat, lng, distance).all()
        serializer = ser.TreeSerializer(query, many=True)
        return Response(serializer.data)


class TreeDetailsReadOnlyView(generics.RetrieveAPIView):
    queryset = Tree.objects.filter(active__exact=True)
    serializer_class = ser.TreeSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        return super(TreeDetailsReadOnlyView, self).retrieve(request, pk, *args, **kwargs)


class PolygonListCreateView(generics.ListCreateAPIView):
    queryset = Polygon.objects.all()
    serializer_class = ser.PolygonSerializer
    permission_classes = (perm.IsAdminOrReadOnly, )


class PolygonDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Polygon.objects.all()
    serializer_class = ser.PolygonSerializer
    permission_classes = (IsAdminUser, )


class TreeImageCreateView(APIView):
    queryset = TreeImages.objects.all()
    serializer_class = ser.TreeImageSerializer
    permission_classes = (IsAuthenticated, perm.IsTreeImageTreeOwner, )
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, pk):
        # save image data on disk
        try:
            tree_obj = Tree.objects.get(pk=pk)
        except Exception:
            return Response({'error': 'Wrong tree ID.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not perm.IsTreeImageTreeOwner().has_object_permission(request, self, tree_obj):
            raise exc.PermissionDenied()

        url = save_image(request.data.get('img'), tree_obj)
        serializer = ser.TreeImageSerializer(data={})
        if serializer.is_valid():
            try:
                serializer.save(url=url, visible=True, tree=tree_obj)
            except IntegrityError:
                return Response({'error': 'This image already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def confirm_tree(request, pk):
    try:
        tree = Tree.objects.get(pk=pk)
    except Exception:
        return Response({'error': 'Wrong tree ID.'},
                        status=status.HTTP_400_BAD_REQUEST)

    if tree.confirms.filter(pk=request.user.pk).exists():
        tree.confirms.remove(request.user)
    else:
        tree.confirms.add(request.user)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def obtain_trees_in_polygon(request, poly_pk):
    try:
        poly = Polygon.objects.get(pk=poly_pk)
    except Exception:
        return Response({'error': 'Wrong polygon ID.'},
                        status=status.HTTP_400_BAD_REQUEST)
    borders = obtain_polygon_borders(poly)
    trees = Tree.objects.filter(latitude__lte=borders['lat_max'],
                                latitude__gte=borders['lat_min'],
                                longitude__lte=borders['lng_max'],
                                longitude__gte=borders['lng_min'])
    # filter trees to match polygon.
    filter_poly = SPolygon([(p.latitude, p.longitude) for p in poly.points.all()])
    def filter_func(tree):
        """Inner function to filter tree by geo coordinates."""
        return filter_poly.intersects(SPoint(tree.latitude, tree.longitude))
    serializer = ser.TreeSerializer(filter(filter_func, trees), many=True)

    return Response(serializer.data)