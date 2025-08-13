import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.utils import timezone
from voting.models import Restaurant, Menu, Vote
from rest_framework_simplejwt.tokens import AccessToken


# Фікстура для створення неавтентифікованого клієнта
@pytest.fixture
def api_client():
    return APIClient()


# Фікстура для створення автентифікованого клієнта
@pytest.fixture
def authenticated_client(api_client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='testpassword')
    token = AccessToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


# Фікстура для створення ресторану
@pytest.fixture
def restaurant():
    return Restaurant.objects.create(name='Test Restaurant')


# Фікстура для створення меню
@pytest.fixture
def menu(restaurant):
    return Menu.objects.create(restaurant=restaurant, date=timezone.localdate(), description='Soup, salad')


# Тест на створення ресторану
@pytest.mark.django_db
def test_create_restaurant(authenticated_client):
    url = reverse('restaurant-list')
    data = {'name': 'Pizza House'}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Restaurant.objects.count() == 1
    assert Restaurant.objects.get().name == 'Pizza House'


# Тест на отримання меню на сьогодні
@pytest.mark.django_db
def test_get_today_menu(authenticated_client, menu):
    url = reverse('menu-today')
    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['description'] == 'Soup, salad'


# Тест на успішне голосування
@pytest.mark.django_db
def test_vote_successfully(authenticated_client, menu):
    url = reverse('vote-list')
    data = {'menu': menu.id}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Vote.objects.count() == 1


# Тест на заборону повторного голосування
@pytest.mark.django_db
def test_vote_once_per_day(authenticated_client, menu):
    url = reverse('vote-list')
    data = {'menu': menu.id}
    # Перше успішне голосування
    authenticated_client.post(url, data, format='json')
    # Друга спроба голосування, яка має завершитися помилкою
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "You have already voted today." in str(response.data)


# Тест на отримання результатів голосування
@pytest.mark.django_db
def test_get_vote_results(authenticated_client, menu):
    url = reverse('vote-today-results')
    # Створюємо кілька голосів за одне меню
    Vote.objects.create(user=User.objects.get(username='testuser'), menu=menu)
    Vote.objects.create(user=User.objects.create_user(username='user2'), menu=menu)

    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK