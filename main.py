"""
Punto de entrada alternativo para el servidor de desarrollo.

Uso:
    uv run main.py runserver
    uv run main.py migrate
"""
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
