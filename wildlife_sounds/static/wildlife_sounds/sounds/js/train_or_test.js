document.addEventListener('DOMContentLoaded', async function () {

    let overlay;

    function assombrirPage(saufElement) {
        // Créer un overlay sombre couvrant toute la page
        overlay = document.createElement("div");
        overlay.style.position = "fixed";
        overlay.style.top = "0";
        overlay.style.left = "0";
        overlay.style.width = "100vw";
        overlay.style.height = "100vh";
        overlay.style.backgroundColor = "rgba(0, 0, 0, 0.7)"; // Assombrissement
        overlay.style.zIndex = "1000";  
    
        // Placer l'élément au-dessus de l'overlay
        saufElement.style.zIndex = "1001";
    
        // Ajouter l'overlay au body
        document.body.appendChild(overlay);
    
        // Supprimer l'overlay au clic dessus (optionnel)
        overlay.addEventListener("click", () => {
            overlay.remove();
            saufElement.style.zIndex = "";
            saufElement.style.display = 'none';
        });
    }

    const data = document.getElementById('data');
    const method = data.getAttribute('method');
    const test_container = document.getElementById('test-container');
    const input_nb_species = document.getElementById("nb-species-test");
    const counter = document.getElementById('counter');
    const launch_test_button = document.getElementById("launch-test-button");

    console.log("method : ", method);

    const lists = document.querySelectorAll('.list');

    let id_list, nb_species

    
    lists.forEach(list => {

        list.addEventListener('click', function() {
            id_list = list.getAttribute('id-list');
            nb_species = list.getAttribute('nb-species');
            
            if (method === 'train') {
                window.location.href = `/lists/${id_list}/train`;
            }
            
            test_container.style.display = 'block';
            assombrirPage(test_container);
            input_nb_species.max = nb_species;
            input_nb_species.value = nb_species;
            counter.innerHTML = nb_species;
            
        })
        
    })

    launch_test_button.addEventListener('click', function() {
        window.location.href = `/lists/${id_list}/test?nb_species=${input_nb_species.value}`;
    })
    

})