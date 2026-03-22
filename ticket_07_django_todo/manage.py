#!/usr/bin/env python
# запуск:
#   pip install django
#   python manage.py makemigrations
#   python manage.py migrate
#   python manage.py createsuperuser
#   python manage.py runserver
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError('не удалось импортировать django') from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
