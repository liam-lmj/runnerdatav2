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

function intial_load() {
    update_charts(bar_chart_safe);
    set_inital_table_values();
    add_inital_sessions(sessions_safe);
    set_event_listners();

    if (plan_string === "new") {
        document.getElementById("copy_button").style.display = "none";
    }
    else {
        document.getElementById("planed_week").style.display = "none";
    }
}

function add_inital_sessions(sessions) {
    session_count_int = 0;

    for (i = 0; i < sessions.length; i++) {
        add_new_session();
        description = document.getElementById("session_desc_" + i.toString()).textContent = sessions[i]["session_desc"];
        description = document.getElementById("session_title_" + i.toString()).textContent = sessions[i]["session_title"];
        description = document.getElementById("session_type_" + i.toString()).value = sessions[i]["session_type"];

    }
}

function set_inital_table_values() {
    for (let i =0; i < days_in_week.length; i++) {
        const am_id = days_in_week[i] + "am";
        const pm_id = days_in_week[i] + "pm";
        const total_id = days_in_week[i] + "total";

        document.getElementById(am_id).textContent = am_values_safe[i];
        document.getElementById(pm_id).textContent = pm_values_safe[i];
        document.getElementById(total_id).textContent = pm_values_safe[i] + am_values_safe[i];
    }
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
            am_values = set_array_values("am");
            pm_values = set_array_values("pm");

            fetch(window.location.pathname, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 'type': 'plan_change', am_values, pm_values})
            })
            .then(response => response.json())
            .then(data => {
                for (let i = 0; i < days_in_week.length; i++) {
                    const total_id = days_in_week[i] + "total";

                    document.getElementById(total_id).textContent = data.totals[i];

                    document.getElementById("total_distance").textContent = data.total_distance;
                    document.getElementById("average_distance").textContent = data.average_distance;
                    document.getElementById("run_count").textContent = data.run_count;

                    const bar_chart = JSON.parse(data.updated_bar_chart);
                    update_charts(bar_chart);
                }
            });      
        }
        }, true);
}

function save_plan() {
    const am_values = set_array_values("am");
    const pm_values = set_array_values("pm");
    const sessions = session_array();

    let week = plan_string;
    if (plan_string === "new") {
        week = document.getElementById("planed_week").value;
    }
    
    fetch(window.location.pathname, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'type': 'plan_save', am_values, pm_values, sessions, week})
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = data.redirect;
    });      
}

function session_array() {
    let array = [];
    for (let i = 0; i < session_count_int; i++) {
        session_dict = {
            "session_title": document.getElementById("session_title_" + i.toString()).textContent,
            "session_desc": document.getElementById("session_desc_" + i.toString()).textContent,
            "session_type": document.getElementById("session_type_" + i.toString()).value,
        }
        array.push(session_dict);
    }

    return array
}

function set_array_values(type) {
    let values = [];

    for (let i = 0; i < days_in_week.length; i++) {
        const id = days_in_week[i] + type;

        values.push(Number(document.getElementById(id).textContent));
    } 

    return values
}

function copy_Plan() {
    document.getElementById("copy_button").style.display = "none";
    document.getElementById("planed_week").style.display = "";
    plan_string = "new";
}