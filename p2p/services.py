from p2p.utils import modal, html
from p2p.utils import menu
from p2p.utils.info import get_post_info, get_post_actions
from authentication.models import User
from p2p.models import NewOrder, BuyPost, SellPost, Order, Message
from django.template.loader import render_to_string

CURRENCIES = ('USDT', 'BTC', 'ETH', 'KPFU', 'SOL')


def get_sell_list_html(section: str, user: User) -> str:
    result_html = render_to_string(
        template_name='menu/currency_menu.html',
        context={'section': section, 'p2p_section': 'sell', 'currencies': CURRENCIES}
    )

    if section == 'all':
        posts = SellPost.objects.order_by('price')
    else:
        posts = SellPost.objects.filter(currency=section).order_by('price')
    result_html += render_to_string(
        template_name='p2p/posts_table.html',
        context={'section': 'sell', 'posts': posts, 'user': user}
    )
    return result_html


def get_buy_list_html(section: str, user: User) -> str:
    result_html = render_to_string(
        template_name='menu/currency_menu.html',
        context={'section': section, 'p2p_section': 'buy', 'currencies': CURRENCIES}
    )
    if section == 'all':
        posts = BuyPost.objects.order_by('-price').exclude(limit=0)
    else:
        posts = BuyPost.objects.filter(currency=section).order_by('-price').exclude(limit=0)
    result_html += render_to_string(
        template_name='p2p/posts_table.html',
        context={'section': 'buy', 'posts': posts, 'user': user}
    )
    return result_html


def get_user_posts_list_html(user: User, section: str) -> str:
    if section == 'buy':
        posts = user.buy_posts.all()
    else:
        posts = user.sell_posts.all()
    result_html = menu.get_posts_menu(section)
    result_html += render_to_string(
        template_name='p2p/user_posts_table.html', context={'section': section, 'posts': posts}
    )
    return result_html


def get_buy_post_html(user: User, post_id: int) -> str:
    post = BuyPost.objects.get(pk=post_id)
    info = get_post_info(post)
    user_limit = getattr(user, post.currency)
    actions = get_post_actions(post, user_limit=user_limit)
    result_html = html.get_post_html('Ордер на продажу', info, actions)
    result_html += html.get_messages_html(section='buy', post_id=post_id, new=True)
    result_html += modal.get_card_number_html(bank=post.get_bank_display(),
                                              post_id=post.id,
                                              new=True)
    return result_html


def get_sell_post_html(post_id: int) -> str:
    post = SellPost.objects.get(pk=post_id)
    info = get_post_info(post)
    actions = get_post_actions(post)
    result_html = html.get_post_html('Ордер на покупку', info, actions)
    result_html += html.get_messages_html(section='sell', post_id=post_id, new=True)
    result_html += modal.get_pay_modal_html(
        bank=post.get_bank_display(),
        card_number=post.card_number,
        post_id=post.id,
        new=True
    )
    render_to_string('p2p/modal/pay.html', context={'post': post, 'new': True, 'order_sum': 0})
    return result_html


def get_my_post_html(section: str, post_id: int) -> str:
    post = ''
    if section == 'buy':
        post = BuyPost.objects.get(pk=post_id)
    elif section == 'sell':
        post = SellPost.objects.get(pk=post_id)
    info = {
        'Валюта': {
            'content': post.currency,
            'extra': ''}, 'Цена': {
            'content': post.price,
            'extra': 'id="order-price"'
        },
        'Лимит': {
            'content': post.limit,
            'extra': 'id="order-limit"'
        },
        'Банк': {
            'content': post.get_bank_display(),
            'extra': ''
        }
    }
    if section == 'sell':
        info['Номер карты'] = {
            'content': post.card_number,
            'extra': ''
        }
    actions = {
        "": {
            'type': 'button',
            'extra': f'''style="align-self:center;" onclick="deletePost('{section}', {post_id})"''',
            'class': f'red-btn{" disabled" if post.has_payed_orders else ""}',
            'content': "Удалить"
        }
    }
    return html.get_post_html('', info, actions, html.get_chats_html(post))


def get_new_order_html(order_id: int, user: User) -> str:
    order = NewOrder.objects.get(pk=order_id)
    should_pay = False
    approve = False
    modal_html = ''
    user_limit = None
    order.check_count(user_limit)
    if order.buyer == user:
        title = 'Ордер на покупку'
        if not order.payed:
            should_pay = True
        modal_html = modal.get_pay_modal_html(
            new=False,
            order_id=order_id,
            order_sum=order.sum,
            bank=order.post.get_bank_display(),
            card_number=order.card_number,
        )
    elif order.seller == user:
        title = 'Ордер на продажу'
        if order.change:
            modal_html = modal.get_card_number_html(
                new=False,
                order_id=order_id,
                order_sum=order.sum,
                bank=order.post.get_bank_display(),
            )
            user_limit = getattr(user, order.post.currency)
            order.check_count(user_limit)
        elif order.payed:
            approve = True
            modal_html = modal.get_approve_modal_html(
                bank=order.post.get_bank_display(),
                order_id=order_id,
                order_sum=order.sum,
                buyer=order.buyer.username
            )

    info = get_post_info(order.post)
    actions = get_post_actions(
        order.post,
        count=order.count,
        is_order=True,
        change=order.change,
        order_id=order_id,
        order_sum=order.sum,
        pay=should_pay,
        approve=approve,
        user_limit=user_limit
    )
    result_html = html.get_post_html(title, info, actions)
    result_html += html.get_messages_html(order_id=order_id, new=False)
    result_html += modal_html
    return result_html


def get_orders_list_html(user: User) -> str:
    result_html = ''

    waiting_user_approve_orders = user.new_sell_orders.filter(change=False, payed=True)
    result_html += html.get_orders_html(
        orders=waiting_user_approve_orders,
        user=user,
        title='Ожидают моего подтверждения',
        func="downloadContent('/api/get-new-order-info/{}')"
    )

    waiting_user_pay_orders = user.new_buy_orders.filter(change=False, payed=False)
    result_html += html.get_orders_html(
        orders=waiting_user_pay_orders,
        user=user,
        title='Ожидают моей оплаты',
        func="downloadContent('/api/get-new-order-info/{}')"
    )

    new_sell_orders = user.new_sell_orders.filter(change=True).exclude(sell_post__user=user)
    new_buy_orders = user.new_buy_orders.filter(change=True).exclude(buy_post__user=user)
    result_html += html.get_discussing_orders_html(
        new_sell_orders,
        new_buy_orders
    )

    waiting_other_approve_orders = user.new_buy_orders.filter(change=False, payed=True)
    result_html += html.get_orders_html(
        orders=waiting_other_approve_orders,
        user=user,
        title='Ожидают подтверждения продавца',
        func="downloadContent('/api/get-new-order-info/{}')"
    )

    waiting_other_pay_orders = user.new_sell_orders.filter(change=False, payed=False)
    result_html += html.get_orders_html(
        orders=waiting_other_pay_orders,
        user=user,
        title='Ожидают оплаты покупателя',
        func="downloadContent('/api/get-new-order-info/{}')"
    )

    sell_orders = user.sell_orders.all()
    buy_orders = user.buy_orders.all()
    result_html += html.get_closed_orders_html(
        sell_orders=sell_orders,
        buy_orders=buy_orders,
        user=user,
    )

    return result_html


def get_order_messages_html(order_id: int, user: User) -> str:
    order = NewOrder.objects.get(pk=order_id)
    messages = order.messages.all()
    result_html = ''
    sep_symbol = "\n"
    for message in messages:
        result_html += f'<div class="message '
        if message.from_user == user:
            result_html += 'message-from'
        else:
            result_html += 'message-to'
        result_html += f'">{"<br>".join(message.text.split(sep_symbol))}</div>'
    return result_html


def get_messages_interface_html(order_id: int) -> str:
    return html.get_messages_html(order_id=order_id, new=False)


def get_user_currency_count(user: User, currency: str) -> dict:
    return {'count': getattr(user, currency)}


def add_post(user: User, info: dict) -> bool:
    post = None
    user = User.objects.get(email=user.email)
    if info['type'] == 'buy':
        post = BuyPost(
            currency=info['currency'],
            limit=info['limit'],
            price=info['price'],
            bank=info['bank'],
            user=user
        )
    else:
        post = SellPost(
            currency=info['currency'],
            limit=info['limit'],
            price=info['price'],
            bank=info['bank'],
            user=user,
            card_number=info['cardNumber']
        )
        user.reserve_currency(info['currency'], int(info['limit']))
    post.save()
    return True


def create_order(user: User, info: dict) -> dict:
    print(info)
    try:
        if info['section'] == 'sell':
            post = SellPost.objects.get(pk=info['postId'])
            order = NewOrder.create(buyer=user, count=info['count'], post=post, payed=info['payed'],
                                    change=not info['payed'])
            if info['payed']:
                post.user.reserve_payed_currency(post.currency, info['count'])
                post.limit -= int(info['count'])
                post.save()
        elif info['section'] == 'buy':
            post = BuyPost.objects.get(pk=info['postId'])
            order = NewOrder.create(post=post, count=info['count'], seller=user, payed=info['payed'])
            if info["cardNumber"]:
                order.card_number = info['cardNumber']
                order.change = False
                user.reserve_currency(post.currency, int(info['count']))
        order.save()
        try:
            text = info["message"]
            message = Message(from_user=user, order=order, text=text)
            message.save()
        except KeyError:
            pass
    except KeyError:
        return {'success': False}
    except ValueError:
        return {'success': False}

    return {'success': True, 'id': order.id}


def add_message(user: User, order_id: int, text: str) -> dict:
    order = NewOrder.objects.get(pk=order_id)
    message = Message(from_user=user, order=order, text=text)
    message.save()
    return {'success': True}


def close_order(order_id: int) -> dict:
    order = NewOrder.objects.get(pk=order_id)
    closed_order = Order.create(order)
    closed_order.save()
    order.close_order()
    if order.post.limit <= 0:
        order.post.remove()
    order.delete()
    return {'success': True}


def change_order_count(order_id: int, count: int) -> dict:
    try:
        order = NewOrder.objects.get(pk=order_id)
        order.count = count
        order.save()
    except:
        return {'success': False}
    return {'success': True}


def pay_order(order_id: int) -> dict:
    try:
        order = NewOrder.objects.get(pk=order_id)
        order.pay()
        order.save()
    except:
        return {'success': False}
    return {'success': True}


def add_card_number(order_id: int, card_number: int) -> dict:
    try:
        order = NewOrder.objects.get(pk=order_id)
        order.card_number = card_number
        order.change = False
        order.seller.reserve_currency(order.post.currency, order.count)
        order.save()
    except:
        return {'success': False}
    return {'success': True}


def delete_post(post_id: int, section: str) -> dict:
    try:
        if section == 'buy':
            post = BuyPost.objects.get(pk=post_id)
        else:
            post = SellPost.objects.get(pk=post_id)

        post.remove()
    except:
        return {'success': False}
    return {'success': True}


def delete_order(order_id: int) -> dict:
    try:
        order = NewOrder.objects.get(pk=order_id)
        order.delete()
    except:
        return {'success': False}
    return {'success': True}
