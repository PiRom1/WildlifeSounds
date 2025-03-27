document.addEventListener('DOMContentLoaded', async function () {

    const data = document.getElementById('data');
    const nb_species = data.getAttribute('nb_species');
    const pk = data.getAttribute('pk');

    let audio = new Audio();

    function play_sound(sound) {
        console.log(sound);
        if (audio) {
            audio.pause();
            audio.currentTime = 0;
        }

        audio = new Audio(sound);
        audio.play().catch(error => {
            console.log(`Erreur : ${error}`);
        });
    };

    

    const terminer = document.getElementById('terminer');
    const next = document.getElementById('next');
    const speaker = document.getElementById('speaker');
    const all_sounds = document.querySelectorAll('.sound');
    const counter = document.getElementById('counter');

    let id = 0;

    let specie_sounds = JSON.parse(all_sounds[id].getAttribute('sounds'));
    let specie_name = all_sounds[id].getAttribute('specie');
    let scientific_specie_name = all_sounds[id].getAttribute('scientific_specie');

    console.log(specie_name);
    let sound;
    
    sound = specie_sounds[Math.floor(Math.random() * specie_sounds.length)]
    play_sound(sound);


    speaker.addEventListener('click', function() {
        sound = specie_sounds[Math.floor(Math.random() * specie_sounds.length)]
        play_sound(sound);
    })


    next.addEventListener('click', function() {
        // Incremente counter
        id += 1;
        counter.innerHTML = id+1;

        mystery_bird.style.display = 'block';
        bird_name.innerHTML = '';
        bird_name.style.display = 'none';
    
        specie_name = all_sounds[id].getAttribute('specie');
        scientific_specie_name = all_sounds[id].getAttribute('scientific_specie');
        specie_sounds = JSON.parse(all_sounds[id].getAttribute('sounds'));
        audio.pause();
        audio.currentTime = 0;

        console.log(specie_name);
    
        sound = specie_sounds[Math.floor(Math.random() * specie_sounds.length)]
        play_sound(sound);
        
        
        if ((id+1).toString() === nb_species) {
            console.log('finito');
            next.style.display = 'none';
            terminer.style.display = 'block';
        }
       
        
    })


    terminer.addEventListener('click', function() {
        window.location.href = `/lists/${pk}`;
    })


    const mystery_bird = document.getElementById('mystery_bird');
    const bird_name = document.getElementById('bird_name');

    mystery_bird.addEventListener('click', function() {
        mystery_bird.style.display = 'none';
        bird_name.style.display = 'block';
        bird_name.innerHTML = `${specie_name} (<i>${scientific_specie_name}</i>)`;
    })



})
