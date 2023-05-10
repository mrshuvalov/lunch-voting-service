from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from .models import Company, Restaurant, Menu, Voting


class LunchVotingServiceTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.login(username="shuvalov_nv", password="qwerty!1234")
        self.user = User.objects.create_user(
            username="shuvalov_nv", password="qwerty!1234"
        )
        self.company = Company.objects.create(name="MindTales")
        self.restaurant = Restaurant.objects.create(name="Kata")
        self.menu = Menu.objects.create(date="2023-05-10", restaurant=self.restaurant)
        self.menu.items.create(name="Rolls", price=20000, weight=400, menu=self.menu)
        self.vote = Voting.objects.create(date="2023-05-10", company=self.company)

    def test_register_account(self):
        url = "/accounts/register/"
        data = {
            "login": "new_user",
            "username": "new_user",
            "password": "password1!23",
            "password_confirm": "password1!23",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = "/accounts/login/"
        data = {"login": "shuvalov_nv", "password": "qwerty!1234"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_company(self):
        url = "/companies/"
        data = {"name": "New Company"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_restaurant(self):
        url = "/restaurants/"
        data = {"name": "New Restaurant"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
