(function(){

var vel = 50;
var moveEl = function(){
var el = document.querySelector("#box");
var left = el.offsetLeft;
var movement = 3;

el.style.left = left + movement + "px";

if(left > 500){
clearInterval(interval);
}
}

var interval = setInterval(moveEl, vel);
}());