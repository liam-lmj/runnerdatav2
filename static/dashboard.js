function update_milage_trend_bar(bar_chart) {
    Plotly.react('mileage_trend_bar', bar_chart.data, bar_chart.layout || {});
}

function update_pace_trend_line(line_chart) {
    Plotly.react('pace_trend_line', line_chart.data, line_chart.layout || {});
}

function initialiseCharts(mileage_trend_bar, pace_trend_line) {
    console.log(mileage_trend_bar);
    update_milage_trend_bar(mileage_trend_bar);
    update_pace_trend_line(pace_trend_line);

    const mileage_trend_selector = document.getElementById("mileage_trend_dropdown");

    mileage_trend_dropdown.addEventListener('change', function() {
        const selected_type = this.value;
        fetch('/dashboard', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selected_type, 'type': 'mileage_trend_change' })
        })
        .then(response => response.json())
        .then(data => {
            const bar_chart = JSON.parse(data.plot);
            update_milage_trend_bar(bar_chart);
        });
    });

    pace_trend_dropdown.addEventListener('change', function() {
        const selected_type = this.value;
        fetch('/dashboard', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selected_type, 'type': 'pace_trend_change' })
        })
        .then(response => response.json())
        .then(data => {
            const line_chart = JSON.parse(data.plot);
            update_pace_trend_line(line_chart);
        });
    });
}
