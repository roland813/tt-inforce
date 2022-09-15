from django.db import IntegrityError
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from menu_choice.models import Restaurant
from menu_choice.serializers import MenuChoiceSerializer, VoteSerializer


class RestaurantViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Restaurant.objects.all().order_by("-votes")
    serializer_class = MenuChoiceSerializer
    permission_classes = (IsAuthenticated,)


class VoteViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            created_instance = serializer.create(validated_data=request.data)
            try:
                created_instance.save()
            except IntegrityError:
                return Response(
                    {
                        "message": "Already voted"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {
                    "message": "Vote cast successful"
                },
                status=status.HTTP_200_OK
            )
