from django.shortcuts import render
from ..models import NftImage, Collection, NftPost
from django.http import JsonResponse
from django.template.loader import render_to_string
from . import services
from authentication.utils import is_auth
# Create your views here.
import json


def user_nft(request) -> JsonResponse:
    images = NftImage.objects.filter(owner=request.user)
    response = {
        'url': '/nft/my-nft',
        'section': 'nft',
        'menu_section': 'my-nft',
        'notifications': '',
        'html': render_to_string(request=request, template_name='nft/my-nft.html', context={'images': images})
    }
    return JsonResponse(response)


def collections(request):
    collections_list = Collection.objects.all()
    response = {
        'url': '/nft/collections',
        'section': 'nft',
        'menu_section': 'collections',
        'notifications': '',
        'html': render_to_string(request=request, template_name='nft/collections.html', context={'collections': collections_list})
    }
    return JsonResponse(response)


def marketplace(request):
    posts = NftPost.objects.all()
    response = {
        'url': '/nft/marketplace',
        'section': 'nft',
        'menu_section': 'marketplace',
        'notifications': '',
        'html': render_to_string(request=request, template_name='nft/marketplace.html',
                                 context={'posts': posts})
    }
    return JsonResponse(response)


def get_collections_list(request):
    collections_list = Collection.objects.filter(changeable=True)
    result = []
    for collection in collections_list:
        result.append(collection.name)
    return JsonResponse({'collections': result})
