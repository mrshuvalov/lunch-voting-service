from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def items(self):
        return Item.objects.filter(menu=self)


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    weight = models.CharField(max_length=50)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lunch_time = models.TimeField(default="14:00")


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)


class Voting(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.PROTECT)


class Results(models.Model):
    id = models.AutoField(primary_key=True)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    points = models.IntegerField(default=0)
