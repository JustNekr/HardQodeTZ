
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from product.views import LessonsByProductsViewSet, ProductStatViewSet

urlpatterns = [
    path(r'products_lessons/', LessonsByProductsViewSet.as_view({'get': 'list'})),
    path(r'product_lessons/<int:pk>/', LessonsByProductsViewSet.as_view({'get': 'retrieve'})),
    path(r'product_stat/', ProductStatViewSet.as_view({'get': 'list'}))
]
