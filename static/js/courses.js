function connectCourses(){
    const socket = new WebSocket(`ws:${window.location.host}/ws/courses/get-courses`);
    socket.onclose = function() {setTimeout(connectCourses, 2000)};
    socket.onmessage = function(e){updateCourses(e.data)}
}
function updateCourses(data){
    data = JSON.parse(data);
    for (let element of data){
        for (let key in element){
        if (key == 'currency') continue;
            document.getElementById(`${element.currency}-${key}`).innerText = element[key];
        }
    }
}