from django.http import JsonResponse
from ..utils import is_auth


@is_auth('JSON')
def get_balance(request) -> JsonResponse:
    return JsonResponse({'balance': request.user.balance})
