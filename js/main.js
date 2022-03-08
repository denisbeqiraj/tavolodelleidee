// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:8765');
var API_KEY = '26044387-30ea27ccb218f7f03d57137ae';
var url = "https://pixabay.com/api/?key="+API_KEY+"&q="+encodeURIComponent('red roses');
var elementimage = document.querySelector("#box");
// Connection opened
socket.addEventListener('open', function (event) {
    socket.send('Start');
});

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
    socket.send('Received');
    elementimage.insertAdjacentHTML('beforeend', '<div id="two">two</div>');
    fetch(url)
        .then(response => {
            return response.json();
        }).then(data => {
            console.log(data["hits"][0]["largeImageURL"]);
        })
        .catch(error => {
            // handle the error
    });
});
