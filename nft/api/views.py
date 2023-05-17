from django.http import JsonResponse
from . import services
from authentication.utils import is_auth
import json


@is_auth('JSON')
def user_nft(request) -> JsonResponse:
    response = {
        'url': '/nft/my-nft',
        'section': 'nft',
        'menu_section': 'my-nft',
        'notifications': '',
        'html': services.user_nft_html(request.user)
    }
    return JsonResponse(response)


@is_auth('JSON')
def collections(request):
    response = {
        'url': '/nft/collections',
        'section': 'nft',
        'menu_section': 'collections',
        'notifications': '',
        'html': services.collections_html(user=request.user)
    }
    return JsonResponse(response)


@is_auth('JSON')
def marketplace(request):
    response = {
        'url': '/nft/marketplace',
        'section': 'nft',
        'menu_section': 'marketplace',
        'notifications': '',
        'html': services.marketplace_html(user=request.user)
    }
    return JsonResponse(response)


@is_auth('JSON')
def nft_info(request, nft_id):
    response = {
        'url': f'/nft/nft-info/{nft_id}',
        'section': 'nft',
        'menu_section': services.select_nft_section(user=request.user, nft_id=nft_id),
        'notifications': '',
        'html': services.get_nft_info_html(user=request.user, nft_id=nft_id)
    }

    return JsonResponse(response)


@is_auth('JSON')
def post_info(request, post_id):
    response = {
        'url': f'/nft/marketplace/{post_id}',
        'section': 'nft',
        'menu_section': services.select_post_section(user=request.user, post_id=post_id),
        'notifications': '',
        'html': services.get_post_html(user=request.user, post_id=post_id)
    }
    return JsonResponse(response)


@is_auth('JSON')
def get_collections_list(request):
    return JsonResponse({'collections': services.get_collections_list(user=request.user)})


@is_auth('JSON')
def add_nft(request):
    data = json.loads(request.POST['info'])
    file = request.FILES['file']
    services.create_nft(user=request.user, data=data, file=file)
    return JsonResponse({'success': True})


@is_auth('JSON')
def sell_nft(request):
    data = json.loads(request.body)
    services.sell_nft(data=data)
    return JsonResponse({'success': True})


@is_auth('JSON')
def buy_nft(request):
    data = json.loads(request.body)
    services.buy_nft(user=request.user, data=data)
    return JsonResponse({'success': True})
