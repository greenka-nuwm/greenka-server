from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from tree.serializers import UserSerializer
from tree.views.image_views import *
from tree.views.poly_views import *
from tree.views.sort_views import *
from tree.views.type_views import *
from tree.views.tree_views import *


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_user(request):
    """Return info about self."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)