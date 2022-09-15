from datetime import datetime
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from menu_choice.models import Restaurant, Vote


class MenuChoiceSerializer(serializers.ModelSerializer):
    weekday = datetime.today().weekday()

    menu_days = {
        0: "menu_monday",
        1: "menu_tuesday",
        2: "menu_wednesday",
        3: "menu_thursday",
        4: "menu_friday",
        5: "menu_saturday",
        6: "menu_sunday",
    }

    current_menu = menu_days[weekday]
    menu = serializers.CharField(source=current_menu)
    votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ["id", "name", "menu", "votes"]


class VoteSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField()

    def create(self, validated_data):
        restaurant = get_object_or_404(
            Restaurant,
            name=validated_data["restaurant_name"]
        )
        vote = Vote()
        vote.restaurant = restaurant
        try:
            vote.save(commit=False)
        except IntegrityError:
            return vote
        return vote

    class Meta:
        model = Vote
        exclude = ("id", "restaurant")
