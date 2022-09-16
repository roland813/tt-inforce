from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from menu_choice.models import Restaurant, Menu, Vote
from menu_choice.serializers import RestaurantSerializer, MenuSerializer

RESTAURANTS_URL = reverse("menu_choice:restaurant-list")
MENU_URL = reverse("menu_choice:menu-list")
SELECTED_MENU_URL = reverse("menu_choice:menu-select-menu")


class UnauthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_restaurants_list(self):
        res = self.client.get(RESTAURANTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_menu_list(self):
        res = self.client.get(MENU_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_restaurant(self):
        Restaurant.objects.create(name="testrest")

        response = self.client.get(RESTAURANTS_URL)

        restaurant = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurant, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_menu(self):
        restaurant = Restaurant.objects.create(name="testrest")
        Menu.objects.create(
            restaurant_id=restaurant.id,
            day="Friday",
            content="test_content"
        )

        response = self.client.get(MENU_URL)

        menu = Menu.objects.all()
        serializer = MenuSerializer(menu, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class SelectMenuTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_selected_menu(self):
        restaurant1 = Restaurant.objects.create(name="testrest1")
        restaurant2 = Restaurant.objects.create(name="testrest2")
        Menu.objects.create(
            restaurant_id=restaurant1.id,
            day="Friday",
            content="test_content"
        )
        menu2 = Menu.objects.create(
            restaurant_id=restaurant2.id,
            day="Friday",
            content="test_content"
        )

        Vote.objects.create(menu=menu2, user_id=self.user.id)

        response = self.client.get(SELECTED_MENU_URL)

        serializer = MenuSerializer(menu2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
