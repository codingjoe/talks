import pytest
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from model_mommy import mommy

from sample import views


class TestRandomPrimeUser:
    view = views.RandomPrimeUser

    def test_calculate_prime_numbers__one(self):
        primes = self.view.calculate_prime_numbers(1)
        with pytest.raises(StopIteration):
            next(primes)

    def test_calculate_prime_numbers__two(self):
        primes = self.view.calculate_prime_numbers(2)
        assert next(primes) == 2
        with pytest.raises(StopIteration):
            next(primes)

    def test_calculate_prime_numbers__many(self):
        assert list(self.view.calculate_prime_numbers(20)) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_get_get_max_user_id__empty(self):
        assert self.view().get_max_user_id(queryset=get_user_model().objects.none()) is None

    def test_get_get_max_user_id__one(self, db):
        user = mommy.make(get_user_model())
        assert self.view().get_max_user_id() == user.pk == 1

    def test_get_get_max_user_id__last_one(self, db):
        users = mommy.make(get_user_model(), _quantity=2)
        assert self.view().get_max_user_id() == users[-1].pk == 2

    def test_get_queryset(self):
        assert isinstance(self.view().get_queryset(), QuerySet)

    def test_get_object(self):
        pass
