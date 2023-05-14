from django.http import JsonResponse
from django.template.loader import render_to_string
from . import services
from authentication.utils import is_auth
# Create your views here.
import json


@is_auth('JSON')
def get_p2p_interface(request) -> JsonResponse:
    response = {
        'url': '/p2p/',
        'section': 'courses',
        'notifications': '',
        'html': render_to_string(request=request, template_name='p2p/p2p_template_dry.html', context={})
    }
    return JsonResponse(response)


@is_auth('JSON')
def get_buy_list(request, section: str) -> JsonResponse:
    response = {
        'url': '/p2p/buy',
        'section': 'p2p',
        'menu_section': 'sell',
        'notifications': '',
        'html': services.get_buy_list_html(section, request.user)
    }
    return JsonResponse(response)


@is_auth('JSON')
def get_sell_list(request, section: str) -> JsonResponse:
    response = {
        'url': '/p2p/sell',
        'section': 'p2p',
        'menu_section': 'buy',
        'notifications': '',
        'html': services.get_sell_list_html(section, request.user)
    }
    return JsonResponse(response)


@is_auth('JSON')
def get_posts_list(request, section: str) -> JsonResponse:
    response = {
        'url': '/p2p/my-posts',
        'section': 'p2p',
        'menu_section': 'my-posts',
        'notifications': '',
        'html': services.get_user_posts_list_html(request.user, section)
    }
    return JsonResponse(response)


@is_auth('JSON')
def get_orders_list(request) -> JsonResponse:
    response = {
        'url': '/p2p/my-orders',
        'section': 'p2p',
        'menu_section': 'my-orders',
        'notifications': '',
        'html': services.get_orders_list_html(user=request.user),
    }
    return JsonResponse(response)


@is_auth('JSON')
def get_buy_post_info(request, post_id: int) -> JsonResponse:
    response = {
        'url': f'/p2p/buy/{post_id}',
        'section': 'p2p',
        'menu_section': 'sell',
        'notifications': '',
        'html': services.get_buy_post_html(request.user, post_id),
    }
    return JsonResponse(response)


@is_auth('JSON')
def get_sell_post_info(request, post_id: int) -> JsonResponse:
    response = {
        'url': f'/p2p/sell/{post_id}',
        'section': 'p2p',
        'menu_section': 'buy',
        'notifications': '',
        'html': services.get_sell_post_html(post_id),
    }
    return JsonResponse(response)


@is_auth('JSON')
def get_my_post_info(request, section: str, post_id: int) -> JsonResponse:
    response = {
        'url': f'/p2p/my-posts/{section}/{post_id}',
        'section': 'p2p',
        'menu_section': 'my-posts',
        'notifications': '',
        'html': services.get_my_post_html(section, post_id)
    }
    return JsonResponse(response)


@is_auth('JSON')
def get_new_order_info(request, order_id: int) -> JsonResponse:
    response = {
        'url': f'/p2p/my-orders/new/{order_id}',
        'section': 'p2p',
        'menu_section': 'my-orders',
        'notifications': '',
        'html': services.get_new_order_html(order_id=order_id, user=request.user),
    }
    return JsonResponse(response)


@is_auth('JSON')
def get_user_currency_count(request, currency: str) -> JsonResponse:
    user = request.user
    return JsonResponse(services.get_user_currency_count(user, currency))


@is_auth('JSON')
def add_post(request) -> JsonResponse:
    success = False
    if request.method == 'POST':
        success = services.add_post(request.user, json.loads(request.body))
    return JsonResponse({'success': success})


@is_auth('JSON')
def send_message(request) -> JsonResponse:
    if request.method == 'POST':
        body = json.loads(request.body)
        result = services.add_message(request.user, body['id'], body['message'])
    return JsonResponse(result)


@is_auth('JSON')
def create_order(request) -> JsonResponse:
    result = services.create_order(request.user, json.loads(request.body))
    return JsonResponse(result)


@is_auth('JSON')
def get_messages(request, order_id: int) -> JsonResponse:
    html = services.get_order_messages_html(order_id=order_id, user=request.user)
    return JsonResponse({'html': html})


@is_auth('JSON')
def get_messages_interface(request, order_id: int) -> JsonResponse:
    html = services.get_messages_interface_html(order_id=order_id)
    return JsonResponse({'html': html, 'id': order_id})


@is_auth('JSON')
def change_order_count(request, order_id: int) -> JsonResponse:
    count = json.loads(request.body)['count']
    return JsonResponse(services.change_order_count(order_id=order_id, count=count))


@is_auth('JSON')
def pay_order(request) -> JsonResponse:
    order_id = json.loads(request.body)['id']
    return JsonResponse(services.pay_order(order_id=order_id))


@is_auth('JSON')
def add_card_number(request) -> JsonResponse:
    body = json.loads(request.body)
    order_id = body['id']
    card_number = body['cardNumber']
    return JsonResponse(services.add_card_number(order_id=order_id, card_number=card_number))


@is_auth('JSON')
def delete_post(request) -> JsonResponse:
    body = json.loads(request.body)
    post_id = body['id']
    section = body['section']
    return JsonResponse(services.delete_post(post_id=post_id, section=section))


@is_auth('JSON')
def close_order(request) -> JsonResponse:
    body = json.loads(request.body)
    order_id = body['id']
    return JsonResponse(services.close_order(order_id=order_id))


@is_auth('JSON')
def abort_order(request) -> JsonResponse:
    body = json.loads(request.body)
    order_id = body['id']
    return JsonResponse(services.delete_order(order_id))
