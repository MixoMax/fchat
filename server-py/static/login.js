function change_password_visibility(){
    const password_visibility_button = document.getElementById("password_visibility_button"); 
    const password_field = document.getElementById("password");
    if (password_visibility_button.value == "true") {
        password_field.type = "password";
        password_visibility_button.value = "false";
        password_visibility_button.innerHTML = "visibility";
    } else {
        password_field.type = "text";
        password_visibility_button.value = "true";
        password_visibility_button.innerHTML = "visibility_off";
    }
}

function login_on_enter(event) {
    if (event.keyCode == 13) {
        console.log("enter")
        login();
    }
}

function login() {
    const sender = document.getElementById("username").value;
    if(sender == "") return;
    //save username in local storage
    localStorage.setItem("username", sender);
    //redirect to chat page
    window.location.replace("/chat");
}