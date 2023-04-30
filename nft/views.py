from django.shortcuts import render
from authentication.utils import is_auth
# Create your views here.
from django.shortcuts import render


@is_auth('HTTP')
def marketplace(request):
    return render(request=request, template_name='nft/marketplace.html', context={'section': "nft"})


def collections(request):
    return render(request=request, template_name='nft/collections.html', context={'section': "nft"})


@is_auth('HTTP')
def my_nft(request):
    return render(request=request, template_name='nft/my-nft.html', context={'section': "nft"})
