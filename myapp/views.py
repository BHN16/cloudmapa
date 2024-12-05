from django.shortcuts import render
from .dynamo import table
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests
from django.views.decorators.http import require_http_methods


def map_view(request):
    response = table.scan()
    items = response['Items']
    print(items)
    return render(request, 'map.html', {'items': items})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def universal_view(request):
    # Obtener el ID del contenedor Docker desde la metadata de ECS
    container_id = "unknown"
    try:
        # Intentar con la URL para el modo de red 'bridge' o 'default'
        ecs_metadata_url = "http://169.254.170.2/v2/metadata"
        response = requests.get(ecs_metadata_url)
        if response.status_code != 200:
            # Si falla, intentar con la URL para el modo de red 'awsvpc'
            ecs_metadata_url = "http://169.254.170.4/v2/metadata"
            response = requests.get(ecs_metadata_url)

        if response.status_code == 200:
            metadata = response.json()
            container_id = metadata.get('DockerId', 'unknown')
    except Exception as e:
        container_id = str(e)

    if request.method == 'GET':
        return JsonResponse({'status': 'success', 'message': 'GET request received', 'container_id': container_id})
    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            return JsonResponse({'status': 'success', 'data': body, 'container_id': container_id})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON', 'container_id': container_id}, status=400)
