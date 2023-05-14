function sendNewNft(){

}
function checkNewNftSubmit(){
    let modal = document.getElementById('add-nft-modal');
    let elements = modal.querySelectorAll('input, select');
    let submit = true;
    for (let element of elements){
        let flag = false;
        if (element.value || element.parentElement.style.overflow == 'hidden') flag = true;
        submit = submit & flag;
        console.log( element, flag)
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
        option.innerHTML = collection;
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
    document.getElementById('upload-container').querySelector('input').value = file;
    preview.appendChild(img); // Предполагается, что "preview" это div, в котором будет отображаться содержимое.

    var reader = new FileReader();
    reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
    reader.readAsDataURL(file);
  }
}