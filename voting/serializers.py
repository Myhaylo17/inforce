# serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Restaurant, Menu, Vote

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'restaurant_name', 'date', 'description']
        read_only_fields = ['restaurant_name']

class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Vote
        fields = ['id', 'menu', 'user', 'date']
        read_only_fields = ['date', 'user']