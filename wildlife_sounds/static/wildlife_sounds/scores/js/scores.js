document.addEventListener('DOMContentLoaded', async function () {
    const csrftoken = document.querySelector('[name="csrf-token"]').content;

    function plot(x, y, labels, title) {
        // Data for the plot
        var data = [{
            x: x,
            y: y,
            type: 'scatter', // This defines the chart type
            mode: 'markers', // Display both lines and markers
            marker: {
                color: '#fefefe',
                size: 8,
            },
            name: 'Sample Data', // Label for the data series
            text: y.map((val, i) => `Date: ${x[i]}<br>Score: ${val}<br>Liste : ${labels[i]}`), // Add custom text for each point
            hoverinfo: 'text' // Show only the custom text on hover
        }];
        
        // Layout configuration
        var layout = {
            title: {
                text: title,
                font: {
                    family: 'Arial',   // Font family
                    size: 24,          // Font size
                    color: '#fefefe'   // Title color
                }
            },
            xaxis: {
                title: {
                    text: 'Dates',
                    font: {
                        family: 'Arial',  // Font family
                        size: 18,         // Font size
                        color: '#fefefe'  // X axis label color
                    }
                },
                tickfont: {
                    family: 'Arial',     // Font family
                    size: 14,            // Font size for ticks
                    color: '#fefefe',     // Tick label color
                },
                tickangle: 40, 
                showgrid: true,         // Show gridlines on x-axis
                gridcolor: '#fefefe'   // Gridline color
            },
            yaxis: {
                title: {
                    text: 'Scores',
                    font: {
                        family: 'Arial',  // Font family
                        size: 18,         // Font size
                        color: '#fefefe'  // Y axis label color
                    }
                },
                tickfont: {
                    family: 'Arial',     // Font family
                    size: 14,            // Font size for ticks
                    color: '#fefefe'     // Tick label color
                },
                tickangle: -45, 
                showgrid: true,         // Show gridlines on y-axis
                gridcolor: '#fefefe'   // Gridline color
            },
            plot_bgcolor: '#ffffff30',  // Background color inside the plot
            paper_bgcolor: '#ffffff30',  // Background color around the plot
        };

        // Create the plot
        Plotly.newPlot('plotly-chart', data, layout);
    }

    async function get_data() {

        body = {'list_name' : list_selector.value, 'pourcentage' : pourcentage_selector.checked};

        const response = await fetch('/fetch_get_scores', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Ajoute cet en-tête pour indiquer qu'il s'agit d'une requête AJAX
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(body)});
        
        const score_data = await response.json();
        return score_data;
            
    }

    // Get data
    let body;
    const data = document.getElementById('data');   
    const listes = JSON.parse(data.getAttribute('listes'));

    const list_selector = document.getElementById('lists-input');
    const pourcentage_selector = document.getElementById('pourcentage-input');

    // Add list choices 
    listes.forEach(liste => {
        let option = document.createElement("option");
        option.value = liste;
        option.textContent = liste;
        list_selector.appendChild(option);
    })
        
    
    // Plot default data : 
    let scores;
    scores = await get_data();
    plot(scores.score_dates, scores.score_values, scores.score_labels, "Vos scores, toutes listes confondues");
    
    let title;

    list_selector.addEventListener('change', async function() {
        
        if (list_selector.value) {
            title = `Vos scores pour la liste ${list_selector.value}`;
        }
        else {
            title = `Vos scores, toutes listes confondues`;
        }

        
        scores = await get_data();
        plot(scores.score_dates, scores.score_values, scores.score_labels, title);
        
    })


    pourcentage_selector.addEventListener('change', async function () {
        scores = await get_data();
        plot(scores.score_dates, scores.score_values, scores.score_labels, title);
        
    })



})