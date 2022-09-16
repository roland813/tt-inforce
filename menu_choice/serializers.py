from rest_framework import serializers
from menu_choice.models import Restaurant, Vote, Menu


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ("id", "restaurant", "day", "content", "votes_count")


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ("id", "menu",)
