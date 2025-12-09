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
    right_div.appendChild(h3);

    const clear_div = document.createElement("div");
    clear_div.className = "w3-clear";

    const desc = document.createElement("h4");
    desc.textContent = "Session Description";
    desc.id = "session_desc_" + session_count_int.toString();

    const select_wrapper = document.createElement("h4");
    const select = document.createElement("select");
    select.className = "drop-down-session";
    select.id = "session_type_" + session_count_int.toString();

    const options = [
        { value: "Current", text: "LT1", selected: true },
        { value: "Past", text: "LT2" },
        { value: "All", text: "Hard" },
        { value: "All", text: "Mixed" }
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
}