from authentication.utils import is_auth
from django.shortcuts import render
from .models import NftImage


@is_auth('HTTP')
def marketplace(request):
    return render(request=request, template_name='nft/loaders/marketplace.html', context={'section': "nft"})


def collections(request):
    return render(request=request, template_name='nft/loaders/collections.html', context={'section': "nft"})


@is_auth('HTTP')
def my_nft(request):
    return render(request=request, template_name='nft/loaders/my-nft.html', context={'section': "nft"})
