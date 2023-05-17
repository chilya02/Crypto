from p2p.models import Post
from django.template.loader import render_to_string


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
    return render_to_string(template_name='p2p/chats.html', context={'orders': orders})


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
