from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser

from callboard.models import Ad, Review
from callboard.paginators import AdPagination
from callboard.serializers import (AdListSerializer, AdRetrieveSerializer,
                                   AdSerializer, ReviewChangeSerializers,
                                   ReviewSerializers)
from users.permissions import IsAutor


class AdListAPIView(generics.ListAPIView):
    """Эндпоинт просмотра списка объявлений"""
    serializer_class = AdListSerializer
    permission_classes = [AllowAny]
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    filter_backends = [SearchFilter]
    search_fields = ['title']


class AdRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт просмотра одного объявления"""
    serializer_class = AdRetrieveSerializer
    queryset = Ad.objects.all()


class AdCreateAPIView(generics.CreateAPIView):
    """Эндпоинт создания объявления"""
    serializer_class = AdSerializer
    queryset = Ad.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт изменения объявления"""
    permission_classes = [IsAdminUser | IsAutor]
    serializer_class = AdSerializer
    queryset = Ad.objects.all()


class AdDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления объявления"""
    permission_classes = [IsAdminUser | IsAutor]
    queryset = Ad.objects.all()


class ReviewAPIViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев"""
    queryset = Review.objects.all()

    def get_queryset(self):
        ad_id = self.request.query_params.get('ad_id')
        if self.action == 'list' and ad_id:
            return self.queryset.filter(ad__id=ad_id)
        elif self.action in ['retrieve', 'destroy', 'update', 'partial_update']:
            return self.queryset
        raise ValidationError("Параметр 'ad_id' обязателен для получения списка комментариев.")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ReviewChangeSerializers
        return ReviewSerializers

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAutor() or IsAdminUser()]
        return super().get_permissions()
