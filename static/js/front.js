function selectP2PSection(section){
    let elements = document.querySelectorAll('.p2p-menu-row, #p2p-nav a')
    for (let element of elements){
        if (element.id == `p2p-${section}-button` | element.id == `mobile-p2p-${section}-button`){
            element.classList.add('active')
        }
        else{
            element.classList.remove('active')
        }
    } 
}

function handleMessage(message, url, is_back=false, func=null, replace=false){
    if (message['redirect']){
        window.location.replace(message['redirect'])
    }
    if (!is_back){
        if (func) func = func.name
        let state = window.history.state;
        let scrollY = window.scrollY;
        if (state){
            window.history.replaceState({href: state['href'], func: state['func'], scrollY: scrollY}, '', state.url);
        }
        if (replace && state != null){
            window.history.replaceState({href: url, func: func, scrollY: scrollY}, "EVILEG", message['url']);
        } else{
            if (state == null || state['href'] != url){
                window.history.pushState({href: url, func: func, scrollY: 0}, "EVILEG", message['url']);
            }
        }
    }

    let parent;
    switch (message['section']){
        case 'p2p':
            selectP2PSection(message['p2p_section']);
            parent = document.querySelector('#p2p-content');
            break;
        case 'courses':
            parent = document.querySelector('#main')
            break;
    }
    parent.innerHTML = message['html'];
    if (message['section'] == 'p2p') addModalListeners();
}

async function downloadContent(url, is_back=false, func=null, replace=false, close_menu=true){
        let rawResponse = await fetch(url);
        let response = await rawResponse.json();
        console.log(close_menu)
        if (close_menu){
          let toggle = document.getElementById('toggle');
          toggle.checked = false;
        }
        for (let el of ['#nft-menu-btn', '#p2p-menu-btn']){
         closeMenu(document.querySelector(el)); 
        }
        handleMessage(response, url, is_back, func, replace);
        if (func) func()
}

window.addEventListener ("popstate", async function (e){
    if (e.state){
        await downloadContent(e.state['href'], true, window.eval(e.state['func']));
        window.scrollTo(0, e.state['scrollY']);
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}


async function downloadP2p(section, currency){
    await downloadContent('/p2p/api/get-p2p-interface');
    downloadContent(`/p2p/api/get-${section}-list/${currency}`, false, null, true)
}

async function getBalance(){
    let rawResponse = await fetch('/api/get-balance');
    let response = await rawResponse.json();
    balance = document.getElementById("header-balance");
    if (balance) {
        if (response['balance']){
            balance.querySelector("span").innerHTML = response['balance']
        }
    }
}


function disableElement(element){
    element.value = ""
    element.classList.add("disabled");
    element.dispatchEvent(new Event('input'));
}

function checkElement(selector, element, point=false){
    setTimeout(_ =>{
        if (element.type == 'number') checkValue(element, point)
        target = document.querySelector(selector);
        if (element.value && element.value > '0') target.classList.remove('disabled')
        else disableElement(target)
    }, 20)
}


function menuView(el){
    if (document.documentElement.clientWidth >= 1200){
        window.location.replace(el.dataset.link)
    }
    let elBlock = document.querySelector(el.dataset.submenu);
    if (elBlock.style.height != "0px"){
        closeMenu(el);
    } else{
       showMenu(el)
    }
}
function showMenu(el){
    el.classList.replace('closed', 'opened');
    let elBlock = document.querySelector(el.dataset.submenu);
    elBlock.style.height = `${ elBlock.scrollHeight }px`;
}
function closeMenu(el){
    el.classList.replace('opened', 'closed');
    let elBlock = document.querySelector(el.dataset.submenu);
    elBlock.style.height = `${ elBlock.scrollHeight }px`;
    window.getComputedStyle(elBlock, null).getPropertyValue("height");
    elBlock.style.height = "0";
}

function mainMenuChange(){
    let toggle = document.getElementById('toggle');
    console.log('menu operation'); 
    switch (toggle.checked){
        case true:
            el = document.querySelector("#main-nav .active[data-submenu]");
            if (el){
                showMenu(el);
            }
            break;
        case false:
            for (let el of document.querySelectorAll('[data-submenu]')){
                closeMenu(el);
            }
    }
}