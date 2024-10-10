from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser

from callboard.models import Ad, Review
from callboard.paginators import AdPagination
from callboard.serializers import (AdListSerializer, AdRetrieveSerializer,
                                   AdSerializer, ReviewChangeSerializers,
                                   ReviewSerializers)
from users.permissions import IsAutor


class AdListAPIView(generics.ListAPIView):
    serializer_class = AdListSerializer
    permission_classes = [AllowAny]
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    filter_backends = [SearchFilter]
    search_fields = ['title']


class AdRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = AdRetrieveSerializer
    queryset = Ad.objects.all()


class AdCreateAPIView(generics.CreateAPIView):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser | IsAutor]
    serializer_class = AdSerializer
    queryset = Ad.objects.all()


class AdDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser | IsAutor]
    queryset = Ad.objects.all()


class ReviewAPIView(viewsets.ModelViewSet):
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ReviewChangeSerializers
        return ReviewSerializers

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser() or IsAutor()]
        return super().get_permissions()
