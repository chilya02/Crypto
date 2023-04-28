from .rows import get_discussing_order_row, get_new_order_row, get_order_row
from authentication.models import User
from p2p.models import Post


def get_discussing_orders_html(new_sell_orders, new_buy_orders) -> str:
    html = ''
    headers = [
        {
            'class': 'la',
            'text': 'Клиент/валюта'
        },
        {
            'class': '',
            'text': 'Цена'
        },
        {
            'class': '',
            'text': 'Лимит'
        },
        {
            'class': 'la',
            'text': 'Банк'
        },
        {
            'class': 'la',
            'text': 'Тип операции'
        },
    ]
    rows = []
    for order in new_sell_orders:
        rows.append(get_discussing_order_row(order))
    for order in new_buy_orders:
        rows.append(get_discussing_order_row(order))
    if rows:
        html += '<h1>На обсуждении</h1>'
        html += get_table_html(headers=headers, rows=rows)
    return html


def get_orders_html(orders, user: User, title: str, func: str) -> str:
    html = ''
    headers = [
        {
            'class': 'la',
            'text': 'Клиент/валюта'
        },
        {
            'class': '',
            'text': 'Цена'
        },
        {
            'class': '',
            'text': 'Количество'
        },
        {
            'class': '',
            'text': 'Сумма'
        },
    ]
    rows = []
    for order in orders:
        rows.append(get_new_order_row(order=order, user=user, func=func))
    if rows:
        html += f'<h1>{title}</h1>'
        html += get_table_html(headers=headers, rows=rows)
    return html


def get_closed_orders_html(sell_orders, buy_orders, user: User) -> str:
    html = ''
    headers = [
        {
            'class': 'la',
            'text': 'Клиент/валюта'
        },
        {
            'class': '',
            'text': 'Цена'
        },
        {
            'class': '',
            'text': 'Количество'
        },
        {
            'class': '',
            'text': 'Сумма'
        },
        {
            'class': 'la',
            'text': 'Тип операции'
        },
    ]
    rows = []
    for order in sell_orders:
        rows.append(get_order_row(order, user))
    for order in buy_orders:
        rows.append(get_order_row(order, user))
    if rows:
        html += '<h1>Закрытые ордера</h1>'
        html += get_table_html(headers=headers, rows=rows)
    return html


def get_table_html(headers: list, rows: list) -> str:
    table_html = '<table><tr class="title">'
    for header in headers:
        table_html += f'<th class="{header["class"]}">{header["text"]}</th>'
    table_html += '</tr>'
    for row in rows:
        table_html += f"""<tr class="table-row" onclick="{row['arg']}">"""
        for data in row['items']:
            table_html += f'<td class="{data["class"]}">{data["text"]}</td>'
        table_html += '</tr>'
    table_html += '</table>'
    return table_html


def get_chats_html(post: Post) -> str:
    html = """<div class="message-interface-box">
        <div class="message-box-interface-title"><span>Чаты</span></div>
        <div class="message-box-interface-body"> <div class="message-box-content">"""
    html += '<table id="chats">'
    orders = post.new_orders.all()
    for order in orders:
        html += f"""<tr class="table-row" onclick="openDialog(this, {order.id})">"""
        html += f'<td class="la"><div class="with-info"><span>{order.client.username}</span><span class="info">{order.count} {order.post.currency}{" (оплачен)" if order.payed else ""}</span></div></td>'
        html += '</tr>'
    html += '</table>'
    html += '</div></div></div>'
    return html


def get_post_info_html(info: dict) -> str:
    html = '<div id="post-info-data">'
    for key, value in info.items():
        html += '<div class="post-info-row">'
        html += f'<span class="info-name">{key}</span>'
        html += f'<span class="info-text" {value["extra"]}>{value["content"]}</span>'
        html += '</div>'
    return html


def get_post_actions_html(actions: dict, extra: str | None) -> str:
    html = '</div> <div id="post-info-actions">'
    if extra:
        html += '<div class="post-info-row">'
        html += extra
        html += '</div>'
    for key, value in actions.items():
        html += '<div class="post-info-row">'
        html += f'<span class="info-name">{key}</span>'
        html += f'<{value["type"]} class="info-text {value["class"] if "class" in value else ""}" {value["extra"]}>{value["content"]}</{value["type"]}>'
        html += '</div>'
    html += '</div>'
    return html


def get_post_html(title: str, info: dict, actions: dict, extra: str | None = None) -> str:
    html = f'<h1>{title}</h1>' if title else ''
    html += '<div id="post-info">'
    html += get_post_info_html(info)
    html += get_post_actions_html(actions, extra)
    html += '<div class="placeholder"></div></div>'
    return html


def get_messages_html(section: str = "", post_id: int = 0, order_id: int = 0, hidden: bool = False,
                      new: bool = True) -> str:
    return f"""
    <div id="message-box" class="message-interface-box closed {"hidden" if hidden else ""} ">
    <div id="message-box-title" onclick="messagesView({'false' if new else f'true, {order_id}'})" 
    class="message-box-interface-title closed"><span>Сообщения</span></div>
    <div id="message-box-body" class="message-box-interface-body closed">
    <div id="messages" class="message-box-content"></div><div id="message-input-area">
    <textarea id="new-message-field" oninput="checkMessage()"></textarea>
    <svg class="disabled" style="cursor:pointer;" onclick="{f"createOrder('{section}', {post_id}, true)" if new else f"sendMessage({order_id})"}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20">
    <g id="_01_align_center" data-name="01 align center">
    <path d="M1.444,6.669a2,2,0,0,0-.865,3.337l3.412,3.408V20h6.593l3.435,3.43a1.987,1.987,0,0,0,1.408.588,2.034,2.034,0,0,0,.51-.066,1.978,1.978,0,0,0,1.42-1.379L23.991.021ZM2,8.592l17.028-5.02L5.993,16.586v-4Zm13.44,13.424L11.413,18h-4L20.446,4.978Z"/>
    </g></svg></div></div></div>"""
