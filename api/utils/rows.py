from authentication.models import User
from p2p.models import Post, BuyPost, NewOrder, Order
from courses.models import Course

def generate_post_row(post: Post, user: User) -> dict:
    if post.user == user:
        common_class = 'my'
        arg = f''' downloadContent('/api/get-post-info/{"buy" if isinstance(post, BuyPost) else "sell"}/{post.id}')'''
    else:
        common_class = ''
        arg = f''' downloadContent('/api/get-{"buy" if isinstance(post, BuyPost) else "sell"}-info/{post.id}')'''
    row = {'items': [
        {
            'class': f'{common_class} la',
            'text': f'<div class="with-info"><span>{post.user.username}</span><span class="info">{post.currency}</span></div>'
        },
        {
            'class': f'{common_class}',
            'text': f'{post.price}'
        },
        {
            'class': f'{common_class}',
            'text': f'{post.limit}'
        },
        {
            'class': f'{common_class} la',
            'text': f'{post.get_bank_display()}'
        }],
        'arg': arg
    }
    return row


def generate_user_post_row(post: Post) -> dict:
    row = {'items':
        [
            {
                'class': 'la',
                'text': f'{post.currency}'
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
        ],
        'arg': f'''downloadContent('/api/get-post-info/{"buy" if isinstance(post, BuyPost) else "sell"}/{post.id}')'''
    }
    return row


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


def generate_currency_row(course: Course) -> dict:
    row = {'items': [
        {
            'class': 'f' 'la',
            'text': course.currency
        },
        {
            'class': '',
            'text': course.RUB
        },
        {
            'class': '',
            'text': course.change
        },
        {
            'class': '',
            'text': course.volume
        },
        {
            'class': '',
            'text': course.quote_volume
        },
        {
            'class': '',
            'text': f'''<button class="blue-btn" onclick="window.location.replace('/p2p/sell')">Купить</button>'''
        },
        {
            'class': '',
            'text': f'''<button class="blue-btn" onclick="window.location.replace('/p2p/sell')">Продать</button>'''
        }],
        'arg': ''
    }
    return row