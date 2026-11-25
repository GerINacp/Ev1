import json
import os

from django.db import DatabaseError, connections
from django.http import HttpResponse
from django.template.loader import render_to_string


class DatabaseAvailabilityMiddleware:
    """Mantiene disponible una portada estática si la base de datos cae."""

    EXEMPT_PATHS = ('/static/', '/media/', '/favicon.ico')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
            return self.get_response(request)

        try:
            connection = connections['default']
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
        except DatabaseError:
            if request.path in ('/', '/inicio/'):
                json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'Tours', 'offline_tours.json')
                try:
                    with open(json_path, 'r', encoding='utf-8') as offline_file:
                        offline_tours = json.load(offline_file)
                except (OSError, json.JSONDecodeError):
                    offline_tours = []

                content = render_to_string(
                    'landing_offline_full.html',
                    {'offline_tours': offline_tours},
                    request=request,
                )
                return HttpResponse(content, status=200)

            content = render_to_string('database_down.html', request=request)
            return HttpResponse(content, status=503)

        return self.get_response(request)
