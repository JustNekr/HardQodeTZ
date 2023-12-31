# Generated by Django 4.2.5 on 2023-09-25 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0004_alter_product_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='products',
            field=models.ManyToManyField(related_name='lesson_set', to='product.product'),
        ),
        migrations.AlterField(
            model_name='lessonview',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_views', to='product.lesson'),
        ),
        migrations.AlterUniqueTogether(
            name='lessonview',
            unique_together={('lesson', 'user')},
        ),
    ]
