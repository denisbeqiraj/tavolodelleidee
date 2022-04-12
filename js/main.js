// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:8765');
var API_KEY = '26044387-30ea27ccb218f7f03d57137ae';
var elementimage = document.querySelector("#box");
// Connection opened
socket.addEventListener('open', function (event) {
    socket.send('Start');
});

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
    socket.send('Received');
    const split_word=JSON.parse(event.data);
    console.log(split_word["all_data"]);
    if(split_word["all_data"]["link"].length>0){
        move(split_word["all_data"]["link"][0]);
    }
});
