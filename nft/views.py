from authentication.utils import is_auth
from django.shortcuts import render
from .models import NftImage


@is_auth('HTTP')
def marketplace(request):
    return render(request=request, template_name='nft/loaders/marketplace.html', context={'section': "nft"})


@is_auth('HTTP')
def collections(request):
    return render(request=request, template_name='nft/loaders/collections.html', context={'section': "nft"})


@is_auth('HTTP')
def my_nft(request):
    return render(request=request, template_name='nft/loaders/my-nft.html', context={'section': "nft"})


@is_auth('HTTP')
def nft_info(request, nft_id):
    return render(request=request, template_name='nft/loaders/nft-info.html', context={'section': "nft", 'nft_id': nft_id})


@is_auth('HTTP')
def post_info(request, post_id):
    return render(request=request, template_name='nft/loaders/post_info.html',
                  context={'section': "nft", 'post_id': post_id})
