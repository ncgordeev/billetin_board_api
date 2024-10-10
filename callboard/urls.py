from django.urls import path
from rest_framework.routers import DefaultRouter

from callboard.apps import CallboardConfig
from callboard.views import (AdCreateAPIView, AdDestroyAPIView, AdListAPIView,
                             AdRetrieveAPIView, AdUpdateAPIView, ReviewAPIView)

app_name = CallboardConfig.name
router = DefaultRouter()
router.register('review', ReviewAPIView, basename='review')
urlpatterns = [
                  path('', AdListAPIView.as_view(), name='ad_list'),
                  path('create/', AdCreateAPIView.as_view(), name='ad_create'),
                  path('detail/<int:pk>/', AdRetrieveAPIView.as_view(), name='ad_detail'),
                  path('update/<int:pk>/', AdUpdateAPIView.as_view(), name='ad_update'),
                  path('delete/<int:pk>/', AdDestroyAPIView.as_view(), name='ad_delete'),
              ] + router.urls
