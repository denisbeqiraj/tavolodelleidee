// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:8765');

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
});