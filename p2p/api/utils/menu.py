def get_posts_menu(section) -> str:
    if section == 'buy':
        classes = ('active', '')
    else:
        classes = ("", 'active')
    return """<div id="post-menu" class="top-menu">
    <div class="top-menu-btn {}" onclick="downloadContent('/p2p/api/get-posts-list/buy', false, null, true)"><span>Покупка
    </span></div><div class="top-menu-btn {}" onclick="downloadContent('/p2p/api/get-posts-list/sell', false, null, true)"">
    <span>Продажа</span></div></div>""".format(*classes)
