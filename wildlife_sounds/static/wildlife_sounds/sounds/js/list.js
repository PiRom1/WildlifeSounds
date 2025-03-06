document.addEventListener('DOMContentLoaded', async function () {


    // Sound
    const speakers = document.querySelectorAll('.speaker');
    let audio = null;

    speakers.forEach(speaker => {
        let speaker_url = speaker.getAttribute('sound')
        speaker.addEventListener('click', function() {
            if (audio) {
                audio.pause();
                audio.currentTime = 0;
            }
            console.log('pseaker url ', speaker_url);
            audio = new Audio(speaker_url);
            audio.play();
        })
    })



    // Filter

    function check_if_row_contains(row, attributes, text) {

        let attribute_name = '';
        attributes.forEach(attribute => {
            attribute = row.getAttribute(attribute);
            attribute_name += attribute + ' / '
        })

            
        if (attribute_name.toLowerCase().includes(text.toLowerCase())) {
            row.style.display = 'table-row';            
        }
        else {
            row.style.display = 'none';
        }

    }
    

    const rows = document.querySelectorAll('.table-row');
    const text_search = document.getElementById('text_search');
    console.log(text_search.value);
    text_search.addEventListener('input', function() {
        rows.forEach(row => {
            const attributes = ['vernacular_name',
                                'scientific_name',
                                'order_name',
                                'family_name',
                                'genus_name',
                                'taxon_name',
                                'type_name',
                                'country_name']

            check_if_row_contains(row, attributes, text_search.value);
            
        })
    })


});