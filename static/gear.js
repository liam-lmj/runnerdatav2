function update_table(data, unit) {
    const table_body = document.getElementById("gear_table").querySelector("tbody");
    table_body.innerHTML = ""; 
    const headers = ["gear_name", "total_distance", "default_type", "active"];
    const select_headers = ["default_type", "active"];
    const default_type_option = ["Easy", "Session", "None"];
    const active_options = ["Active", "Retired"];

    for (let gear of data) {
        const tr = document.createElement("tr");
        tr.id = gear["gear_id"]
        for (let header of headers) {
            const cell = document.createElement("td");

            if (select_headers.includes(header)) {
                const select = document.createElement("select");
                select.className = "table-drop-down";
                let options = header === "default_type" ? default_type_option : active_options;

                for (let choose of options) {
                    const option = document.createElement("option");
                    option.value = choose;
                    option.textContent = choose;

                    if (choose === gear[header]) {
                        option.selected = true;
                    }
                    select.appendChild(option);
                }
                select.id = header + "-" + gear["gear_id"];

                cell.appendChild(select);
            }
            else {
                cell.textContent = gear[header];
                cell.contentEditable = "true";  
                cell.id = header + "-" + gear["gear_id"];
            }


            tr.appendChild(cell);
        }
        table_body.appendChild(tr); 
    }
}

function set_event_listners(data) {
    update_table(data, "miles");

    const table = document.getElementById('gear_table');

    table.addEventListener('blur', (event) => {
        const cell = event.target;
        if (cell.tagName === 'TD') {
            const row = cell.closest('tr'); 
            const row_id = row.getAttribute('id');

            get_values(row_id);
        }
        }, true);

    table.addEventListener('change', (event) => {
        const target = event.target;
        if (target.tagName === 'INPUT' || target.tagName === 'SELECT') {
            const row = target.closest('tr');
            const row_id = row.getAttribute('id');

            get_values(row_id);
        }
        });
}

function get_values(id) {
    const shoe = document.getElementById('gear_name-' + id).textContent;
    const total_distance = document.getElementById('total_distance-' + id).textContent;
    const default_type = document.getElementById('default_type-' + id).value;
    const active = document.getElementById('active-' + id).value;

    fetch(window.location.pathname, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'type': 'gear_change', shoe, total_distance, default_type, active, id })
    })
    .then(response => response.json())
    .then(data => {
        update_table(data.updated_data, "miles");
    });
}

function add_new_row(){    
    fetch(window.location.pathname, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'type': 'gear_change', 
                                "shoe": "New Trainer", 
                                "total_distance": "0",
                                "default_type": "None", 
                                "active": "Active",
                                "id": "0" }) //default id that can't exist
    })
    .then(response => response.json())
    .then(data => {
        update_table(data.updated_data, "miles");
    });

    table_body.appendChild(tr);
}