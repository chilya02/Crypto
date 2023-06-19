from p2p.models import Post
from django.template.loader import render_to_string


def get_chats_html(post: Post) -> str:
    orders = post.new_orders.all()
    return render_to_string(template_name='messages/chats.html', context={'orders': orders})


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
    return render_to_string(
        'messages/messages.html',
        context={
            'section': section,
            'post_id': post_id,
            'order_id': order_id,
            'hidden': hidden,
            'new': new,
        }
    )
