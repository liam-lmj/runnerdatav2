function update_table(updated_data) {
    const table_body = document.getElementById("activity_table").querySelector("tbody");
    table_body.innerHTML = ""; 
    const headers = ["lap_split", "lap_type", "lap_meters", "lap_pace", "lap_formatted_time", "lap_heartrate_average"]

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
}