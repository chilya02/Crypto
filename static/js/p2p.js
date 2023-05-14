function calcSum(update=false, oldCount=0){
    let count = document.getElementById('order-count');
    if (!checkValue(count)){
        document.getElementById('post-info-actions').querySelector('.action').classList.add('disabled');
        if (update){
            document.getElementById('change-count-btn').classList.add('disabled');
        }
    } else{
        document.getElementById('post-info-actions').querySelector('.action').classList.remove('disabled');
        if (update){
            if (count.value == oldCount){
                document.getElementById('change-count-btn').classList.add('disabled');
            }
            else{
                document.getElementById('change-count-btn').classList.remove('disabled');
                document.getElementById('post-info-actions').querySelector('.action').classList.add('disabled');
            }
        }
        if (update & oldCount == 0){
            document.getElementById('post-info-actions').querySelector('.action').classList.add('disabled');
        }
    }
    let sums = document.querySelectorAll('.order-sum');
    let price = document.getElementById('order-price');
    for (let el of sums){
        el.textContent = Math.round(Number(count.value) * Number(price.textContent)*100)/100;
    }

};

async function sendCount(id){
    let count = document.getElementById('order-count');
    count.setAttribute('oninput', `calcSum(true, ${count.value})`);
    calcSum(true, count.value);
    let body = {
        count: count.value
    }
    let rawResponse = await fetch(
        `/p2p/api/change-order-count/${id}`,{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(body)
          });
    let response = await rawResponse.json();
}



function checkValue(target, point=false){
    if (target.value == ''){
        return false;
    }
    let result = target.value
    if (target.max == "Infinity") {
        if (!point)
        target.value = Math.round(Number(result));
        else 
        target.value = Math.round(Number(result * 100)) / 100;
        return true;
    }
    if (Number(target.value) < 1) result = 1;
    if (Number(target.value) > Number(target.max)) result = target.max;
    if (Number(target.max) == 0) {
        target.value = '';
        return false;
    }
    if (!point)
    target.value = Math.round(Number(result));
    else 
    target.value = Math.round(Number(result * 100)) / 100;
    return true;
};

async function getLimit(){
    let buy = false;
    let limitBlock = document.getElementById('new-post-limit');
    let limit = limitBlock.querySelector('input');
    let currency = document.querySelector('#new-post-currency select').value;
    if (!currency) return
    let text = 'Лимит';
    if (document.getElementById('new-post-buy').classList.contains('active')) buy = true;
    if (buy){
        limit.max=Infinity;
        if (currency) limit.classList.remove('disabled')
        else limit.classList.add('disabled')
    } else{
        let rawResponse = await fetch(`/p2p/api/get-currency-count/${currency}`);
        let response = await rawResponse.json();
        let count = response['count']
        if (count) limit.classList.remove('disabled');
        else disableElement(limit)
        limit.max = count;
        if (Number(limit.value) > count) limit.value = count;
        text = `Лимит (${count} доступно)`;
    }
    limitBlock.querySelector('span').textContent = text;
}

function addListeners(element){
    element.addEventListener('input', checkValue);
    element.onblur = function (){
        element.removeEventListener('input', checkValue);
    }
}

function messagesView(load=false, id=null){
    let messageBoxBody = document.getElementById("message-box-body");
    if (messageBoxBody.classList.contains("closed")){
        openMessages(load, id)
    } else{
        closeMessages()
    }
};

function openMessages(load=false, id=null){
    if (load) loadMessages(id)
    let messageBoxBody = document.getElementById("message-box-body");
    let messageBoxTitle = document.getElementById("message-box-title");
    let messageBox = document.getElementById("message-box");
    messageBoxBody.classList.replace("closed", "opened")
    messageBoxTitle.classList.replace("closed", "opened")
    messageBox.classList.replace("closed", "opened")
}

function closeMessages(){
    let messageBoxBody = document.getElementById("message-box-body");
    let messageBoxTitle = document.getElementById("message-box-title");
    let messageBox = document.getElementById("message-box");
    messageBoxBody.classList.replace("opened", "closed")
    messageBoxTitle.classList.replace("opened", "closed")
    messageBox.classList.replace("opened", "closed")
}

function newPostBuy(){
    let elBlock = document.querySelector(".new-post-info-row.moving");
        if (elBlock.style.height != "0px"){
        elBlock.style.height = `${ elBlock.scrollHeight }px`;
        window.getComputedStyle(elBlock, null).getPropertyValue("height");
        elBlock.style.height = "0";
        elBlock.style.overflow = 'hidden';
    };
    document.getElementById('new-post-buy').classList.add('active');
    document.getElementById('new-post-sell').classList.remove('active');
    getLimit()
}

function newPostSell(){
    let elBlock = document.querySelector(".new-post-info-row.moving");
    if (elBlock.style.height === "0px") {
        elBlock.style.height = `${ elBlock.scrollHeight }px`;
        elBlock.style.overflow = 'visible';
    }
    document.getElementById('new-post-sell').classList.add('active');
    document.getElementById('new-post-buy').classList.remove('active');
    getLimit()
}

function showMessages(){
    document.getElementById('message-box').classList.remove('hidden');
    setTimeout(openMessages, 2)
}

function hideMessages(){
    closeMessages()
    setTimeout(function(){}, 100)
    document.getElementById('message-box').classList.add('hidden')
}

function checkSubmit(){
    let modal = document.getElementById('add-post-modal');
    let elements = modal.querySelectorAll('input, select');
    let submit = true;
    for (let element of elements){
        let flag = false;
        if (element.value || element.parentElement.style.overflow == 'hidden') flag = true;
        submit = submit & flag;
    }
    let btn = document.getElementById('add-new-post-btn');
    if (submit){
        btn.classList.remove('disabled');
    } else{
        btn.classList.add('disabled');
    }
}

async function sendPost(){
    let type = document.getElementById('new-post-buy').classList.contains('active') ? 'buy': 'sell';
    let currency = document.querySelector('#new-post-currency select').value;
    let price = document.querySelector('#new-post-price input').value;
    let limit = document.querySelector('#new-post-limit input').value;
    let bank = document.querySelector('#new-post-bank select').value;
    let cardNumber = document.querySelector('#new-post-card-number input').value;
    let info = {
        type: type,
        currency: currency,
        price: price,
        limit: limit,
        bank: bank,
    }
    if (type == 'sell'){
        info['cardNumber'] = cardNumber;
    }
    let rawResponse = await fetch(
        '/p2p/api/add-post',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(info)
          });
    let response = await rawResponse.json();
    if (response['success']) window.location.replace('/p2p/my-posts')
}


function checkMessage(){
    let field = document.getElementById("new-message-field");
    if (field.value){
        document.querySelector("#message-input-area svg").classList.remove('disabled');
    } else{
        document.querySelector("#message-input-area svg").classList.add('disabled');
    }
}

async function sendMessage(orderId){
    let field = document.getElementById('new-message-field')
    let message = field.value;
    field.value = '';
    checkMessage();
    let rawResponse = await fetch(
        '/p2p/api/send-message',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({message: message, id:orderId})
          });
    let response = await rawResponse.json();
    if (response['success']) loadMessages(orderId);
}

async function createOrder(section, postId, with_message=false, payed=false){
    let count = document.getElementById('order-count').value;
    if (!count) count = 0;
    let body = {
        section: section,
        postId: postId,
        payed: payed,
        count: count,
        cardNumber: null,
    }
    if (with_message){
        let message = document.getElementById('new-message-field').value;
        body["message"] = message;
        body["payed"] = false;
        body["cardNumber"] = null;
    } else{
        if (section == 'buy'){
            let formCardNumber = document.getElementById('order-card-number').value;
            body["cardNumber"] = formCardNumber;
        }
    }
    let rawResponse = await fetch(
        '/p2p/api/create-order',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(body)
          });
    let response = await rawResponse.json();
    if (response["success"])
    await downloadContent(`/p2p/api/get-new-order-info/${response["id"]}`)
    if (with_message) openMessages(true, response['id']);
}

async function loadMessages(orderId){
    let rawResponse = await fetch(`/p2p/api/get-messages/${orderId}`);
    let response = await rawResponse.json();
    let messages = document.getElementById('messages')
    messages.innerHTML = response['html'];
    messages.scrollTo(0, messages.scrollHeight);
}

async function openDialog(target, orderId){
    let messageBox = document.getElementById('message-box');
    let parentElement = document.getElementById('p2p-content');
    if (messageBox){
        closeMessages()
        parentElement.removeChild(messageBox);

        
    }
    let chats = document.querySelectorAll('#chats tbody tr');
    for (let chat of chats){
        chat.classList.remove('active')
    }
    target.classList.add('active')
    let rawResponse = await fetch(`/p2p/api/get-messages-interface/${orderId}`);
    let response = await rawResponse.json();
    parentElement.innerHTML += response['html']
    setTimeout(_ =>{
        openMessages(true, response['id'])
    }, 5)
    
}

async function payOrder(orderId){
    let body = {id: orderId}
    let rawResponse = await fetch(
        '/p2p/api/pay-order',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(body)
          });
    let response = await rawResponse.json();
    if (response['success']) downloadContent(`/p2p/api/get-new-order-info/${orderId}`)
}

async function sendCardNumber(orderId){
    let formCardNumber = document.getElementById('order-card-number').value;
    let body = {id: orderId, cardNumber: formCardNumber}
    let rawResponse = await fetch(
        '/p2p/api/add-card-number',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(body)
          });
    let response = await rawResponse.json();
    if (response['success']) downloadContent(`/p2p/api/get-new-order-info/${orderId}`)
}

async function deletePost(section, postId){
    body = {
        section: section,
        id: postId
    }
    let rawResponse = await fetch(
        '/p2p/api/delete-post',{
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(body)
          });
    let response = await rawResponse.json();
    if (response['success']) downloadContent(`/p2p/api/get-posts-list/sell`);
}

async function abortOrder(orderId){
    body = {
        id: orderId
    }
    let rawResponse = await fetch(
        '/p2p/api/abort-order',{
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(body)
          });
    let response = await rawResponse.json();
    if (response['success']) downloadContent(`/p2p/api/get-orders-list`)
}

async function closeOrder(orderId){
    body = {id: orderId}
    let rawResponse = await fetch(
        '/p2p/api/close-order',{
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(body)
          });
    let response = await rawResponse.json();
    if (response['success']) downloadContent(`/p2p/api/get-orders-list`)
}