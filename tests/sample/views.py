import random

from django.contrib.auth import get_user_model
from django.db.models import Max
from django.shortcuts import render
from django.views.generic import DetailView


def random_prime_user(request, **kwargs):
    max_id = get_user_model().objects.aggregate(max_id=Max('id'))['max_id']
    primes = []
    for possible_prime in range(2, max_id + 1):
        isPrime = True
        for num in range(2, int(possible_prime ** 0.5) + 1):
            if possible_prime % num == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(possible_prime)
    while True:
        pk = random.choice(primes)
        try:
            user = get_user_model().objects.get(pk=pk)
            return render(request, 'sample/random_user.html', {'user': user})
        except get_user_model().DoesNotExist:
            primes.remove(pk)


class RandomPrimeUser(DetailView):
    template_name = 'sample/random_user.html'

    def get_queryset(self):
        return get_user_model().objects.get_queryset()

    @staticmethod
    def calculate_prime_numbers(max_id):
        """
        Return iterator of prime numbers until given value.

        """
        for possible_prime in range(2, max_id + 1):
            isPrime = True
            for num in range(2, int(possible_prime ** 0.5) + 1):
                if possible_prime % num == 0:
                    isPrime = False
                    break
            if isPrime:
                yield possible_prime

    def get_max_user_id(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.aggregate(max_id=Max('id'))['max_id']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        max_id = self.get_max_user_id(queryset)
        primes = list(self.calculate_prime_numbers(max_id))

        while True:
            pk = random.choice(primes)
            try:
                return get_user_model().objects.get(pk=pk)
            except get_user_model().DoesNotExist:
                primes.remove(pk)
