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