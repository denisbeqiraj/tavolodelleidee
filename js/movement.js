(function(){

var vel = 50; //millisecondi
var start = performance.now(); //momento di partenza
var duration = 5000 //durata animazione
var el = document.querySelector("#box");
var left = el.offsetLeft;
var top = el.offsetTop;
var movement = 6;
/*
function moveEl(){
    var timePassed = performance.now() - start; //tempo passato dal momento di partenza

    animation1(timePassed);

    if(timePassed >= duration){ //l'animazione finisce dopo duration
        clearInterval(interval);
    }
}

var growth = 0;

function animation1(time){
    var dim = 150;
    if(growth + time/duration < dim) { //Quando l'immagine raggiunge una certa dimensione smette di crescere
        el.style.height = growth + time/duration + "px";
        el.style.width = growth + time/duration + "px";
        growth++;
    }
    el.style.transform = "rotate("+ time/movement +"deg)";
}

var interval = setInterval(moveEl, vel); // cambia posizione ogni vel
*/
var veloc = 50;
var vel_angolare = 1;

function animation2(time){
    el.style.transform = "rotate("+ 0 +"deg)"; //posiziona l'immagine dritta dopo la rotazione
    //va cambiato perchè bisogna farlo ruotare mentre gira nello schermo
    //console.log(left);
    time = time/1000;
    el.style.left = (veloc*time)*Math.sin(vel_angolare*time) + "px"; //x da 0 a 3 secondi, il cubo si sposta da 0 a 1000 px
    el.style.top = (veloc*time)*Math.cos(vel_angolare*time) + "px"; //y
}

//var interval = setInterval(moveEl, vel); // cambia posizione ogni vel

var duration2 = 15000;
var vel2 = 2;
function moveEl2(){
    var timePassed2 = performance.now() - start; //tempo passato dal momento di partenza

    animation2(timePassed2);

    if(timePassed2 >= duration2){ //l'animazione finisce dopo duration
        clearInterval(interval2);
    }
}

start = performance.now();
var interval2 = setInterval(moveEl2, vel2);
}());