from django.shortcuts import render
from authentication.utils import is_auth
# Create your views here.


@is_auth('HTTP')
def marketplace(request):
    pass


def collections(request):
    pass


@is_auth('HTTP')
def my_nft(request):
    pass
