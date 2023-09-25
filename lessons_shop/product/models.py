from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

PERCENT_AS_FULL = 0.8


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    access_users = models.ManyToManyField(User, blank=True, related_name='accessible_products')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    products = models.ManyToManyField(Product, related_name='lesson_set')
    title = models.CharField(max_length=200)
    video_link = models.URLField()
    duration_seconds = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class LessonView(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_time = models.PositiveIntegerField(default=0)
    is_viewed = models.BooleanField(default=False)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = [["lesson", "user"]]

    def __str__(self):
        return f'{self.user.username} viewed {self.lesson.title}'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.lesson.duration_seconds * PERCENT_AS_FULL <= self.viewed_time:
            self.is_viewed = True

        super(LessonView, self).save()
        return


# def product_access_changed(sender, **kwargs):
#     # print(sender)
#     pass
#
#
# m2m_changed.connect(product_access_changed, sender=Product.access_users.through)
# class ProductAccess(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'Access to {self.product} for {self.user.username}'