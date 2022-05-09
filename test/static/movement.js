const img2 = document.getElementById("img2");
img2.addEventListener("error", myFunction(img2));

function myFunction(img2) {
        const text = document.createElement("div");
        text.className = "text";
        text.innerHTML = "Lavoro di semestre di Natalia Andaloro e Denis Beqiraj";
        text.id = "text";
        const parent = img2.parentNode;
        parent.insertBefore(text,img2);
        parent.removeChild(img2);
    }

const img1 = document.querySelector('#img1');
img1.addEventListener("error", function(){
    img1.src = "../static/logo.png";
})
const img3 = document.querySelector('#img3');
img3.addEventListener("error", function(){
    img3.src = "../static/supsi_bianca.jfif";
})
const img4 = document.querySelector('#img4');
img4.addEventListener("error", function(){
    img4.src = "../static/StartUpGarage.png";
})
const img5 = document.querySelector('#img5');
img5.addEventListener("error", function(){
    img5.src = "../static/logo.png";
});

function move(images, word){

    const box = document.querySelector("#box");
    setTimeout(function(){
        if(box.classList.contains('animate')){
            box.classList.remove('animate');
        }
    }, 200000);
    let img2 = document.querySelector("#img2");
    if(img2){
        img2.src=images[1];
    } else {
        const parent = document.querySelector("#back");
        img2 = document.createElement("img");
        img2.id = "img2";
        const text = document.querySelector("#text");
        parent.insertBefore(img2,text);
        parent.removeChild(text);
        img2.src=images[1];
        img2.width = "150";
        img2.height = "150";
    }
    img2.addEventListener("error", myFunction(img2));

    const img1 = document.querySelector('#img1');
    img1.src=images[0];
    const img3 = document.querySelector('#img3');
    img3.src=images[2];
    const img4 = document.querySelector('#img4');
    img4.src=images[3];
    const img5 = document.querySelector('#img5');
    img5.src=images[4];
    const words = document.querySelector('#word');
    words.textContent=word;
    box.classList.add('animate');

}