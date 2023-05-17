from p2p.models import Post, BuyPost


def get_post_info(post: Post) -> dict:
    info = {'Валюта': {
        'content': post.currency,
        'extra': ''}, 'Цена': {
        'content': post.price,
        'extra': 'id="order-price"'
    }, 'Лимит': {
        'content': post.limit,
        'extra': 'id="order-limit"'
    }}
    if isinstance(post, BuyPost):
        info['Банк продавца'] = {
            'content': post.get_bank_display(),
            'extra': ''
        }
    else:
        info['Банк покупателя'] = {
            'content': post.get_bank_display(),
            'extra': ''
        }
    return info


def get_post_actions(post: Post, count: int = 0, is_order: bool = False, change: bool = True, order_id: int = 0,
                     order_sum: float = 0, user_limit: int | None = None, pay: bool = False,
                     approve: bool = False) -> dict:
    actions = {}
    if user_limit is None:
        limit = post.limit
    else:
        limit = min(user_limit, post.limit)
    if not change:
        actions["Количество"] = {
            'type': 'span',
            'extra': 'id="order-count"',
            'content': count
        }
    else:
        arg = ''
        if is_order:
            arg = f'true, {count}'
        actions[f"Количество{'' if user_limit is None else f' ({user_limit} доступно)'}"] = {
            'type': 'input',
            'extra': f'type="number" min="1" max="{limit}" value="{count if count else " "}" \
                id="order-count" placeholder="0" oninput="calcSum({arg})"',
            'content': ""
        }
    actions["Сумма"] = {
        'type': 'span',
        'extra': 'id="order-sum"',
        'class': 'order-sum',
        'content': f"{order_sum}"
    }
    if change:
        if is_order:
            actions["  "] = {
                'type': 'button',
                'extra': f'id="change-count-btn" onclick="sendCount({order_id})"',
                'class': 'blue-btn disabled',
                'content': "Сохранить"
            }
            actions[" "] = {
                'type': 'button',
                'extra': f'onclick="abortOrder({order_id})"',
                'class': 'blue-btn',
                'content': "Отменить"
            }
        if isinstance(post, BuyPost):
            actions[""] = {
                'type': 'button',
                'extra': 'id="sell-btn" data-modal="pay-modal"',
                'class': f'red-btn action {"" if count else "disabled"}',
                'content': "Продать"
            }
        else:
            actions[""] = {
                'type': 'button',
                'extra': 'id="buy-btn" data-modal="pay-modal"',
                'class': f'red-btn action {"" if count else "disabled"}',
                'content': "Купить"
            }
    else:
        if pay:
            actions[""] = {
                'type': 'button',
                'extra': 'data-modal="pay-modal"',
                'class': f'red-btn',
                'content': "Оплатить"
            }
        if approve:
            actions[""] = {
                'type': 'button',
                'extra': 'data-modal="pay-modal"',
                'class': f'red-btn',
                'content': "Подтвердить"
            }
    return actions
