from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory

from polls import apiviews

class TestPoll(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)  # type: ignore
        self.view = apiviews.PollViewSet.as_view({'get': 'list'})
        self.uri = '/polls/'

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            username='test',
            email='test@example.org',
            password='test',
        )

    def test_list(self):
        request = self.factory.get(self.uri, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         f'Expected Response Code 200 but received {response.status_code}')
