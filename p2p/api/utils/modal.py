def p2p_modal_interface(function) -> str:
    def _wrapper(*args, order_id: int = 0, **kwargs):
        html = f'''<div class="dlg-modal dlg-modal-fade first-open" id="pay-modal">
        <span class="closer" data-close=""></span>'''
        html += function(*args, order_id=order_id, **kwargs)
        html += '</div>'
        return html

    return _wrapper


@p2p_modal_interface
def get_pay_modal_html(bank: str, card_number: int, order_id: int = 0, order_sum: float = 0, new: bool = False,
                       post_id: int = 0) -> str:
    if new:
        arg = f"createOrder('sell', {post_id}, false, true)"
    else:
        arg = f'payOrder({order_id})'
    return f'''
    <h1>Оплата ордера</h1>
    <div id="pay-info" class="modal-info"><div class="order-info-row"><span class="info-name">Сумма</span>
    <span class="info-text order-sum"">{order_sum}</span></div><div class="order-info-row">
    <span class="info-name">Банк</span><span class="info-text">{bank}</span></div>
    <div class="order-info-row"><span class="info-name">Номер карты</span>
    <span class="info-text">{card_number}</span></div><div class="order-info-row">
    <button id="pay-btn" class="red-btn" data-close="" onclick="{arg}">Я оплатил</button></div></div>
'''


@p2p_modal_interface
def get_card_number_html(bank: str, order_id: int = 0, order_sum: float = 0, new: bool = False,
                         post_id: int = 0) -> str:
    if new:
        arg = f"createOrder('buy', {post_id}, false, false)"
    else:
        arg = f'sendCardNumber({order_id})'
    return f'''
    <h1>Оплата ордера</h1>
    <div id="pay-info" class="modal-info"><div class="order-info-row"><span class="info-name">Сумма</span>
    <span class="info-text order-sum">{order_sum}</span></div><div class="order-info-row">
    <span class="info-name">Банк</span><span class="info-text">{bank}</span></div>
    <div class="order-info-row"><span class="info-name">Номер карты</span>
    <input class="info-text card-number" type="number" id="order-card-number" min="0" max="Infinity" oninput="checkElement('#save-btn', this)">
    </div><div class="order-info-row">
    <button id="save-btn" class="red-btn disabled" data-close="" onclick="{arg}">Сохранить</button></div></div>'''


@p2p_modal_interface
def get_approve_modal_html(bank: str, buyer: str, order_id: int = 0, order_sum: float = 0) -> str:

    return f'''
    <h1>Оплата ордера</h1>
    <div id="pay-info" class="modal-info"><div class="order-info-row"><span class="info-name">Сумма</span>
    <span class="info-text order-sum">{order_sum}</span></div><div class="order-info-row">
    <span class="info-name">Банк</span><span class="info-text">{bank}</span></div>
    <div class="order-info-row"><span class="info-name">Покупатель</span>
    <span class="info-text">{buyer}</span></div>
    </div><div class="order-info-row">
    <button id="approve-btn" class="red-btn" style="font-size:30px;" data-close="" onclick="closeOrder({order_id})">Подтвердить</button></div></div>'''
