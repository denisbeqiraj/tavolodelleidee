const firstBox = document.querySelector("#firstBox");
firstBox.addEventListener("animationend", deleteBox);

function deleteBox(){
    this.remove();
}

function move(images, word){

    const parent = document.querySelector(".scene");

    const newBox = document.createElement("div");
    newBox.className = "box animate";

    const front = document.createElement("div");
    front.className = "box__face box__face--front text";
    const wordNode = document.createTextNode(word);
    front.appendChild(wordNode);

    newBox.appendChild(front);

    const back = document.createElement("div");
    back.className = "box__face box__face--back";
    const img0 = document.createElement("img");
    img0.src=images[0];
    img0.width = "150";
    img0.height = "150";
    img0.addEventListener("error", function() {
        const text = document.createElement("div");
        text.className = "text";
        text.innerHTML = "Lavoro di semestre di Natalia Andaloro e Denis Beqiraj";
        text.id = "text";
        const parent = this.parentNode;
        parent.insertBefore(text,this);
        parent.removeChild(this);
    });
    back.appendChild(img0);

    newBox.appendChild(back);

    const right = document.createElement("div");
    right.className = "box__face box__face--right";
    const img1 = document.createElement("img");
    img1.src=images[1];
    img1.width = "150";
    img1.height = "150";
    img1.addEventListener("error", function(){
        img1.src = "../static/supsi_bianca.jfif";
    });
    right.appendChild(img1);

    newBox.appendChild(right);

    const left = document.createElement("div");
    left.className = "box__face box__face--left";
    const img2 = document.createElement("img");
    img2.src=images[2];
    img2.width = "150";
    img2.height = "150";
    img2.addEventListener("error", function(){
        img2.src = "../static/StartUpGarage.png";
    });
    left.appendChild(img2);

    newBox.appendChild(left);

    const top = document.createElement("div");
    top.className = "box__face box__face--top";
    const img3 = document.createElement("img");
    img3.src=images[3];
    img3.width = "150";
    img3.height = "150";
    img3.addEventListener("error", function(){
        img3.src = "../static/logo.png";
    });
    top.appendChild(img3);

    newBox.appendChild(top);

    const bottom = document.createElement("div");
    bottom.className = "box__face box__face--bottom";
    const img4 = document.createElement("img");
    img4.src=images[4];
    img4.width = "150";
    img4.height = "150";
    img4.addEventListener("error", function(){
        img4.src = "../static/logo.png";
    });
    bottom.appendChild(img4);

    newBox.appendChild(bottom);

    newBox.addEventListener("animationend", deleteBox);
    const end = document.querySelector(".end");
    parent.insertBefore(newBox,end);
}