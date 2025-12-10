 const days_in_week = ["mon_", "tue_", "wed_", "thu_", "fri_", "sat_", "sun_"];

 function update_charts(bar_chart) {
    Plotly.react('bar', bar_chart.data, bar_chart.layout || {});
}

function add_new_session() {
    const session_container = document.getElementById("session_container");

    const quarter_container = document.createElement("div");
    quarter_container.id = "session_" + session_count_int.toString();
    quarter_container.className = "w3-quarter";
    quarter_container.style.paddingTop = "20px"; 

    const inner_container = document.createElement("div");
    inner_container.className = "w3-container w3-pale-blue w3-padding-16";

    const left_div = document.createElement("div");
    left_div.className = "w3-left";
    const icon = document.createElement("i");
    icon.className = "fa fa-bolt w3-xxxlarge";
    left_div.appendChild(icon);

    const right_div = document.createElement("div");
    right_div.className = "w3-right";
    const h3 = document.createElement("h3");
    h3.id = "session_title_" + session_count_int.toString();
    h3.textContent = "Session Title";
    h3.contentEditable = "true";    
    right_div.appendChild(h3);

    const clear_div = document.createElement("div");
    clear_div.className = "w3-clear";

    const desc = document.createElement("h4");
    desc.textContent = "Session Description";
    desc.contentEditable = "true";   
    desc.id = "session_desc_" + session_count_int.toString();

    const select_wrapper = document.createElement("h4");
    const select = document.createElement("select");
    select.className = "drop-down-session";
    select.id = "session_type_" + session_count_int.toString();

    const options = [
        { value: "lt1", text: "LT1", selected: true },
        { value: "lt2", text: "LT2" },
        { value: "hard", text: "Hard" },
        { value: "mixed", text: "Mixed" }
    ];

    options.forEach(opt_data => {
        const option = document.createElement("option");
        option.value = opt_data.value;
        option.textContent = opt_data.text;
        if (opt_data.selected) option.selected = true;
        select.appendChild(option);
    });

    select_wrapper.appendChild(select);

    inner_container.appendChild(left_div);
    inner_container.appendChild(right_div);
    inner_container.appendChild(clear_div);
    inner_container.appendChild(desc);
    inner_container.appendChild(select_wrapper);

    quarter_container.appendChild(inner_container);

    session_container.appendChild(quarter_container);
    
    session_count_int++;
    update_session_count();
}

function remove_most_recent_session() {
    if (session_count_int > 0 ) {
        session_count_int--;
        const most_recent_session_id = "session_" + session_count_int.toString();
        const most_recent_session = document.getElementById(most_recent_session_id);
        most_recent_session.remove();
        update_session_count();
    }
}

function update_session_count() {
    document.getElementById("session_count").textContent = session_count_int;
}

function set_event_listners() {
    const table = document.getElementById('plan_table');

    table.addEventListener('blur', (event) => {
        const cell = event.target;
        value = cell.textContent;
        value_is_text = isNaN(Number(value));

        if (value_is_text) {
            cell.textContent = "0";
        }
        else {
            let am_values = [];
            let pm_values = [];

            for (let i = 0; i < days_in_week.length; i++) {
                const am_id = days_in_week[i] + "am";
                const pm_id = days_in_week[i] + "pm";

                am_values.push(Number(document.getElementById(am_id).textContent));
                pm_values.push(Number(document.getElementById(pm_id).textContent));
            } 

            fetch(window.location.pathname, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 'type': 'plan_chage', am_values, pm_values})
            })
            .then(response => response.json())
            .then(data => {
                for (let i = 0; i < days_in_week.length; i++) {
                    const total_id = days_in_week[i] + "total";

                    document.getElementById(total_id).textContent = data.totals[i];

                    document.getElementById("total_distance").textContent = data.total_distance;
                    document.getElementById("average_distance").textContent = data.average_distance;
                    document.getElementById("run_count").textContent = data.run_count;

                    const bar_chart = JSON.parse(data.bar_chart);
                    update_charts(bar_chart);
                }
            });      
        }
        }, true);
}