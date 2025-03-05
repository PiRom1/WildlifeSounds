document.addEventListener('DOMContentLoaded', async function () {

    const csrftoken = document.querySelector('[name="csrf-token"]').content;

    const data = document.getElementById('data');
    let available_species = JSON.parse(data.getAttribute('available-species'));
    const pk_list = data.getAttribute('pk-list');
    const new_specie = document.getElementById('new-specie');
    const available_species_div = document.getElementById('available-species-div');
    const tbody = document.querySelector('table tbody');

    let included_species = [];
    let debounceTimeout;

    console.log(available_species);

    // Fonction de recherche avec debounce
    new_specie.addEventListener('input', function () {
        clearTimeout(debounceTimeout); // Annuler l'exécution précédente si un nouvel input arrive
        debounceTimeout = setTimeout(() => {
            if (new_specie.value === '') {
                included_species = [];
            }
            else {
                // Filtrer les espèces correspondantes
                included_species = available_species.filter(specie =>
                    specie.toLowerCase().includes(new_specie.value.toLowerCase())
                );
            }

            // Créer les éléments <li> à insérer dans la div
            let listItems = included_species.map(specie => {
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


                    fetch('/list/add_specie_to_list', {
                        method: 'POST',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest', // Ajoute cet en-tête pour indiquer qu'il s'agit d'une requête AJAX
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify({specie, pk_list})
                    }).then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log(data.available_names)
                            available_species = JSON.parse(data.available_names);
                            new_specie.focus()
                        }
                        else {
                            console.log(data.error)
                        }
                    })
                
                


                    // Ajouter l'élément à la liste
                    const newRow = document.createElement('tr');
                    const newCell = document.createElement('th');
                    newCell.setAttribute('scope', 'row');
                    newCell.textContent = specie;  // Texte de la nouvelle ligne, tu peux l'adapter
            
                    // Ajouter la cellule à la ligne
                    newRow.appendChild(newCell);
            
                    // Ajouter la nouvelle ligne au <tbody>
                    tbody.appendChild(newRow);
                    new_specie.value = '';
                    available_species_div.innerHTML = '';
                })

                return element;
            });

            // Remplacer tout le contenu de la div avec les nouveaux éléments
            available_species_div.innerHTML = '';
            listItems.forEach(item => available_species_div.appendChild(item));

        }, 50); // Temps d'attente avant d'exécuter la recherche (300ms)
    });


    const plus = document.getElementById('plus');

    plus.addEventListener('click', function() {
        new_specie.style.display = 'block';
    })


});
