document.addEventListener('DOMContentLoaded', async function () {
    const csrftoken = document.querySelector('[name="csrf-token"]').content;

    let name, call, song, country, sound, type
    const submit_button = document.getElementById('submit');

    submit_button.addEventListener('click', function() {
        name = document.getElementById('name').value;
        call = document.getElementById('call').checked;
        song = document.getElementById('song').checked;
        country = document.getElementById('country').value;
        sound = document.getElementById('sound').files[0];
        
        console.log(JSON.stringify({name : name,type : type,country : country,sound : sound}));

        type = 'song';
        if (call) {
            type = 'call';
        }

        let formData = new FormData();
        formData.append('name', name);
        formData.append('type', type);
        formData.append('country', country);
        formData.append('sound', sound); // Ajout du fichier
        formData.append('csrfmiddlewaretoken', csrftoken); // Ajout du token CSRF

        fetch('/add_sound_fetch', {
            method: 'POST',
            body: formData
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/list';
            }
            else {
                console.log(data.error)
            }
        })
    
    })


})