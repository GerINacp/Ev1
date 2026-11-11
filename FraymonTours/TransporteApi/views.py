import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from Tours.models import Viajes


def _serialize_tour(tour):
    return {
        'id': tour.codigo,
        'nombre': tour.nombre,
        'descripcion': tour.descripcion or '',
        'precio': int(tour.precio),
        'precio_clp': int(tour.precio),
        'imagen': (tour.imagen.url if tour.imagen else ''),
        'creado': tour.creado.isoformat() if tour.creado else None,
    }


def tours_api(request):
    tours = Viajes.objects.order_by('nombre')
    data = {
        'status': 'ok',
        'source': 'local_db',
        'count': tours.count(),
        'tours': [_serialize_tour(tour) for tour in tours],
    }
    return JsonResponse(data, safe=True)


def tour_detail_api(request, tour_id):
    tour = get_object_or_404(Viajes, codigo=tour_id)
    return JsonResponse({
        'status': 'ok',
        'source': 'local_db',
        'tour': _serialize_tour(tour),
    }, safe=True)


def _normalize_external_tour(item):
    if isinstance(item, dict):
        return {
            'id': item.get('id') or item.get('codigo') or item.get('tour_id'),
            'nombre': item.get('nombre') or item.get('title') or item.get('name') or 'Tour',
            'descripcion': item.get('descripcion') or item.get('description') or '',
            'precio': item.get('precio') or item.get('price') or item.get('precio_clp') or 0,
            'precio_clp': item.get('precio_clp') or item.get('precio') or item.get('price') or 0,
            'imagen': item.get('imagen') or item.get('image') or item.get('img') or '',
            'origen': 'external_api',
        }
    return None


def _fetch_external_api():
    url = os.getenv('TOURS_API_URL')
    if not url:
        return {'status': 'not_configured', 'message': 'No existe la variable de entorno TOURS_API_URL'}

    headers = {'Accept': 'application/json'}
    token = os.getenv('TOURS_API_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'

    request = Request(url, headers=headers, method='GET')
    try:
        with urlopen(request, timeout=20) as response:
            payload = response.read().decode('utf-8')
            data = json.loads(payload)
    except (Exception) as exc:
        return {
            'status': 'error',
            'message': f'No se pudo conectar a la API externa: {exc}',
        }

    items = data
    if isinstance(data, dict):
        if 'tours' in data:
            items = data['tours']
        elif 'data' in data:
            items = data['data']
        elif 'results' in data:
            items = data['results']
        else:
            items = [data]

    normalized = []
    for item in items:
        parsed = _normalize_external_tour(item)
        if parsed:
            normalized.append(parsed)

    return {
        'status': 'ok',
        'source': 'external_api',
        'count': len(normalized),
        'tours': normalized,
    }


def external_tours_api(request):
    result = _fetch_external_api()
    return JsonResponse(result)


def google_places_tours_api(request):
    api_key = getattr(settings, 'GOOGLE_API_KEY', None) or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return JsonResponse({
            'status': 'error',
            'message': 'Falta la API key de Google Maps. Define GOOGLE_API_KEY en el entorno o en settings.py.',
        }, status=500)

    query = request.GET.get('q', 'tour en Chile')
    country = request.GET.get('country', 'Chile')
    full_query = f"{query} {country}"

    params = {
        'query': full_query,
        'key': api_key,
        'language': 'es',
        'region': 'cl',
        'type': 'tourist_attraction',
    }
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?' + urlencode(params)

    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except Exception as exc:
        return JsonResponse({
            'status': 'error',
            'message': f'Error al consultar Google Places: {exc}',
        }, status=502)

    if payload.get('status') != 'OK':
        return JsonResponse({
            'status': 'error',
            'message': payload.get('error_message', 'Google Places respondió con un error.'),
            'google_status': payload.get('status'),
        }, status=400)

    results = []
    for item in payload.get('results', [])[:10]:
        results.append({
            'place_id': item.get('place_id'),
            'nombre': item.get('name'),
            'direccion': item.get('formatted_address'),
            'rating': item.get('rating'),
            'tipo': item.get('types'),
            'icono': item.get('icon'),
            'lat': item.get('geometry', {}).get('location', {}).get('lat'),
            'lng': item.get('geometry', {}).get('location', {}).get('lng'),
        })

    return JsonResponse({
        'status': 'ok',
        'source': 'google_places',
        'query': full_query,
        'count': len(results),
        'results': results,
    })
