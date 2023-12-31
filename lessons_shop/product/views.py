from django.contrib.auth.models import User
from django.db.models.functions import Cast
from rest_framework import generics, mixins, viewsets, status
from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Subquery, Prefetch, FilteredRelation, Q, F, OuterRef, FloatField
from .models import Lesson, Product, LessonView
from .serializers import AllProductsLessonStatsSerializer, ProductLessonStatsSerializer, ProductsStatsSerializer


class LessonsByProductsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AllProductsLessonStatsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        lesson_view = LessonView.objects.filter(user=self.request.user, lesson__pk=OuterRef('pk'))
        users_lessons = Lesson.objects.annotate(
            viewed_time=Subquery(lesson_view.values('viewed_time')),
            is_viewed=Subquery(lesson_view.values('is_viewed'))).filter(
            products__in=self.request.user.accessible_products.all()).distinct()
        return users_lessons

    def retrieve(self, request, *args, **kwargs):
        product = self.request.user.accessible_products.get(pk=kwargs['pk'])
        if product:

            lesson_view = LessonView.objects.filter(user=self.request.user, lesson__pk=OuterRef('pk'))

            user_product_lessons = Lesson.objects.annotate(
                viewed_time=Subquery(lesson_view.values('viewed_time')),
                is_viewed=Subquery(lesson_view.values('is_viewed')),
                updated_at=Subquery(lesson_view.values('updated_at'))).filter(
                products__in=(product,)).distinct()
            data = ProductLessonStatsSerializer(user_product_lessons, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response()


class ProductStatViewSet(generics.ListAPIView):
    serializer_class = ProductsStatsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        products = Product.objects.prefetch_related('lesson_set__lesson_views', 'access_users').annotate(
            total_viewed=Count('lesson_set__lesson_views', filter=Q(lesson_set__lesson_views__is_viewed=True), distinct=True),
            total_time=Sum('lesson_set__lesson_views__viewed_time', filter=Q(lesson_set__lesson_views__user__in=F('access_users'))),
            total_students=Count('access_users', distinct=True),
            buyer_percent=F('total_students') / Cast(User.objects.all().count(), output_field=FloatField())
        ).all()
        return products
