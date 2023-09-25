#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lessons_shop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


'''
В этом задании у нас есть три бизнес-задачи на хранение:

Создать сущность продукта. У продукта должен быть владелец. 
Необходимо добавить сущность для сохранения доступов к продукту для пользователя.


Создать сущность урока. Урок может находиться в нескольких продуктах одновременно. 
В уроке должна быть базовая информация: название, ссылка на видео, длительность просмотра (в секундах).

Урок могут просматривать множество пользователей. 
Необходимо для каждого фиксировать время просмотра и фиксировать статус “Просмотрено”/”Не просмотрено”. 
Статус “Просмотрено” проставляется, если пользователь просмотрел 80% ролика.
'''