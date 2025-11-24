function update_charts(pie_chart) {
    Plotly.react('pie', pie_chart.data, pie_chart.layout || {});
}

function update_table(updated_data) {
    const table_body = document.getElementById("activity_table").querySelector("tbody");
    table_body.innerHTML = ""; 
    const headers = ["formatted_date", "run_description", "activity_meters", "formated_time", "heartrate_average"]
    const link_field = "run_description";

    for (let activity of updated_data) {
        const tr = document.createElement("tr");
        for (let header of headers) {

            const cell = document.createElement("td");

            if (header === link_field) {
                const link = document.createElement("a");
                link.href = activity["activity_url"];
                link.textContent = activity[header];
                cell.appendChild(link);
            }
            else {
                cell.textContent = activity[header];
            }

            tr.appendChild(cell);
        }
        table_body.appendChild(tr); 
    }
}

function initialiseCharts(pie_chart, data) {
    update_charts(pie_chart);
    update_table(data);

    const week_selector = document.getElementById("week");
    const total_distance = document.getElementById("total_distance");
    const average_heartrate = document.getElementById("average_heartrate");
    const formated_total_time = document.getElementById("formated_total_time");
    const run_count = document.getElementById("run_count");


    week_selector.addEventListener('change', function() {
        const selected_week = this.value;
        fetch('/week', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selected_week, 'type': 'week_change' })
        })
        .then(response => response.json())
        .then(data => {
            const pie_chart = JSON.parse(data.pie_chart);
            total_distance.innerText = data.total_distance;
            average_heartrate.innerText = data.average_heartrate;
            formated_total_time.innerText = data.formated_total_time;
            run_count.innerText = data.run_count;
            const updated_data = data.updated_data
            update_charts(pie_chart);
            update_table(updated_data);
        });
    });
}