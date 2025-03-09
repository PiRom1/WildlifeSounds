document.addEventListener('DOMContentLoaded', async function () {

    const data = document.getElementById('data');
    const paths = JSON.parse(data.getAttribute('path'));

    let id = 0;

    const left = document.getElementById('left');
    console.log(paths[id]);
    left.style.cursor = `url(${paths[id]}) 16 16, auto`;


    document.addEventListener("wheel", function (event) {
        if (event.deltaY > 0) {
            id += 1
            

        } else {
            id -= 1
        }
        if (id < 0) {
            id = paths.length - 1;
        }
        else if (id > paths.length - 1) {
            id = 0;
        }

        left.style.cursor = `url(${paths[id]}) 16 16, auto`;

    });
    

})