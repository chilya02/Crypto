from django.http import JsonResponse
from . import services


def get_courses(request) -> JsonResponse:
    response = {
        'url': '/courses',
        'section': 'courses',
        'notifications': '',
        'html': services.get_courses_html()
    }
    return JsonResponse(response)
