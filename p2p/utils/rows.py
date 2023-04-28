from authentication.models import User
from p2p.models import Post, BuyPost, NewOrder, Order
from courses.models import Course


def get_discussing_order_row(order: NewOrder) -> dict:
    post_type = order.post_type
    if post_type == 'buy':
        post = order.buy_post
    else:
        post = order.sell_post
    row = {'items': [
        {
            'class': 'la',
            'text': f'<div class="with-info"><span>{post.user.username}</span><span class="info">{post.currency}</span></div>'
        },
        {
            'class': '',
            'text': f'{post.price}'
        },
        {
            'class': '',
            'text': f'{post.limit}'
        },
        {
            'class': 'la',
            'text': f'{post.get_bank_display()}'
        },
        {
            'class': 'la',
            'text': f'{"Покупка" if post_type == "sell" else "Продажа"}'
        }],
        'arg': f'''downloadContent('/api/get-new-order-info/{order.id}')'''
    }
    return row


def get_new_order_row(order: NewOrder, user: User, func: str) -> dict:
    post = order.post
    row = {'items': [
        {
            'class': 'la',
            'text': f'<div class="with-info"><span>{order.get_other_side(user).username}</span><span class="info">{post.currency}</span></div> '
        },
        {
            'class': '',
            'text': f'{post.price}'
        },
        {
            'class': '',
            'text': f'{order.count}'
        },
        {
            'class': '',
            'text': f'{order.sum}'
        }],
        'arg': func.format(order.id)
    }
    return row


def get_order_row(order: Order, user: User) -> dict:
    action = "Покупка" if user == order.buyer else "Продажа"
    row = {'items': [
        {
            'class': 'la',
            'text': f'<div class="with-info"><span>{order.get_other_side(user).username}</span><span class="info">{order.currency}</span></div> '
        },
        {
            'class': '',
            'text': f'{order.price}'
        },
        {
            'class': '',
            'text': f'{order.count}'
        },
        {
            'class': '',
            'text': f'{order.sum}'
        },
        {
            'class': '',
            'text': f'{action}'
        }],
        'arg': "downloadContent('/api/get-order-info/{}".format(order.id)
    }
    return row
