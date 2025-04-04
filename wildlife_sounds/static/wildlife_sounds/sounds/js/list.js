document.addEventListener('DOMContentLoaded', async function () {

    const csrftoken = document.querySelector('[name="csrf-token"]').content;

    
    const data = document.getElementById('data');
    const sounds0 = JSON.parse(data.getAttribute('sounds0'));
    const all_species = JSON.parse(data.getAttribute("all-species"));
    const table = document.getElementById('body-table');

    const search = document.getElementById('text_search');
    const cross = document.getElementById('cross');
    let audio = null;


    // Sound
    function launch_speakers() {
        const speakers = document.querySelectorAll('.speaker');

        speakers.forEach(speaker => {
            let speaker_url = speaker.getAttribute('sound')
            speaker.addEventListener('click', function() {
                if (audio) {
                    audio.pause();
                    audio.currentTime = 0;
                }
                audio = new Audio(speaker_url);
                audio.play();
            })
        })
    }


    function addRow(data) {
        const row = document.createElement('tr');
        row.classList.add("table-row");

        
        // Ajouter les attributs dynamiquement
        for (const key in data) {
            row.setAttribute(key, data[key]);
        }
        
        // Créer et ajouter la première cellule (th)
        const th = document.createElement("th");
        th.scope = "row";
        th.innerHTML = data.vernacular_name;
        row.appendChild(th);
        
        // Créer et ajouter la cellule du haut-parleur
        const speakerTd = document.createElement("td");
        speakerTd.classList.add("speaker");
        speakerTd.setAttribute("sound", data.sound_url);
        speakerTd.innerHTML = "&#128266"; // Icône de haut-parleur
        row.appendChild(speakerTd);
        
        // Ajouter les autres cellules dynamiquement
        const keysToIgnore = ["vernacular_name", "sound_url"]; // Éviter les doublons
        for (const key in data) {
            if (!keysToIgnore.includes(key)) {
                const td = document.createElement("td");
                td.innerHTML = data[key];
                row.appendChild(td);
            }
        }
        
        // Ajouter la ligne au tableau
        table.appendChild(row);
    }


    cross.addEventListener('click', function() {
        search.value = '';
        table.innerHTML = '';
        sounds0.forEach(sound => {
            if (sound) {
                addRow(sound);
            }
        })
        launch_speakers();
    })



    // Mettre les premières données
    sounds0.forEach(sound => {
        if (sound) {
            addRow(sound);
        }
    })

    launch_speakers();





    let included_species = [];
    let debounceTimeout;
    let query_species = document.getElementById('query-species');

    search.addEventListener('input', function () {
        clearTimeout(debounceTimeout); // Annuler l'exécution précédente si un nouvel input arrive
        debounceTimeout = setTimeout(() => {
            if (search.value === '') {
                included_species = [];
                sounds0.forEach(sound => {
                    if (sound) {
                        addRow(sound);
                    }
                })
            
                launch_speakers();
            }
            else {
                // Filtrer les espèces correspondantes
                included_species = all_species.filter(specie =>
                    specie.toLowerCase().includes(search.value.toLowerCase())
                );
            }

            const fragment = document.createDocumentFragment();

            
            included_species.forEach(specie => {
                const element = document.createElement("li");
                element.textContent = specie;
                element.style.border = '1px solid black';
                element.style.padding = '2px';
                element.style.backgroundColor = 'rgba(242, 241, 207, 0.50)';
                element.style.cursor = 'pointer';

                
                element.addEventListener('mouseover', function() {
                    element.style.backgroundColor = 'rgba(242, 241, 207, 0.33)';  // Couleur de survol
                });
                element.addEventListener('mouseout', function() {
                    element.style.backgroundColor = 'rgba(242, 241, 207, 0.50)';  // Couleur normale
                });


                element.addEventListener('click', function() {

                    search.value = specie;
                    query_species.innerHTML = '';


                    fetch('/all/fetch_specie', {
                        method: 'POST',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest', // Ajoute cet en-tête pour indiquer qu'il s'agit d'une requête AJAX
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify({specie})
                    }).then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            table.innerHTML = '';
                            data.data.forEach(sound => {
                                addRow(sound)
                            })
                            launch_speakers();
                        }
                        else {
                            console.log(data.error)
                        }
                    })
                })
    

                fragment.appendChild(element);

            })

            query_species.innerHTML = '';
            query_species.appendChild(fragment);


        }, 100)

    })

            


});