import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_mommy import mommy


class TestGetRandomUser:
    """"""

    def setup(self):
        """Database contains a set of Users."""
        return mommy.make(get_user_model(), _quantity=20)

    def test_get_user(self, db, client):
        self.setup()
        url = reverse('rnd_user_2')

        response = client.get(url)

        assert response.status_code == 200
        assert 'user' in response.context

    def test_no_user(self, db, client):
        url = reverse('rnd_user_2')

        response = client.get(url)

        assert response.status_code == 404
