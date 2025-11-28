function update_table(updated_data) {
    const table_body = document.getElementById("activity_table").querySelector("tbody");
    table_body.innerHTML = ""; 
    const headers = ["lap_split", "lap_type", "lap_meters", "lap_formatted_time", "lap_pace", "lap_heartrate_average", "lap_cadence"]

    for (let activity of updated_data) {
        const tr = document.createElement("tr");
        for (let header of headers) {

            const cell = document.createElement("td");
            cell.textContent = activity[header];

            tr.appendChild(cell);
        }
        table_body.appendChild(tr); 
    }
}

function initialise_content(data) {
    update_table(data);

    const lap_selector = document.getElementById("lap_type");
    const total_distance = document.getElementById("total_distance");
    const average_heartrate = document.getElementById("average_heartrate");
    const formated_total_time = document.getElementById("formated_total_time");
    const run_count = document.getElementById("Cadence");
    
    lap_selector.addEventListener('change', function() {
        const selected_type = this.value;
        fetch(window.location.pathname, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selected_type, 'type': 'lap_change', })
        })
        .then(response => response.json())
        .then(data => {
            total_distance.innerText = data.total_distance;
            average_heartrate.innerText = data.average_heartrate;
            formated_total_time.innerText = data.formated_total_time;
            cadence.innerText = data.cadence;
            const updated_data = data.updated_data
            update_table(updated_data);
        });
    });

}