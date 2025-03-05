document.addEventListener('DOMContentLoaded', async function () {


    const next = document.getElementById('next');
    const speaker = document.getElementById('speaker');
    const sounds = document.querySelectorAll('.sound');
    const counter = document.getElementById('counter');
    let id = 0;
    let sound = sounds[0];

    next.addEventListener('click', function() {
        // Incremente counter
        id += 1;
        counter.innerHTML = id+1;

        // Get sound
        sound = sounds[id];
        let specie_name = sound.getAttribute('specie');
        let specie_sounds = JSON.parse(sound.getAttribute('sounds'));
        console.log(specie_name, specie_sounds);


    })



    // sounds.forEach(sound => {
    //     let specie_name = sound.getAttribute('specie');
    //     let specie_sounds = JSON.parse(sound.getAttribute('sounds'));
    //     console.log(specie_name, specie_sounds);
    // })

})
