# views.py
from datetime import date
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Restaurant, Menu, Vote
from .serializers import RestaurantSerializer, MenuSerializer, VoteSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='today')
    def today_menu(self, request):
        today = date.today()
        menus = Menu.objects.filter(date=today)
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Забезпечуємо, що користувач не може проголосувати за два різних меню в один день.
        # Цю перевірку краще робити у валідаторі, але можна і тут.
        # Ваша модель вже має unique_together = ('user', 'date'), що забезпечує унікальність.
        # Тому тут достатньо просто зберегти.
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='today-results')
    def today_results(self, request):
        today = date.today()
        results = (
            Menu.objects.filter(date=today)
            .annotate(votes_count=Count('vote'))
            .values('restaurant__name', 'description', 'votes_count')
            .order_by('-votes_count')
        )
        return Response(list(results))