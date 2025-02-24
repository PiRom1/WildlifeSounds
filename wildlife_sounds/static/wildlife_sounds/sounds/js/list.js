document.addEventListener('DOMContentLoaded', async function () {

    const speakers = document.querySelectorAll('.speaker');
    let audio = null;

    speakers.forEach(speaker => {
        console.log(speaker);
        let speaker_url = speaker.getAttribute('sound')
        speaker.addEventListener('click', function() {
            if (audio) {
                audio.pause();
                audio.currentTime = 0;
            }
            audio = new Audio(speaker_url);
            audio.play();
            console.log(speaker_url);
        })
    })

});