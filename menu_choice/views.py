from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from datetime import date as d

from rest_framework.response import Response

from menu_choice.models import Restaurant, Menu, Vote
from menu_choice.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    VoteSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)


class MenuViewSet(viewsets.ModelViewSet):

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        today = d.today()
        return Menu.objects.filter(day=today.strftime('%A'))

    @action(
        methods=["GET"],
        detail=False,
        url_path="selected",
        permission_classes=[IsAuthenticated],
    )
    def select_menu(self, request):
        selected_menu = max(self.get_queryset(),
                            key=lambda menu: menu.votes_count)
        serializer = self.get_serializer(selected_menu)

        try:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class VoteViewSet(viewsets.ModelViewSet):

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Vote.objects.filter(user_id=self.request.user.id)
