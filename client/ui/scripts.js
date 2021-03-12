// Connects python and javascript over bridge eel

// JAVASRIPT -> PYTHON
function mute_button_pressed() {
  eel.mute_button_pressed()
}

function deaf_button_pressed() {
    eel.deaf_button_pressed()
}

function connect_button_pressed() {
  eel.connect_button_pressed()
}

function enter_room(room_name) {
    eel.enter_room(room_name)
}

function close_program() {
    eel.close_program()
}


// PYTHON -> JAVASCRIPT

// WHEN A USER CLICKS CONNECT BUTTON
eel.expose(display_online_users)
function display_online_users(users_connect) {

    // Go through online users and create divs
    var parent = document.getElementById("onlineusers_div");
    var child = document.createElement("onlineuser_div");
    var ips = users_connect.split(",");

    var amount_users = ips.length;
    for (var i = 0; i < amount_users; i++) {
        child.innerHTML = ips[i];
        child.id = "onlineuser_div";
        child.className = "onlineuser_div";
        parent.appendChild(child);
    }

}

eel.expose(update_users_view)
function update_users_view(users_connect, users_room1, users_room2, users_room3) {

    // DISPLAY USER AMOUNT
    //var text = document.getElementById("users_online_text");
    //text.innerText = users_connect;

    // Show dictionairy users in divs
    var users_div = document.getElementById("room1_users");
    users_div.innerText = users_room1

    // Show dictionairy users in divs
    var users_div = document.getElementById("room2_users");
    users_div.innerText = users_room2

    // Show dictionairy users in divs
    var users_div = document.getElementById("room3_users");
    users_div.innerText = users_room3

}

eel.expose(update_room_hover)
function update_room_hover(room_name) {
    // Updates "hover" effect on selected room

    // Remove every other selection
    let i = 1;
    while (i <= 3 ) {
        var roomname = "room"+i+"_button"
        var room_notselected= document.getElementById(roomname);

        // Select room
        room_notselected.style.backgroundColor = "#251c3b";
        room_notselected.style.color = "#9c98a6";
        i++;
    }

    // Select room
    var room_selected = document.getElementById(room_name+"_button");
    room_selected.style.backgroundColor = "#463d58";
    room_selected.style.color = "white";

}



eel.expose(display_rooms)
function display_rooms(amount) {
    // Starts showing rooms once user connected

    // DISPLAY USER AMOUNT
    var room1 = document.getElementById("room1_button");
    var room2 = document.getElementById("room2_button");
    var room3 = document.getElementById("room3_button");
    var room4 = document.getElementById("room4_button");


    // Hide Buttons
    if (room1.style.display === "flex") {
        room1.style.display = "block";
    } else {
        room1.style.display = "flex";
    }
    if (room2.style.display === "flex") {
        room2.style.display = "block";
    } else {
        room2.style.display = "flex";
    }
    if (room3.style.display === "flex") {
        room3.style.display = "block";
    } else {
        room3.style.display = "flex";
    }
    if (room4.style.display === "flex") {
        room4.style.display = "block";
    } else {
        room4.style.display = "flex";
    }

}