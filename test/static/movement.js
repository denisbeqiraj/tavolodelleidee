function move(images, word){

    const img2 = document.querySelector('#img2');
    img2.addEventListener("error", myFunction());

    function myFunction() {
        var text = document.createElement("div");
        text.className = "text";
        text.innerHTML = "Lavoro di semestre di Natalia Andaloro e Denis Beqiraj";
        var parent = img2.parentNode;
        parent.insertBefore(text,img2);
        parent.removeChild(img2);
    }
    const img1 = document.querySelector('#img1');
    img1.src=images[0];
    img2.src=images[1];
    const img3 = document.querySelector('#img3');
    img3.src=images[2];
    const img4 = document.querySelector('#img4');
    img4.src=images[3];
    const img5 = document.querySelector('#img5');
    img5.src=images[4];
    const words = document.querySelector('#word');
    words.textContent=word;

};