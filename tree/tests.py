from django.test import TestCase
from unittest import mock
from rest_framework.test import APIRequestFactory
from tree.models import Tree
from django.contrib.auth.models import User


class GetTreesTestCase(TestCase):
    """Test case for get_trees endpoint."""

    @classmethod
    def setUpClass(cls):
        super(GetTreesTestCase, cls).setUpClass()
        User.objects.create_user(username='test', password='123')

    def setUp(self):
        pass

    def tearDown(self):
        Tree.objects.all().delete()

    @mock.patch('rest_framework.permissions.IsAuthenticated')
    def test_get_trees_authenticated_one(self, auth_mock):
        """If user have one tree."""
        auth_mock.has_permission.return_value = True

        Tree.objects.create(latitude=5.0,
                            longitude=5.0,
                            tree_state=Tree.HEALTHY,
                            owner=User.objects.get(pk=1))
        factory = APIRequestFactory()
        request = factory.get('/trees/all')
        print(request.data)
        print(request)
