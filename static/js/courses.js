function connectCourses(){
    const socket = new WebSocket(`ws:${window.location.host}/ws/courses/get-courses`);
    socket.onclose = connectCourses;
    socket.onmessage = function(e){updateCourses(e.data)}
}
function updateCourses(data){
    console.log(data);
}