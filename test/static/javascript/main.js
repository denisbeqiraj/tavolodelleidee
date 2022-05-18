var socket = io();
//Connessione websocket
socket.on('connect', function() {
    socket.emit('tavolodelleidee', {data: 'I\'m connected!'});
});
//Setup ogni richiesta
socket.on('response', function(msg) {
//parso il json in input
    const split_word=JSON.parse(msg);
    //console.log(split_word["all_data"]);
    //Se ci sono parole aggiungo
    if(split_word["all_data"]["link"].length>0){
        move(split_word["all_data"]["link"], split_word["all_data"]["word"][0]);
    }
});