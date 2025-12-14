function update_bar(bar_chart) {
    Plotly.react('bar', bar_chart.data, bar_chart.layout || {});
}

function update_table(updated_data) {
    const table_body = document.getElementById("plan_table").querySelector("tbody");
    table_body.innerHTML = ""; 
    const headers = ["week", "formatted_distance", "session_types", "outcome"]
    const link_field = "week";

    for (let plan of updated_data) {
        const tr = document.createElement("tr");
        for (let header of headers) {

            const cell = document.createElement("td");

            if (header === link_field) {
                const link = document.createElement("a");
                link.href = base_url + plan["week"];
                link.textContent = plan[header];
                cell.appendChild(link);
            }
            else {
                cell.textContent = plan[header];
            }

            tr.appendChild(cell);
        }
        table_body.appendChild(tr); 
    }
}

function initialiseContent(data, bar_chart) {
    update_bar(bar_chart);
    update_table(data);

    const training_selector = document.getElementById("drop_down");

    training_selector.addEventListener('change', function() {
        const selected_type = this.value;
        fetch(window.location.pathname, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selected_type, 'type': 'training_change' })
        })
        .then(response => response.json())
        .then(data => {
            const bar_chart = JSON.parse(data.bar_chart);
            const updated_data = data.updated_data;
            update_bar(bar_chart);
            update_table(updated_data);
        });
    });
}