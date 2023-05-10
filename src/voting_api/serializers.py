from typing import Any, Dict, List

from rest_framework import serializers

from .models import Company, Employee, Restaurant, Menu, Item, Voting, Results


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["name", "price", "weight"]


class MenuSerializer(serializers.ModelSerializer):
    items: List[Dict[str, Any]] = ItemSerializer(many=True)

    class Meta:
        model = Menu
        fields = "__all__"

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        items_data: List[Dict[str, Any]] = validated_data.pop("items")
        menu = Menu.objects.create(**validated_data)
        items = [
            Item.objects.create(menu=menu, **item_data) for item_data in items_data
        ]
        return {
            "menu": menu.id,
            "date": menu.date,
            "restaurant": menu.restaurant,
            "items": items,
        }


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = ["voting_id", "voting_date", "company"]


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = "__all__"
