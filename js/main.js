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
    var split_word=event.data.split(",")
    if(split_word.length != 1){
        console.log(split_word);
        move(split_word[0])
    }
});
