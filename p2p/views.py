from django.shortcuts import render
from authentication.utils import is_auth


@is_auth('HTTP')
def buy(request):
    return render(
        request=request,
        template_name='p2p/buy.html',
        context={'section': 'p2p'}
    )


@is_auth('HTTP')
def buy_post(request, post_id: int):
    return render(
        request=request,
        template_name='p2p/post_buy_info.html',
        context={'section': 'p2p', 'id': post_id}
    )


@is_auth('HTTP')
def sell(request):
    return render(
        request=request,
        template_name='p2p/sell.html',
        context={'section': 'p2p'}
    )


@is_auth('HTTP')
def sell_post(request, post_id: int):
    return render(
        request=request,
        template_name='p2p/post_sell_info.html',
        context={'section': 'p2p', 'id': post_id}
    )


@is_auth('HTTP')
def my_posts(request):
    return render(
        request=request,
        template_name='p2p/my_posts.html',
        context={'section': 'p2p'}
    )


@is_auth('HTTP')
def my_post(request, section: str, post_id: int):
    return render(
        request=request,
        template_name='p2p/my_post_info.html',
        context={
            'section': 'p2p', 
            'id': post_id,
            'post_section': section
            }
    )


@is_auth('HTTP')
def my_orders(request):
    return render(
        request=request,
        template_name='p2p/my_orders.html',
        context={'section': 'p2p'}
    )


@is_auth('HTTP')
def my_order(request, order_id):
    return render(
        request=request,
        template_name='p2p/my_order_info.html',
        context={'section': 'p2p', 'id': order_id}
    )


@is_auth('HTTP')
def my_new_order(request, order_id):
    return render(
        request=request,
        template_name='p2p/my_new_order_info.html',
        context={'section': 'p2p', 'id': order_id}
    )