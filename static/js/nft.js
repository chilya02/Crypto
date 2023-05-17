async function sendNewNft(){
    let currency = document.querySelector('#new-nft-currency select').value;
    let price = document.querySelector('#new-nft-price input').value;
    let name = document.querySelector('#new-nft-name input').value;
    let collection = document.querySelector('#new-nft-collection select').value;
    let newCollection = document.querySelector('#new-nft-new-collection input').value;
    let info = {
        name: name,
        currency: currency,
        price: price,
        collection: collection,
    }
    if (collection == 'Create-new-collection'){
        info['new_collection'] = newCollection;
    }
    let file = document.getElementById('file-input').files[0];
    const xhr = new XMLHttpRequest(); // создаем объект XMLHttpRequest
    const formData = new FormData(); // создаем объект FormData для передачи файла
    formData.append('file', file); // добавляем файл в объект FormData
    formData.append('info', JSON.stringify(info))
    xhr.open('POST', '/nft/api/add-nft'); // указываем метод и URL сервера, куда будет отправлен файл
    xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
    xhr.onload = function() { // добавляем обработчик события
        let response = JSON.parse(xhr.response);
        console.log(response);
        console.log(response['success'])
        if (response['success']) window.location.replace('/nft/my-nft');
  }

    xhr.send(formData);
}

async function sendNftPost(nft_id){
    let currency = document.querySelector('#sell-nft-currency select').value;
    let price = document.querySelector('#sell-nft-price input').value;
    let data = {
        currency: currency,
        price: price,
        id: nft_id
    }
    let rawResponse = await fetch(
    '/nft/api/sell-nft',{
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(data),
      });
    let response = await rawResponse.json();
    if (response['success']) window.location.replace('/nft/my-nft')
}
async function buyNft(post_id){
    let data = {
        id: post_id
    }
    let rawResponse = await fetch(
    '/nft/api/buy-nft',{
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(data),
      });
    let response = await rawResponse.json();
    if (response['success']) window.location.replace('/nft/my-nft')
}
function checkCollection(value){
 let elBlock = document.querySelector(".new-post-info-row.moving");
    if (value == 'Create-new-collection'){
        if (elBlock.style.height === "0px") {
            elBlock.style.height = `${ elBlock.scrollHeight }px`;
            elBlock.style.overflow = 'visible';
        }
    }
    else{
        if (elBlock.style.height != "0px"){
            elBlock.style.height = `${ elBlock.scrollHeight }px`;
            window.getComputedStyle(elBlock, null).getPropertyValue("height");
            elBlock.style.height = "0";
            elBlock.style.overflow = 'hidden';
        };
    }
}
function checkNewNftSubmit(){
    let modal = document.getElementById('add-nft-modal');
    let elements = modal.querySelectorAll('input, select');
    let submit = true;
    for (let element of elements){
        let flag = false;
        if (element.value || element.parentElement.style.overflow == 'hidden') flag = true;
        submit = submit & flag;
    }
    let btn = document.getElementById('add-new-nft-btn');
    if (submit){
        btn.classList.remove('disabled');
    } else{
        btn.classList.add('disabled');
    }
}

async function loadCollections(){
    let rawResponse = await fetch('/nft/api/get-collections-list');
    let response = await rawResponse.json();
    let select = document.querySelector('#new-nft-collection select')
    let options = select.querySelectorAll('.collection-select-name')
    for (let option of options){
        option.remove()
    }
    for (let collection of response['collections']){
        let option = document.createElement('option');
        option.innerHTML = collection['name'];
        option.value = collection['id'];
        option.className = 'collection-select-name'
        select.append(option)
    }
}
function dragenter(e) {
  e.stopPropagation();
  e.preventDefault();
  console.log('123123');
}

function dragover(e) {
  e.stopPropagation();
  e.preventDefault();
}

function drop(e) {
  e.stopPropagation();
  e.preventDefault();

  let dt = e.dataTransfer;
  let files = dt.files;
   setTimeout(_ =>{}, 20)
  handleFiles(files);
}

function handleFiles(files) {
  for (var i = 0; i < files.length; i++) {
    var file = files[i];
    if (!file.type.startsWith('image/')){ continue }

    var img = document.createElement("img");
    img.classList.add("obj");
    img.file = file;
    img.style.width = '100%';
    img.style.objectFit = 'contain';
    img.style.height = '100%';
    let preview = document.getElementById('nft-preview');
    preview.style.display = 'block';
    document.getElementById('upload-container').style.display = 'none';
//    document.getElementById('upload-container').querySelector('input').value = file;
    preview.appendChild(img);

    var reader = new FileReader();
    reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
    reader.readAsDataURL(file);
  }
}