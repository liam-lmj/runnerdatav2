function update_table(data, unit) {
    const table_body = document.getElementById("gear_table").querySelector("tbody");
    table_body.innerHTML = ""; 
    const headers = ["gear_name", "distance", "default_type", "active"];
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

                cell.appendChild(select);
            }
            else {
                cell.textContent = gear[header];
                cell.contentEditable = "true";  
                cell.id = gear[header] + "-" + gear["gear_id"]
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
    const shoe = document.getElementById('gear_name-' + id).textContent
    const miles = document.getElementById('miles-' + id).textContent
    const default_type = document.getElementById('default_type-' + id).value
    const active = document.getElementById('active-' + id).value

    console.log('Row edited:', shoe, miles, default_type, active);
}