from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from product.models import Product, Lesson, LessonView

usernames = ['even', 'odd', 'both']


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        for name in usernames:
            try:
                User.objects.create_superuser(name, password='123')
            except Exception:
                pass
        user_odd = User.objects.get(username='odd')
        product_odd = Product.objects.get_or_create(name='odd')[0]
        for i in range(1, 11, 2):
            lesson = Lesson.objects.get_or_create(title=f'{i}', video_link=f'https://{i}', duration_seconds=i * 100)[0]

            product_odd.lesson_set.add(lesson)
        user_odd.accessible_products.add(product_odd)
        user_odd_lessons = Lesson.objects.filter(products__in=user_odd.accessible_products.all()).distinct()
        for lesson in user_odd_lessons:
            LessonView.objects.get_or_create(lesson=lesson, user=user_odd, viewed_time=100)


        user_even = User.objects.get(username='even')
        product_even = Product.objects.get_or_create(name='even')[0]
        for i in range(2, 11, 2):
            lesson = Lesson.objects.get_or_create(title=f'{i}', video_link=f'https://{i}', duration_seconds=i * 100)[0]
            product_even.lesson_set.add(lesson)
        user_even.accessible_products.add(product_even)
        user_even_lessons = Lesson.objects.filter(products__in=user_even.accessible_products.all()).distinct()
        for lesson in user_even_lessons:
            LessonView.objects.get_or_create(lesson=lesson, user=user_even, viewed_time=100)

        user_both = User.objects.get(username='both')
        user_both.accessible_products.add(product_even)
        user_both.accessible_products.add(product_odd)
        user_both_lessons = Lesson.objects.filter(products__in=user_both.accessible_products.all()).distinct()
        for lesson in user_both_lessons:
            LessonView.objects.get_or_create(lesson=lesson, user=user_both, viewed_time=100)


