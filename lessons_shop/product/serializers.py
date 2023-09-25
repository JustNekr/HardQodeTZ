from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Lesson, Product, LessonView


class AllProductsLessonStatsSerializer(serializers.ModelSerializer):
    viewed_time = serializers.IntegerField()
    is_viewed = serializers.BooleanField()

    class Meta:
        model = Lesson
        fields = ['title', 'video_link', 'viewed_time', 'is_viewed']


class ProductLessonStatsSerializer(serializers.ModelSerializer):
    viewed_time = serializers.IntegerField()
    is_viewed = serializers.BooleanField()
    updated_at = serializers.DateField()

    class Meta:
        model = Lesson
        fields = ['title', 'video_link', 'viewed_time', 'is_viewed', 'updated_at']


class ProductsStatsSerializer(serializers.ModelSerializer):
    total_viewed = serializers.IntegerField()
    total_time = serializers.IntegerField()
    total_students = serializers.IntegerField()
    buyer_percent = serializers.FloatField()

    class Meta:
        model = Product
        fields = ['owner', 'name', 'access_users', 'total_viewed', 'total_time', 'total_students', 'buyer_percent']
