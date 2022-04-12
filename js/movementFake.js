function move(images){

    const el = document.querySelector("#box");
    //const imm = document.querySelector('#img');
    //imm.src=images;

    //el.style.height = innerHeight/4 + "px";
    //el.style.width = innerWidth/4 + "px";

    /*In questo modo l'immagine ha un limite di altezza che dipende dall'altezza del div box
    if(imm.naturalHeight > el.clientHeight){
        imm.style.height = el.clientHeight + "px";
    }*/

    //dimensioni della finestra
    //alert(innerWidth); 1280
    //alert(innerHeight); 577

    var timings = {
        duration: 1500
    };

    var keyframes = [
        {
            transform: 'translateZ(-100000px)',
        },
        {
            transform: 'translateZ(-100px)',
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
        //new KeyframeEffect(el,keyframes2,timings2)
    ];

    var sequence = new SequenceEffect(effects);

    document.timeline.play(sequence);


};