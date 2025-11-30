function update_milage_trend_bar(bar_chart) {
    Plotly.react('mileage_trend_bar', bar_chart.data, bar_chart.layout || {});
}

function update_pace_trend_line(line_chart) {
    Plotly.react('pace_trend_line', line_chart.data, line_chart.layout || {});
}

function update_time_pie_chart(pie_chart) {
    Plotly.react('time_pie_chart', pie_chart.data, pie_chart.layout || {});
}

function update_run_count_bar(bar_chart) {
    Plotly.react('run_count_trend', bar_chart.data, bar_chart.layout || {});
}

function initialiseCharts(mileage_trend_bar, pace_trend_line, time_pie_chart, run_count_plot) {
    console.log(mileage_trend_bar);
    update_milage_trend_bar(mileage_trend_bar);
    update_pace_trend_line(pace_trend_line);
    update_time_pie_chart(time_pie_chart);
    update_run_count_bar(run_count_plot);
    
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

    time_dropdown.addEventListener('change', function() {
        const selected_type = this.value;
        fetch('/dashboard', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selected_type, 'type': 'pie_time_change' })
        })
        .then(response => response.json())
        .then(data => {
            const pie_chart = JSON.parse(data.plot);
            update_time_pie_chart(pie_chart);
        });
    });

    run_count_dropdown.addEventListener('change', function() {
        const selected_type = this.value;
        fetch('/dashboard', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selected_type, 'type': 'bar_count_change' })
        })
        .then(response => response.json())
        .then(data => {
            const bar_chart = JSON.parse(data.plot);
            update_run_count_bar(bar_chart);
        });
    });
}
