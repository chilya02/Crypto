def get_posts_menu(section) -> str:
    if section == 'buy':
        classes = ('active', '')
    else:
        classes = ("", 'active')
    return """<div id="post-menu" class="top-menu">
    <div class="top-menu-btn {}" onclick="downloadContent('/api/get-posts-list/buy', false, null, true)"><span>Покупка
    </span></div><div class="top-menu-btn {}" onclick="downloadContent('/api/get-posts-list/sell', false, null, true)"">
    <span>Продажа</span></div></div>""".format(*classes)


def get_cur_menu(p2p_section: str, section: str) -> str:
    """Создает HTML меню выбора валют"""

    url = f"get-{p2p_section}-list"

    cur_menu = f"""<div id="cur-menu" class="top-menu">
    <div class="top-menu-btn {"active" if section == 'all' else ""}" onclick="downloadContent('/api/{url}/all')">
    <span>Все</span>
    </div>"""

    for cur in ('USDT', 'BTC', 'ETH', 'KPFU', 'SOL'):
        cur_menu += f"""<div class="top-menu-btn {"active" if cur == section else ""}" 
        onclick="downloadContent('/api/{url}/{cur}', false, null, true)">
        <span>{cur}</span></div>"""

    cur_menu += "</div>"
    return cur_menu
