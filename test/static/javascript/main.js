var socket = io();
socket.on('connect', function() {
    socket.emit('tavolodelleidee', {data: 'I\'m connected!'});
});
socket.on('response', function(msg) {
    const split_word=JSON.parse(msg);
    console.log(split_word["all_data"]);
    if(split_word["all_data"]["link"].length>0){
        move(split_word["all_data"]["link"], split_word["all_data"]["word"][0]);
    }
});