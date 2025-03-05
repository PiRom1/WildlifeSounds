document.addEventListener('DOMContentLoaded', async function () {

    const button = document.getElementById('button');
    const loader = document.getElementById('loader');


    button.addEventListener('click', function() {
        loader.style.display = 'block';

        fetch('/load_data_xeno_canto', {
            method: 'GET',
        }).then(response => response.json())
        .then(data => {
        })
    

    })


})
