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
eel.expose(update_users)
function update_users(amount) {

    // DISPLAY USER AMOUNT
    var text = document.getElementById("users_online_text");
    text.innerText = "Users online: " + amount;
}

eel.expose(update_room)
function update_room(room_name) {
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
    var room_selected = document.getElementById(room_name);
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