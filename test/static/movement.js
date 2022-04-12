function move(images, word){

    //const el = document.querySelector("#box");
    const imm = document.querySelector('#img1');
    imm.src=images[0];
    imm = document.querySelector('#img2');
    imm.src=images[1];
    imm = document.querySelector('#img3');
    imm.src=images[2];
    imm = document.querySelector('#img4');
    imm.src=images[3];

    const key = document.querySelector('#word');


    //el.style.height = innerHeight/4 + "px";
    //el.style.width = innerWidth/4 + "px";

    /*In questo modo l'immagine ha un limite di altezza che dipende dall'altezza del div box
    if(imm.naturalHeight > el.clientHeight){
        imm.style.height = el.clientHeight + "px";
    }

    //dimensioni della finestra
    //alert(innerWidth); 1280
    //alert(innerHeight); 577

    var timings = {
        duration: 1500
    };

    var keyframes = [
        {
            transform: 'rotate(0) scale(0%,0%)',
            opacity: 0
        },
        {
            transform: 'rotate(720deg) scale(70%,70%)',
            opacity: 1
        }
    ];

    var timings2 = {
        duration: 12000,
        fill: 'both'
    };

    var keyframes2 = [
        {
            offsetDistance: '0%'
        },
        {
            offsetDistance: '100%'
        }
    ];

    var effects = [
        new KeyframeEffect(el,keyframes,timings),
        new KeyframeEffect(el,keyframes2,timings2)
    ];

    var sequence = new SequenceEffect(effects);

    console.log()

    document.timeline.play(sequence);
*/

};