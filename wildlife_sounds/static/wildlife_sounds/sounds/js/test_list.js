document.addEventListener('DOMContentLoaded', async function () {
    const csrftoken = document.querySelector('[name="csrf-token"]').content;

    //  Data
    const data = document.getElementById('data');
    const nb_species = data.getAttribute('nb_species');
    const pk = data.getAttribute('pk');
    

    // Audio
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



    let html_score = document.getElementById('score');
    let score = 0;
    let nb_vernacular = 0;
    let nb_scientific = 0;
    let nb_error = 0;
    const terminer = document.getElementById('terminer');
    const next = document.getElementById('next');
    const speaker = document.getElementById('speaker');
    const all_sounds = document.querySelectorAll('.sound');
    const counter = document.getElementById('counter');

    let id = 0;
    let specie_sounds, vernacular_name, scientific_name

    const result = document.getElementById('result');

    function show_result_popup(success, vernacular_name, scientific_name, score) {
        if (success) {
            result.style.backgroundColor = '#7db856ca';
            result.innerHTML = 'Bravo !<br>'
        }
        else {   
            result.style.backgroundColor = '#FF746Cca';
            result.innerHTML = 'Dommage ...<br>'
        }

        result.innerHTML += `${vernacular_name} <i>${scientific_name}</i><br>`
        if (score > 1) {
            result.innerHTML += `+${score} points`;
        }
        else {
            result.innerHTML += `+${score} point`;
        }
        

        result.style.display = 'block';

    }




    function get_specie_data(id) {
        let specie_sounds = JSON.parse(all_sounds[id].getAttribute('sounds'));
        let vernacular_name = all_sounds[id].getAttribute('vernacular_specie');
        let scientific_name = all_sounds[id].getAttribute('scientific_specie');
    
        return {
            specie_sounds: specie_sounds,
            vernacular_name: vernacular_name,
            scientific_name: scientific_name
        };
    }
    let sound;

    let specieData = get_specie_data(id);
    
    console.log(specieData);
    
    sound = specieData.specie_sounds[Math.floor(Math.random() * specieData.specie_sounds.length)]
    play_sound(sound);
    

    
    speaker.addEventListener('click', function() {
        sound = specieData.specie_sounds[Math.floor(Math.random() * specieData.specie_sounds.length)]
        play_sound(sound);
    })


    // Validate

    const text_input = document.getElementById('text-input');
    const validate = document.getElementById('validate');

    validate.addEventListener('click', function() {

        if (text_input.value.toLowerCase() === specieData.vernacular_name.toLowerCase()) {
            score += 1;
            nb_vernacular += 1;
            console.log('nom vernaculaire ok');
            show_result_popup(true, specieData.vernacular_name, specieData.scientific_name, 1);

        }
        else if (text_input.value.toLowerCase() === specieData.scientific_name.toLocaleLowerCase()) {
            score += 3;
            nb_scientific += 1;
            console.log('nom scientifique ok !');
            show_result_popup(true, specieData.vernacular_name, specieData.scientific_name, 3);
        }
        else {
            console.log('NUL');
            nb_error += 1;
            show_result_popup(false, specieData.vernacular_name, specieData.scientific_name, 0);
        }

        html_score.innerHTML = score;


        text_input.value = '';

        // Incremente counter
        id += 1;
        counter.innerHTML = id+1;

        
        if (id + 1 <= parseInt(nb_species)) {
            specieData = get_specie_data(id);
            audio.pause();
            audio.currentTime = 0;


            console.log(specieData);
            sound = specieData.specie_sounds[Math.floor(Math.random() * specieData.specie_sounds.length)]
            play_sound(sound);
        }

        if (id + 1 === parseInt(nb_species) + 1) {
            counter.innerHTML = id;
            console.log('finito');
            validate.style.display = 'none';
            terminer.style.display = 'block';
            text_input.style.display = 'none';
            console.log('score : ', score);
        }



        
        
    })


    terminer.addEventListener('click', function() {

        
        fetch('/record_score', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Ajoute cet en-tête pour indiquer qu'il s'agit d'une requête AJAX
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({pk, score, nb_vernacular, nb_scientific, nb_error, nb_species})
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.success) {
                window.location.href = '/lists';
            }
            else {
                console.log(data.error)
            }
        })
    
    })




})
