function connectCourses(){
    const socket = new WebSocket(`ws:${window.location.host}/ws/courses/get-courses`);
    socket.onclose = function() {setTimeout(connectCourses, 2000)};
    socket.onmessage = function(e){updateCourses(e.data)}
}
function updateCourses(data){
    data = JSON.parse(data);
    console.log(data)
    for (let element in data){
        for (let key in data[element]){
        console.log(`${element}-${key}`);
        if (key == 'USDT') continue;
        let domElement = document.getElementById(`${element}-${key}`)
        if (key == 'change'){
            if (data[element][key] >= 0){
                domElement.style.color = '#0ECB81';
            } else{
                domElement.style.color = '#F6465D';
            }
        }
            domElement.innerText = data[element][key];
        }
    }
}