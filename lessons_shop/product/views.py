from django.contrib.auth.models import User
from rest_framework import generics, mixins, viewsets, status
from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Subquery, Prefetch, FilteredRelation, Q, F, OuterRef
from .models import Lesson, Product, LessonView
from .serializers import AllProductsLessonStatsSerializer, ProductLessonStatsSerializer



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


'''

Реализовать API для отображения статистики по продуктам. 
Необходимо отобразить список всех продуктов на платформе, 
к каждому продукту приложить информацию:
Количество просмотренных уроков от всех учеников.
Сколько в сумме все ученики потратили времени на просмотр роликов.
Количество учеников занимающихся на продукте.
Процент приобретения продукта 
(рассчитывается исходя из количества полученных доступов к продукту деленное на общее количество пользователей на платформе).

'''

class ProductStatViewSet(generics.ListAPIView):
    serializer_class = AllProductsLessonStatsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        total_viewed = LessonView.objects.filter(lesson__in=OuterRef('lesson_set'), is_viewed=True).count()
        total_time = LessonView.objects.filter(lesson__in=OuterRef('lesson_set')).values('viewed_time')
        products = Product.objects.prefetch_related('lesson_set__lesson_views').annotate(
            total_viewed=Subquery(total_viewed),
            total_time=Sum(Subquery(total_time)),).all()
        return products
    