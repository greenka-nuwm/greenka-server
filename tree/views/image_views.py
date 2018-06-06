from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import exceptions as exc
from rest_framework import status
from django.db import IntegrityError

from tree.models import TreeImages, Tree
from tree.permissions import IsTreeImageTreeOwner
from tree.serializers import TreeImageSerializer
from greenka.helpers import save_image


class TreeImageCreateView(APIView):
    """Add image"""
    queryset = TreeImages.objects.all()
    serializer_class = TreeImageSerializer
    permission_classes = (IsAuthenticated, IsTreeImageTreeOwner, )
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, pk):
        try:
            tree_obj = Tree.objects.get(pk=pk)
        except Exception:
            return Response({'error': 'Wrong tree ID.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not IsTreeImageTreeOwner().has_object_permission(request, self, tree_obj):
            raise exc.PermissionDenied()

        img = request.data.get('img')
        if not img:
            return Response({'error': 'No `img` data found.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # save image data on disk
        url = save_image(img, tree_obj)
        serializer = TreeImageSerializer(data={})
        if serializer.is_valid():
            try:
                serializer.save(url=url, visible=True, tree=tree_obj)
            except IntegrityError:
                return Response({'error': 'This image already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)